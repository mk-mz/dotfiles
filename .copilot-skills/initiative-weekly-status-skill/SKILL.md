---
name: initiative-weekly-status
description: >
  This skill should be used when the user asks to "generate a weekly report",
  "write a status update", "summarize an initiative", "catch me up on progress",
  "what happened this week", or needs an aggregated summary of GitHub issue and
  PR activity for a product initiative. It is designed for product managers and
  stakeholders who need high-level overviews without deep technical details.
tools:
  - read
  - search
  - agent
  - runInTerminal
  - terminalLastCommand
  - terminalSelection
  - github/actions_get
  - github/actions_list
  - github/get_copilot_job_status
  - github/get_discussion
  - github/get_discussion_comments
  - github/get_file_contents
  - github/get_job_logs
  - github/get_label
  - github/get_latest_release
  - github/get_me
  - github/get_team_members
  - github/get_teams
  - github/issue_read
  - github/list_branches
  - github/list_commits
  - github/list_discussion_categories
  - github/list_discussions
  - github/list_issue_types
  - github/list_issues
  - github/list_pull_requests
  - github/list_releases
  - github/list_tags
  - github/pull_request_read
  - github/search_code
  - github/search_issues
  - github/search_pull_requests
  - github/search_repositories
  - github/search_users
  - github/dismiss_notification
  - github/get_notification_details
  - github/list_notifications
  - github/mark_all_notifications_read
  - todo
agents:
  - kusto-analytics
handoffs:
  - label: 📊 Pull Weekly Metrics
    agent: kusto-analytics
    prompt: "weekly report"
    send: false
  - label: 📊 Pull ETv2 Metrics
    agent: kusto-analytics
    prompt: "initiative: etv2"
    send: false
  - label: 📊 Pull Copilot Standalone Metrics
    agent: kusto-analytics
    prompt: "initiative: copilot-standalone"
    send: false
---

# Reporting Skill

Generate weekly summaries and progress updates for GitHub initiatives by aggregating information from epic sub-issues and related pull requests.

## When to Use

✅ **Good triggers for this skill:**
- "Generate a weekly report for [initiative]"
- "Write a status update for [issue URL]"
- "Catch me up on [initiative] since [date]"
- "Summarize progress on [epic]"
- "What happened this week on [project]?"

❌ **Not a good fit — use other tools instead:**
- Querying raw Kusto metrics without a report (→ use `kusto-analytics` directly)
- Creating or editing GitHub issues/PRs (→ use standard GitHub tools)
- Deep technical code review (→ use code review tools)

## Prerequisites

Before generating a report, verify you have:

1. **Initiative issue URL or issue number + repository** — ask the user if not provided
2. **Access to the repository** — confirm via:
   ```bash
   gh repo view OWNER/REPO --json name -q .name
   ```
3. **kusto-analytics subagent available** — required for the 📊 Metrics & Insights section

## Workflow

Follow these steps in order for every report:

### Step 1: Identify the Initiative

Ask the user for the initiative issue URL or issue number + repository. Validate it exists:

```bash
gh issue view 123 -R OWNER/REPO --json number,title,state
```

Expected output:
```json
{"number": 123, "title": "Initiative: Feature X", "state": "OPEN"}
```

If the issue is not found:
```
❌ Issue #123 not found in OWNER/REPO
Available open issues:
```
```bash
gh issue list -R OWNER/REPO --label "initiative" --limit 5
```

### Step 2: Read the Main Issue

Read the main issue body to understand scope, goals, and linked work:

```bash
gh issue view 123 -R OWNER/REPO --json body,title,labels,milestone,assignees
```

### Step 3: Gather Sub-Issues and Related Work

Identify epic sub-issues and related issues from:
- Sub-issues (use `issue_read` with `get_sub_issues`)
- Issue body (linked issues, task lists)
- Issue comments (cross-references)
- Labels (e.g., `epic`, `initiative`)

Use the `issue_read` tool with `get_sub_issues` method to traverse the issue hierarchy. Then recursively read each sub-issue to discover further nested work.

⚠️ **Do NOT use the `linked:` search qualifier** (e.g., `gh issue list --search "linked:123"`). The GitHub Search API only supports `linked:` for PR-to-issue links, not issue-to-issue links, and will return a 422 error.

### Step 4: Collect Recent PR Activity

Find all PRs linked to the initiative and sub-issues:

```bash
# Search PRs that reference the initiative
gh pr list -R OWNER/REPO --search "123" --state all --json number,title,state,mergedAt,url
```

For each relevant PR:
1. Check PR status (open, merged, closed)
2. Read PR descriptions and review comments for context
3. **Translate technical changes into business impact:**

   ❌ "Refactored authentication middleware to use JWT tokens"
   ✅ "Improved login security and performance"

   ❌ "Added GraphQL resolver for nested team queries"
   ✅ "Teams API now supports fetching member details in a single request"

### Step 5: Pull Live Metrics (Required)

⚠️ **This step is NOT optional for weekly reports.**

**Priority 1 — Delegate to kusto-analytics subagent:**

Run the kusto-analytics custom agent as a subagent with an explicit, complete prompt:

```
"Run the weekly report for all initiatives with week-over-week comparison"
```

```
"Run initiative: etv2 — pull all ETv2 metrics with comparisons to last week"
```

```
"Run initiative: copilot-standalone — pull Copilot Standalone metrics"
```

Incorporate the returned metrics directly into the 📊 Metrics & Insights section.

**Priority 2 — Direct query fallback:**

If the subagent fails:
1. Read `initiative-weekly-status-skill/kusto-analytics.agent.md` for query templates
2. Execute queries directly via terminal using the `az rest` method documented there
3. If both fail, state what was attempted in the 📊 section and suggest the user try the handoff buttons

### Step 6: Synthesize the Report

Combine all gathered information into the output format below.

## Output Format

Always wrap the final output in a markdown code block so it is copy-paste friendly.

```markdown
Status: [On Track | At Risk | Off Track] 🟢🟡🔴

Target Date: [Date]

### ✅ Progress Summary
[Concise bulleted summary of progress made in the last week. Each bullet starts with a **Bolded Header:** followed by a complete sentence describing the update. Answer: "What moved forward? What decisions were made? What milestones were completed?"]

- **Header:** Complete sentence describing the progress.

### ⚠️ Blockers
[Concise summary of any blockers or challenges and their impact. If none, state "None".]

### 🎯 Next
[Concise bulleted summary of planned work for the next week. Each bullet starts with a **Bolded Header:** followed by a complete sentence. Answer: "What is planned next? Timeframe: until next report."]

- **Header:** Complete sentence describing the planned work.

### 🔥 Demos
[Links to demos or prototypes in hyperlink markdown format with descriptive text. If none, state "None".]

- [Descriptive text](URL)

### 📊 Metrics & Insights
[**Required.** Adoption numbers, week-over-week comparisons, and key data points from kusto-analytics. Answer: "What did you learn?" Include links to dashboards and docs.]
```

### Example: Full Weekly Report Output

User: "Generate a weekly report for github/features#456"

Agent produces:

````markdown
Status: On Track 🟢

Target Date: 2026-03-15

### ✅ Progress Summary
- **OAuth Integration:** Users can now sign in with their company accounts, completing the SSO milestone ahead of schedule.
- **Performance Optimization:** Dashboard load times reduced by 40% after caching improvements merged in [#789](https://github.com/github/features/pull/789).
- **Design Review:** Finalized the updated onboarding flow based on feedback from user research sessions.

### ⚠️ Blockers
- **API Rate Limiting:** Downstream API provider changed rate limits without notice, requiring rework of the batch sync logic. ETA for resolution: 2 days. Tracked in [#501](https://github.com/github/features/issues/501).

### 🎯 Next
- **Beta Launch Prep:** Finalize rollout plan and feature flags for limited beta starting Feb 20.
- **Documentation:** Publish user-facing docs and migration guide for existing customers.

### 🔥 Demos
- [SSO Login Flow Demo](https://github.com/github/features/discussions/320)

### 📊 Metrics & Insights
- **Weekly Active Users:** 12,340 (+8% WoW)
- **Adoption Rate:** 34% of eligible orgs have enabled the feature
- **Error Rate:** 0.3% (down from 1.1% last week)
- [Dashboard](https://metrics.internal/features-456)
````

## Boundaries

**Will:**
- Generate structured weekly status reports from GitHub issue and PR activity
- Translate technical PR changes into business-impact language
- Pull live metrics via the kusto-analytics subagent
- Include clickable issue/PR links in all outputs
- Report only on changes since a specified date for catch-up requests

**Will Not:**
- Create, edit, or close GitHub issues or PRs
- Make deployment or release decisions
- Access systems outside GitHub and the kusto-analytics subagent
- Generate reports without attempting to pull live metrics first
- Fabricate metrics or status — if data is unavailable, state that clearly

## Error Handling

### Initiative issue not found

```
❌ Issue #123 not found in OWNER/REPO.
Here are recent open issues labeled "initiative":
```
Then run: `gh issue list -R OWNER/REPO --label "initiative" --limit 5`

### No linked PRs or sub-issues found

```
⚠️ No linked PRs or sub-issues found for #123.
This could mean:
  • Work hasn't started yet
  • Issues/PRs aren't cross-referenced properly
Would you like me to search more broadly by label or keyword?
```

### kusto-analytics subagent fails

```
⚠️ Could not retrieve metrics via kusto-analytics subagent.
Attempting direct query fallback...
```

If fallback also fails:

```
❌ Metrics unavailable. Attempted:
  1. kusto-analytics subagent delegation
  2. Direct az rest query fallback
Please try the 📊 handoff buttons to query metrics manually.
```

### Repository access denied

```
❌ Cannot access OWNER/REPO. Check that:
  • The repository exists
  • You have read access
  • gh auth status shows a valid session
```

## Style Guidelines

- **Direct and actionable** — no filler, no jargon
- **Complete sentences** — every bullet is a full thought
- **Impact over implementation** — translate code changes to business outcomes
- **Clickable links** — always include issue/PR URLs
- **Copy-paste ready** — wrap final output in a markdown code block
- **Catch-up scoping** — for catch-up requests, only report changes since the specified date
