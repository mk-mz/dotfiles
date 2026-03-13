# Example: Quarterly Summary with Custom Slack Display Name

## Scenario

Your GitHub handle is `alexr`, but Slack shows you as `Alex R.` in a workspace that does not share the same domain as the GitHub org.

## User Request

> Generate a quarterly accomplishments summary. My Slack display name is `Alex R.` and I want Slack kudos included if auth works.

## Agent Response

```text
⚠️ Slack data may contain private or sensitive information. I can continue with GitHub-only data, or include Slack if you want and have permission to use it.

Thanks — if approved Slack tooling is available in this environment, I’ll include Slack and use:
- GH_USER=alexr
- SLACK_TEAM=octo-eng
- SLACK_USER=Alex R.

If approved Slack tooling is unavailable or auth fails, I’ll continue with GitHub-only data and call that out in the summary.
```

## Expected Outcome

- Slack self-messages are filtered correctly via `--slack-user`
- Slack auth failure does not block the overall workflow
- The final summary includes recognition from both GitHub Discussions and Slack when available
