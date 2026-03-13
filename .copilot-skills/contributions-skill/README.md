# Contributions Skill

Generate a polished contributions summary for a review cycle, quarter, or custom date range by collecting authored PRs, meaningful reviews, issue work, GitHub Discussions recognition, and optional Slack follow-up notes.

## When to Use This Skill

- Preparing self-review or promotion evidence
- Summarizing accomplishments for a quarter, month, or YTD
- Turning raw GitHub activity into accomplishment narratives
- Collecting peer recognition from GitHub Discussions, with optional Slack follow-up if your environment has approved tooling

## ⚠️ Security Notes

This skill can read GitHub content and may optionally incorporate Slack-derived notes that contain internal details, customer references, or sensitive discussion history.

Before using Slack or non-public GitHub data:

- Review whether you have permission to process the data
- Confirm the target org and Slack workspace are correct
- Avoid sharing unredacted output outside the intended audience

Slack follow-up is optional and not bundled in this repo package. The skill should continue with GitHub-only analysis if Slack access is declined, unavailable, or lacks approved tooling.

## Prerequisites

- `gh` CLI installed and authenticated
- `python3` available for the bundled helper scripts
- Access to the target GitHub org and, optionally, the matching Slack workspace

## Installation

### Personal Skills

```bash
cp -r contributions-skill ~/.copilot/skills/
```

### Project Skills

```bash
cp -r contributions-skill /path/to/repo/.github/skills/
```

## Usage

This skill activates when you ask Copilot to:

- "Summarize my contributions for Q1 2026"
- "Write a self-review summary from my GitHub activity"
- "Generate a YTD accomplishments summary"
- "Pull together my PRs, reviews, and kudos for January"

The skill will:

1. Normalize the requested date range
2. Resolve the GitHub org and optional Slack display name
3. Collect GitHub data in parallel
4. Optionally incorporate Slack-derived notes if approved tooling is available
5. Synthesize the results into a narrative summary

## Features

- **Parallel data collection** - Separates authored PRs, reviewed PRs, Discussions, and Slack into concurrent workstreams
- **Meaningful review filtering** - Excludes boilerplate approvals so review work is represented accurately
- **Portable source helpers** - Ships Python source helpers with offline validation
- **Performance test harness** - Includes `scripts/test_performance.py` for correctness and concurrency checks
- **GitHub-first fallback** - Still useful when Slack is unavailable

## Bundled Scripts

- `scripts/fetch-details.py` - Enriches PRs and issues, caches per-item fetches, and produces detail JSON
- `scripts/filter-reviewed-prs.py` - Filters review-requested PRs down to genuine review activity
- `scripts/search-discussion-kudos.py` - Searches GitHub Discussions for kudos and authored discussions
- `scripts/test_performance.py` - Offline validation suite for the Python helpers

## Slack Follow-up

This repo package intentionally does **not** bundle an automated Slack helper because any Slack integration should use approved, policy-compliant tooling in the target environment.

Treat Slack as an optional follow-up step after the GitHub summary is assembled.

## Examples

- [GitHub-only quarterly summary](./examples/github-only-summary.md)
- [Quarterly summary with custom Slack display name](./examples/with-slack-display-name.md)

## References

- [Workflow reference](./references/workflow.md)
- [Script reference](./references/script-reference.md)
