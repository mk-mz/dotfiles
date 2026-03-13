# Example: Integration with Snippet Builder

Shows how usage stats appear when embedded in a weekly snippet report.

## Context

The `snippet-builder` agent invokes `copilot-usage-stats` as step 7 of its workflow, appending metrics at the end of the weekly accomplishment summary.

## Combined Output (end of snippet)

```markdown
### 🚢 Key Ships & Accomplishments

## :copilot: AI Work
- Built the <a href="https://github.com/example/repo/pull/42">terraform-preflight skill</a> to catch deployment failures before terraform apply — ⚡ prevents 403 and SKU errors that previously wasted 12+ turns per session
- Created <a href="https://github.com/example/repo/pull/45">non-implemented-findings skill</a> to track security controls GitHub doesn't enforce — 🔧 prevents re-investigating settled decisions

## 🎉 Fundamentals
- Deployed 9 FedRAMP security findings to <a href="https://github.com/example/wiz/pull/740">wiz-as-code</a> — 🛡️ covers NSG, Storage, and App Gateway controls

## 📊 Copilot CLI Metrics

### Summary Totals

| Metric | Count |
|--------|-------|
| **Copilot Sessions** | 18 (~2.6/day) |
| **Conversation Turns** | 294 |
| **Custom Agents Used** | 4 |
| **Custom Skills Used** | 7 |
| **Repositories Worked** | 5 |

### Artifacts Produced

| Artifact | Count |
|----------|-------|
| **Pull Requests** | 9 (~1.3/day) |
| **Issues Updated** | 14 |
| **Commits** | 22 |
| **Unique Files Touched** | 38 |
| **Files Created** | 11 |
| **Files Edited** | 27 |
```

## How It's Invoked

The snippet-builder agent calls this skill automatically:
1. Calculates the same 7-day window used for the snippet
2. Runs all 10 SQL queries in parallel
3. Formats the two tables
4. Appends to the end of the snippet markdown
