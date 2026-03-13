# Example: Custom Time Window

Shows how to request metrics for a custom time period.

## User

> how much AI have I used this month?

## Agent Response

The skill parses "this month" as 30 days.

```markdown
## 📊 AI Usage Metrics (last 30 days)

### Summary Totals

| Metric | Count |
|--------|-------|
| **Copilot Sessions** | 154 (~5.1/day) |
| **Conversation Turns** | 2,847 |
| **Custom Agents Used** | 8 |
| **Custom Skills Used** | 14 |
| **Repositories Worked** | 11 |

### Artifacts Produced

| Artifact | Count |
|----------|-------|
| **Pull Requests** | 106 (~3.5/day) |
| **Issues Updated** | 217 |
| **Commits** | 184 |
| **Unique Files Touched** | 312 |
| **Files Created** | 89 |
| **Files Edited** | 223 |
```

## Supported Time Phrases

| User Says | Parsed As |
|-----------|-----------|
| "last 7 days" | 7 days |
| "last 2 weeks" | 14 days |
| "this month" | 30 days |
| "last 30 days" | 30 days |
| "last quarter" | 90 days |
| (no input) | 7 days (default) |
