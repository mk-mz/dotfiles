# Example 1: Basic Error Rate Monitor

This example shows a simple error rate monitor for a service that tracks backend errors.

## Monitor Configuration

```yaml
# Alert if error (non-2xx, non-413) responses from Sentry are over 1%
# of requests for 1 hour
backend-error-rate:
  priority: 2
  type: metric alert
  query: |
    sum(last_1h):sum:failbotg.responses{destination:sentry,!code:201,!code:2xx,!code:413,!code:429}.as_count()
    / sum:failbotg.responses{destination:sentry}.as_count() * 100 > 1
  message: |
    {{#is_alert}}
    Backend error rate for delivering exceptions to {{destination.name}} is over {{threshold}}%!
    This may be an issue with {{destination.name}}, but may be an issue with
    failbotg itself. Check the [Failbotg Dashboard](https://app.datadoghq.com/dashboard/q3p-2dd-s5n).
    You may find more details in the [failbotg runbook](https://github.com/github/observability/blob/master/docs/runbooks/failbotg.md).
    {{/is_alert}}
    {{#is_alert_recovery}}
    The error rate for Sentry is now ok!
    {{/is_alert_recovery}}
  require_full_window: true
  notify_no_data: false
  new_host_delay: 300
  critical: 1.0
```

## Key Points

- **Service**: `failbotg`
- **Monitor Name**: `backend-error-rate`
- **Full Name**: `failbotg/backend-error-rate`
- **Priority**: 2 (Slack + Issues, no pages)
- **Type**: Percentage calculation over 1 hour window
- **Threshold**: 1% error rate (matches `critical: 1.0`)

## What This Monitors

- Calculates percentage of error responses (non-2xx) to Sentry
- Excludes specific codes: 201, 413, 429
- Looks at 1 hour window
- Alerts when error rate exceeds 1%
- Requires full window of data before alerting

## Message Structure

- **Alert state**: Provides context, dashboard link, and runbook reference
- **Recovery state**: Simple confirmation message
- **Uses template variables**: `{{destination.name}}`, `{{threshold}}`
