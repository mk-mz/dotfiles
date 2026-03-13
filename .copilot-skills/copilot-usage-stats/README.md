# Copilot Usage Stats Skill 📊

Generate AI usage metrics from your Copilot CLI session history. Produces two standardized tables — **Summary Totals** and **Artifacts Produced** — covering a configurable time window.

## Trigger Phrases

- "usage stats"
- "AI metrics"
- "session metrics"
- "copilot stats"
- "how much AI have I used"
- "generate metrics"

## Installation

```bash
# Via gh-hubber-skills
gh hubber-skills install copilot-usage-stats

# Or manually
cp -r copilot-usage-stats ~/.copilot/skills/
```

## Prerequisites

- Copilot CLI with session history (`session_store` database)
- SQL tool access for querying session data

## Features

- **Configurable time window** — default 7 days, supports "last 30 days", "this month", etc.
- **10 parallel SQL queries** for fast collection
- **Two clean tables** — Summary Totals and Artifacts Produced
- **Per-day averages** for sessions and PRs
- **Agent & skill tracking** — counts distinct custom agents and skills used
- **Cross-repo visibility** — counts unique repositories worked across

## Metrics Collected

| Category | Metrics |
|----------|---------|
| **Activity** | Sessions, conversation turns, sessions/day |
| **Artifacts** | PRs, issues, commits, files created, files edited |
| **Tooling** | Custom agents used, custom skills invoked |
| **Scope** | Unique repos worked across, unique files touched |

## Example Output

```markdown
## 📊 AI Usage Metrics (last 7 days)

### Summary Totals

| Metric | Count |
|--------|-------|
| **Copilot Sessions** | 23 (~3.3/day) |
| **Conversation Turns** | 347 |
| **Custom Agents Used** | 5 |
| **Custom Skills Used** | 8 |
| **Repositories Worked** | 4 |

### Artifacts Produced

| Artifact | Count |
|----------|-------|
| **Pull Requests** | 12 (~1.7/day) |
| **Issues Updated** | 31 |
| **Commits** | 28 |
| **Unique Files Touched** | 47 |
| **Files Created** | 15 |
| **Files Edited** | 32 |
```

## How It Works

The skill runs 10 SQL queries in parallel against the `session_store` database (read-only). It counts sessions, turns, refs (PRs/issues/commits), file operations, and pattern-matches agent/skill names in conversation text. Results are formatted into two markdown tables.

## Integration

This skill is designed to be invoked by other skills/agents:
- **snippet-builder** — includes metrics in weekly accomplishment summaries
- **daily-review** — morning briefing includes yesterday's stats
- Standalone — run anytime to check your AI usage

## Boundaries

**Will:** Query session history, format tables, accept custom time windows

**Will Not:** Modify data, query external APIs, include PII
