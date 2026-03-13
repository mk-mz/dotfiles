# Example 3: Count-Based Monitor

This example shows a simple count-based monitor that alerts when a metric exceeds a threshold.

## Monitor Configuration

```yaml
# Alert when there are more than 100 failed jobs in 5 minutes
failed-job-count:
  priority: 2
  type: metric alert
  query: sum(last_5m):sum:jobs.failed{*}.as_count() > 100
  message: |
    {{#is_alert}}
    There have been {{value}} failed jobs in the last 5 minutes (threshold: {{threshold}})!
    
    This indicates a problem with job processing. 
    
    **Next Steps:**
    1. Check the [Jobs Dashboard](https://app.datadoghq.com/dashboard/jobs)
    2. Review recent deployments
    3. Check for errors in job logs
    4. Consult the [Jobs Runbook](https://github.com/github/runbooks/jobs.md)
    {{/is_alert}}
    {{#is_alert_recovery}}
    Failed job count is back to normal levels.
    {{/is_alert_recovery}}
  require_full_window: true
  notify_no_data: false
  new_host_delay: 300
  critical: 100
```

## Key Points

- **Simple Count**: Monitors absolute count of failed jobs
- **Time Window**: 5 minute window (`last_5m`)
- **Threshold**: Alerts when more than 100 failures
- **Threshold Match**: Query uses `> 100` and `critical: 100` matches
- **Structured Response**: Message includes numbered next steps

## Common Count-Based Patterns

### Error Count
```yaml
query: sum(last_5m):sum:service.errors{*}.as_count() > 50
critical: 50
```

### Request Count (Too Low)
```yaml
query: sum(last_10m):sum:service.requests{*}.as_count() < 10
critical: 10
```

### Queue Depth
```yaml
query: avg(last_5m):avg:queue.depth{*} > 1000
critical: 1000
```

## When to Use Count vs Rate

- **Count**: Absolute numbers matter (e.g., "more than 100 errors")
- **Rate**: Percentage or ratio matters (e.g., "error rate over 5%")
- **Count**: Good for low-frequency events
- **Rate**: Good for high-volume metrics where percentage indicates health
