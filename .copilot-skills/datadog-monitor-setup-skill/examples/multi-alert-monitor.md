# Example 2: Multi-Alert Monitor

This example shows how to create a monitor that generates separate alerts for different environments.

## Monitor Configuration

```yaml
# Alert on high error rate per environment
api-error-rate:
  priority: 1  # Priority 1 for production, but routing can differ by env
  type: metric alert
  query: |
    sum(last_5m):sum:api.errors{*} by {env}.as_count()
    / sum:api.requests{*} by {env}.as_count() * 100 > 5
  message: |
    {{#is_alert}}
    Error rate for {{env.name}} environment is over {{threshold}}%!
    
    Current error rate: {{value}}%
    
    Check the [API Dashboard](https://app.datadoghq.com/dashboard/api-overview)
    Review the [API Runbook](https://github.com/github/runbooks/api-errors.md)
    {{/is_alert}}
    {{#is_alert_recovery}}
    Error rate for {{env.name}} is back to normal.
    {{/is_alert_recovery}}
  require_full_window: false
  notify_no_data: true
  new_host_delay: 300
  critical: 5.0
```

## Key Points

- **Multi-Alert**: Uses `by {env}` to create separate alerts per environment
- **Dynamic Naming**: Use `api-error-rate-{{env.name}}` in UI to show environment
- **Priority**: Set to 1, but routing can send prod alerts to pages and test to Slack
- **Tag Variable**: `{{env.name}}` shows which environment is alerting

## Routing Configuration

With multi-alert monitors, you can configure different routing per tag:

- `my-service/api-error-rate-production` → Pages on-call
- `my-service/api-error-rate-staging` → Slack only  
- `my-service/api-error-rate-development` → No notification

Configure routing in Nines based on the full monitor name including tag value.

## When to Use Multi-Alert

- Monitoring the same metric across different dimensions
- Need different routing based on tag values
- Want consolidated monitor configuration
- Common dimensions: `env`, `host`, `region`, `cluster`
