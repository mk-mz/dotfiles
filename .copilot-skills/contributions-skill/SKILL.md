---
name: contributions
description: This skill should be used when the user asks to "summarize my contributions", "write a self-review summary", "generate a quarterly accomplishments summary", "pull together my PRs and kudos", "create a YTD impact summary", or needs a narrative summary of GitHub work, recognition, and optional Slack follow-up for a specific time period. CRITICAL - Confirm the GitHub org, warn about Slack/privacy concerns before reading Slack data, and continue with GitHub-only analysis if Slack access is unavailable or unapproved.
---

# Contributions - Build an Accomplishments Summary from GitHub and Slack Signals

Use this skill to turn a date range into a narrative summary of authored work, reviews, issue participation, recognition, and cross-team impact.

## When to Use This Skill

- The user needs a monthly, quarterly, or YTD accomplishments summary
- The user wants self-review or performance evidence grounded in GitHub activity
- The user wants authored PRs separated from review contributions
- The user wants recognition from GitHub Discussions and optional Slack mentions

## Prerequisites

- `gh` is installed and authenticated
- `gh auth token` returns a token with enough scope to read PRs, issues, and discussions
- `python3` is available
Resolve the skill directory before running bundled scripts:

```bash
if [ -d .github/skills/contributions-skill ]; then
  SKILL_DIR=.github/skills/contributions-skill
elif [ -d "$HOME/.copilot/skills/contributions-skill" ]; then
  SKILL_DIR="$HOME/.copilot/skills/contributions-skill"
else
  echo "❌ contributions-skill is not installed in .github/skills or ~/.copilot/skills"
  exit 1
fi
```

## Step 1: Normalize Inputs

Parse the requested period into `START_DATE` and `END_DATE` in `YYYY-MM-DD` format.

Examples:

- `YTD` → Jan 1 of current year through today
- `Q1 2026` → `2026-01-01` to `2026-03-31`
- `last quarter` → previous calendar quarter
- `2026-01-01 to 2026-03-31` → explicit range

Resolve:

- `GH_USER` from `gh api user --jq .login`
- `GH_ORG` from the user if it is not obvious
- `SLACK_USER` only if the user's Slack display name differs from the GitHub handle
- `SLACK_TEAM` only if the Slack workspace domain differs from the GitHub org

```bash
GH_USER=$(gh api user --jq .login)
GH_ORG="github"
GH_TOKEN=$(gh auth token)
SLACK_TEAM="${SLACK_TEAM:-$GH_ORG}"
SLACK_USER="${SLACK_USER:-$GH_USER}"
RUN_TS=$(date +%H%M)
WORK_DIR="$HOME/contributions-${START_DATE}-to-${END_DATE}-${RUN_TS}"
mkdir -p "$WORK_DIR"/{phase1,phase2,phase3,phase4,phase5}
```

## Step 2: Show Slack Privacy Warning Before Slack Access

Before any Slack follow-up, warn the user that Slack data may contain private or sensitive information. Ask for confirmation before using Slack. If the user declines, skip Slack and continue with GitHub-only analysis.

Use wording like:

```text
⚠️ Slack data may contain private conversations, internal plans, customer details, or other sensitive information.
I can continue with GitHub-only data, or include Slack if you want and have permission to use it.
```

This packaged skill does not include a bundled Slack automation helper. If the environment does not already have approved Slack tooling, stop at GitHub-only analysis and say so explicitly.

## Step 3: Launch Parallel Data Collection

Run independent collection phases in parallel when possible.

### A. Search Authored PRs, Review-Requested PRs, and Issues

```bash
gh search prs --author="$GH_USER" --created="${START_DATE}..${END_DATE}" --owner="$GH_ORG" --limit=200 \
  --json number,title,repository,state,createdAt,url > "$WORK_DIR/phase1/prs-authored.json"

gh search prs --review-requested="$GH_USER" --created="${START_DATE}..${END_DATE}" --owner="$GH_ORG" --limit=200 \
  --json number,title,repository,state,createdAt,url > "$WORK_DIR/phase1/prs-reviewed-raw.json"

gh search issues --author="$GH_USER" --created="${START_DATE}..${END_DATE}" --owner="$GH_ORG" --limit=200 \
  --json number,title,repository,state,createdAt,url > "$WORK_DIR/phase1/issues-authored.json"

gh search issues --assignee="$GH_USER" --created="${START_DATE}..${END_DATE}" --owner="$GH_ORG" --limit=200 \
  --json number,title,repository,state,createdAt,url > "$WORK_DIR/phase1/issues-assigned.json"

gh search issues --mentions="$GH_USER" --created="${START_DATE}..${END_DATE}" --owner="$GH_ORG" --limit=200 \
  --json number,title,repository,state,createdAt,url > "$WORK_DIR/phase1/issues-mentioned.json"
```

If a search approaches API result limits, split the date range and deduplicate by `repo + number`.

Combine the three issue searches into `issues-all-deduped.json` and preserve all matching roles:

```bash
python3 - <<'PY'
import json, os
work_dir = os.environ["WORK_DIR"]
phase1 = os.path.join(work_dir, "phase1")
inputs = [
    ("authored", "issues-authored.json"),
    ("assigned", "issues-assigned.json"),
    ("mentioned", "issues-mentioned.json"),
]
merged = {}
for role, filename in inputs:
    path = os.path.join(phase1, filename)
    for item in json.load(open(path)):
        key = (item["repository"]["nameWithOwner"], item["number"])
        entry = merged.setdefault(key, dict(item, roles=[]))
        if role not in entry["roles"]:
            entry["roles"].append(role)
output = os.path.join(phase1, "issues-all-deduped.json")
json.dump(list(merged.values()), open(output, "w"), indent=2)
print(f"Wrote {len(merged)} unique issues to {output}")
PY
```

### B. Filter Meaningful Review Work

```bash
python3 "$SKILL_DIR/scripts/filter-reviewed-prs.py" \
  --username "$GH_USER" \
  --input "$WORK_DIR/phase1/prs-reviewed-raw.json" \
  --output-dir "$WORK_DIR/phase2"
```

Expected output includes:

```text
FILTER RESULTS
Total processed: 37
Genuinely reviewed (kept): 14
Discarded: 23
Errors: 0
```

### C. Fetch Detailed PR and Issue Data

Authored PRs and issues:

```bash
python3 "$SKILL_DIR/scripts/fetch-details.py" \
  --username "$GH_USER" \
  --prs-authored "$WORK_DIR/phase1/prs-authored.json" \
  --prs-reviewed "$WORK_DIR/phase2/prs-genuinely-reviewed.json" \
  --issues "$WORK_DIR/phase1/issues-all-deduped.json" \
  --output-dir "$WORK_DIR/phase5" \
  --skip-reviewed
```

Reviewed PR details:

```bash
python3 "$SKILL_DIR/scripts/fetch-details.py" \
  --username "$GH_USER" \
  --prs-authored "$WORK_DIR/phase1/prs-authored.json" \
  --prs-reviewed "$WORK_DIR/phase2/prs-genuinely-reviewed.json" \
  --issues "$WORK_DIR/phase1/issues-all-deduped.json" \
  --output-dir "$WORK_DIR/phase5" \
  --skip-authored --skip-issues
```

Expected output includes authored lines changed, reviewed inline comment count, and issue totals.

### D. Search GitHub Discussions

```bash
python3 "$SKILL_DIR/scripts/search-discussion-kudos.py" \
  --username "$GH_USER" \
  --org "$GH_ORG" \
  --start-date "$START_DATE" \
  --end-date "$END_DATE" \
  --output-dir "$WORK_DIR/phase3"
```

Expected output:

```text
DISCUSSION RESULTS
Mention discussions analyzed: 12
Kudos entries found:          4
Discussions authored:         3
```

### E. Optionally Incorporate Slack Notes

Only do this if the user approved Slack access **and** the environment already has approved Slack tooling. Do not invent or install ad hoc Slack scraping dependencies as part of this skill.

If Slack tooling is present, use a separate `SLACK_TEAM` value rather than assuming it matches `GH_ORG`.

If Slack auth fails, approved tooling is unavailable, or the workspace/domain is uncertain, report that clearly and continue with GitHub-only results.

## Step 4: Merge and Sanity Check Results

Merge authored and reviewed PR detail files before synthesis:

```bash
python3 - <<'PY'
import json, os
work_dir = os.environ["WORK_DIR"]
phase5 = os.path.join(work_dir, "phase5")
authored_path = os.path.join(phase5, "pr-details-authored.json")
reviewed_path = os.path.join(phase5, "pr-details-reviewed.json")
merged_path = os.path.join(phase5, "pr-details.json")
authored = json.load(open(authored_path)) if os.path.exists(authored_path) else []
reviewed = json.load(open(reviewed_path)) if os.path.exists(reviewed_path) else []
json.dump(authored + reviewed, open(merged_path, "w"), indent=2)
print(f"Merged {len(authored)} authored + {len(reviewed)} reviewed")
PY
```

Before writing the final narrative, surface data quality warnings such as:

- zero genuine reviews when there were review requests
- zero authored PRs for a long period that should have activity
- zero Slack results without an auth failure, which may indicate a display-name mismatch

## Step 5: Write the Narrative Summary

Separate:

- **Authored PRs** - work shipped, scope, scale, and business/technical impact
- **Reviewed PRs** - mentoring, architecture feedback, and collaboration
- **Issues** - execution, support, incidents, and coordination
- **Recognition** - kudos and influence from Discussions and optional Slack follow-up

Focus on meaningful accomplishments, not just counts.

Write a final summary to:

```bash
SUMMARY_PATH="$WORK_DIR/contributions-summary.md"
```

Use headings like:

- `Major accomplishments`
- `Code review and technical leadership`
- `Operational / support work`
- `Recognition and cross-team impact`

## Output Format

Use a concise but evidence-backed summary. Example:

```markdown
# Contributions Summary: Q1 2026

## Major accomplishments
- Led the rollout of ...
- Shipped reliability improvements across ...

## Code review and technical leadership
- Reviewed high-impact changes in ...

## Recognition and cross-team impact
- Received kudos from ...
```

## Error Handling

### GitHub token or scope problems

- Symptom: GraphQL 401/403, zero review data, or repeated REST failures
- Fix: re-run `gh auth status`, refresh auth, and confirm the token can read PR reviews and discussions

### Search result truncation

- Symptom: exactly 200 results in a broad query
- Fix: split the date range and deduplicate by `repo + number`

### Slack display-name mismatch

- Symptom: self-messages appear in kudos output or Slack results are unexpectedly empty
- Fix: ask whether Slack display name differs from GitHub handle and pass `--slack-user`

### Slack auth failure

- Symptom: Slack helper cannot authenticate with browser cookies
- Fix: tell the user Slack data was skipped and continue with GitHub-only synthesis

## Boundaries

**Will:**

- Build summaries from GitHub activity and optional Slack signals
- Distinguish authored work from review work
- Continue gracefully without Slack when needed
- Use the bundled scripts instead of re-implementing fetch logic ad hoc

**Will Not:**

- Read Slack without a privacy warning and user confirmation
- Treat raw counts as the final deliverable
- Hide data-quality problems that could skew the summary
- Add unapproved Slack automation dependencies to the packaged skill

## Validation Checklist

- [ ] Date range normalized correctly
- [ ] GitHub org confirmed
- [ ] Slack approval captured before Slack access
- [ ] Helper scripts executed from installed skill directory
- [ ] `pr-details.json` merged before synthesis
- [ ] Final summary focuses on impact, collaboration, and recognition
- [ ] Slack omission or data-quality caveats called out when relevant

## References

- For phase-by-phase details, see `references/workflow.md`
- For helper script I/O and expectations, see `references/script-reference.md`
