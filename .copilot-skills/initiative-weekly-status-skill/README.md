# Initiative Weekly Status Skill

Generate structured weekly status reports for GitHub initiatives by aggregating sub-issue activity, pull request progress, and live Kusto metrics into a copy-paste-ready summary for stakeholders.

## When to Use This Skill

- Generating a weekly status report for a product initiative
- Summarizing progress across an epic's sub-issues and linked PRs
- Catching up on initiative activity since a specific date
- Pulling live adoption metrics with week-over-week comparisons
- Writing stakeholder-ready updates that translate technical changes into business impact

## Prerequisites

- GitHub CLI (`gh`) installed and authenticated
- Access to the target repository's issues and PRs
- For metrics: Azure CLI (`az login`) with access to the GitHub Analytics Kusto cluster

## Installation

### Using gh-hubber-skills (Recommended)

```bash
# Install the extension
gh extension install github/gh-hubber-skills

# Install the skill
gh hubber-skills install initiative-weekly-status-skill
```

### Manual Installation

**Personal Skills**
```bash
cp -r initiative-weekly-status-skill ~/.copilot/skills/
```

**Project Skills**
```bash
cp -r initiative-weekly-status-skill /path/to/repo/.github/skills/
```

## Usage

This skill activates when you ask Copilot to:
- "Generate a weekly report for github/repo#123"
- "Write a status update for this initiative"
- "Catch me up on progress since last Monday"
- "Summarize what happened this week on the ETv2 initiative"
- "What's the current status of this epic?"

The skill will:
1. Read the initiative issue and identify sub-issues and linked PRs
2. Collect recent activity across all related work items
3. Translate technical PR changes into business-impact language
4. Pull live metrics from Kusto with week-over-week comparisons
5. Produce a structured, copy-paste-ready status report

## Features

- **Structured output** — Consistent format with Progress, Blockers, Next, Demos, and Metrics sections
- **PR translation** — Converts technical changes to stakeholder-friendly language
- **Live metrics** — Pulls adoption data from Kusto via the kusto-analytics subagent
- **Week-over-week comparisons** — Automatic delta calculations with absolute and percentage changes
- **Copy-paste ready** — Output wrapped in markdown code blocks for direct use

## Supporting Files

This skill includes supporting agent and prompt configuration files for VS Code Copilot:

| File | Purpose |
|------|---------|
| `reporting.agent.md` | Core reporting agent with Kusto integration and output format |
| `kusto-analytics.agent.md` | Subagent for querying GitHub Analytics Kusto cluster |
| `github-task-assistant.agent.md` | Agent for tracking and managing GitHub engineering tasks |
| `github-catchup.prompt.md` | Prompt for catching up on GitHub notifications and tasks |
| `initiative-weekly-status.prompt.md` | Prompt for triggering a weekly status report |

## Examples

### Generate a weekly report
```
User: "Generate a weekly report for github/meao#456"
Agent: Reads the initiative, gathers sub-issue and PR activity, pulls Kusto
       metrics, and produces a structured status report with progress,
       blockers, next steps, and adoption numbers.
```

### Catch up on progress
```
User: "Catch me up on the ETv2 initiative since last Monday"
Agent: Scopes activity to the last week, summarizes completed work,
       highlights any new blockers, and shows metric trends.
```

### Status with metrics
```
User: "What's the current status of Enterprise Teams v2?"
Agent: Pulls live customer adoption counts, Copilot license assignments,
       IdP sync percentages, and org role stats with week-over-week deltas.
```

## Tips

- Provide the initiative issue URL or number + repo for best results
- The skill automatically pulls metrics — no need to ask separately
- For catch-up requests, specify a date to scope the activity window
- Output is formatted for direct paste into tracking issues or Slack

---

**Required:** GitHub CLI (`gh`) with repository access. For metrics: Azure CLI (`az`) with Kusto cluster access.
