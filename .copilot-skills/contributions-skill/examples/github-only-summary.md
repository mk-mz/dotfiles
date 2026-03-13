# Example: GitHub-Only Quarterly Summary

## Scenario

You want a Q1 summary for review prep, but you do not want Slack included.

## User Request

> Summarize my contributions for Q1 2026 in the `github` org. Skip Slack and focus on impact, reviews, and recognition from GitHub.

## Agent Response

```text
I’ll normalize the date range, collect GitHub PR, issue, and Discussion data, and skip Slack entirely.

Resolved:
- START_DATE=2026-01-01
- END_DATE=2026-03-31
- GH_ORG=github

Running GitHub collection scripts from the installed contributions-skill directory...
```

## Expected Outcome

- Authored PRs are separated from reviewed PRs
- Issue involvement is included
- GitHub Discussions kudos and authored discussions are summarized
- The final summary is written to `contributions-summary.md` with GitHub-only caveats noted
