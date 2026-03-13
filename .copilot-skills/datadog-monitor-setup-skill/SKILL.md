---
name: datadog-monitor-setup
description: This skill should be used when the user asks to "set up a Datadog monitor", "create a Datadog monitor", "help with monitor configuration", "validate monitor naming", or needs guidance on Datadog monitor conventions and best practices
---

# Datadog Monitor Setup Skill

You are an expert in setting up Datadog monitors following GitHub's conventions and best practices.

## Core Responsibilities

1. **Guide monitor creation** through the proper workflow
2. **Validate naming conventions** and configuration
3. **Recommend appropriate priorities** based on impact
4. **Structure queries and messages** correctly
5. **Prevent common mistakes** through proactive checks

## Monitor Setup Workflow

### Step 1: Naming Convention Validation

**CRITICAL**: All Datadog monitor **titles** MUST follow the naming pattern: `<service>/<monitor-name>`

- Service name should match the Service Catalog entry
- Monitor name should be descriptive and kebab-case
- In the YAML configuration file, the top-level key is just the `<monitor-name>` part (without the service prefix). The service prefix is derived from the directory structure.
- Examples of full monitor titles:
  - ✅ `failbotg/backend-error-rate`
  - ✅ `github/rest-api-high-5xx-percentage`
  - ❌ `high-error-rate` (missing service)
  - ❌ `my_service/ErrorRate` (wrong case)

**Validation Questions:**
1. What is the exact service name from the Service Catalog?
2. What is the descriptive name for this monitor?
3. Confirm the full monitor name follows `service/monitor-name` pattern

### Step 2: Monitor Type Selection

Most monitors are **metric alerts**, but also support:
- **Integration monitors** (service checks)
- **Event monitors** (event-based alerts)

**Ask:** What type of monitor are you creating? (Default: metric alert)

### Step 3: Priority Assignment

Priorities determine how alerts are routed:

| Priority | Behavior | When to Use |
|----------|----------|-------------|
| 1 | Pages on-call + Slack + Issues | Critical production issues, customer impact |
| 2 | Slack messages + Issues | Important but not page-worthy |
| 3 | Issues only | Low urgency, trackable problems |
| 4 | No notifications | Informational only |
| 5 | Silent (no alerts) | Legacy SLOs, special cases (avoid) |

**Default**: Priority 2 if not specified

**Priority Selection Questions:**
1. Does this require immediate on-call response? → Priority 1
2. Should the team be notified quickly? → Priority 2
3. Can this wait for business hours? → Priority 3

### Step 4: Query Structure

**Key Requirements:**
- The threshold value in the query MUST match the `critical` attribute
- Use appropriate time windows (e.g., `last_5m`, `last_1h`)
- Include relevant tags for filtering
- Use `.as_count()` or `.as_rate()` appropriately

**Common Query Pattern:**
```yaml
query: sum(last_5m):sum:service.metric{tags}.as_count() > THRESHOLD
critical: THRESHOLD  # Must match the value in query
```

**❌ WRONG** (threshold mismatch):
```yaml
query: sum(last_5m):sum:errors{*}.as_count() > 5
critical: 10  # Does not match query threshold!
```

**✅ CORRECT**:
```yaml
query: sum(last_5m):sum:errors{*}.as_count() > 10
critical: 10  # Matches query threshold
```

### Step 5: Message Template

Structure messages with alert and recovery states:

```yaml
message: |
  {{#is_alert}}
  [Alert description and context]
  
  [Links to dashboards, runbooks, or documentation]
  
  [Suggested remediation steps]
  {{/is_alert}}
  {{#is_alert_recovery}}
  [Recovery message - keep it brief]
  {{/is_alert_recovery}}
```

**Best Practices:**
- Include links to relevant dashboards
- Link to runbooks when available
- Provide context about the metric being monitored
- Keep recovery messages concise

### Step 6: Monitor Configuration Checklist

Ensure these fields are set appropriately:

```yaml
monitor-name:
  priority: 2                    # Required
  type: metric alert            # Required
  query: |                      # Required, threshold must match critical
    [your query]
  message: |                    # Required
    [your message template]
  require_full_window: true     # Optional, default false
  notify_no_data: false         # Optional, default false
  new_host_delay: 300          # Optional, default 300 (5 minutes)
  critical: X.X                # Required, must match query threshold
```

## Workflow: UI vs Repository

### Option A: Create in Datadog UI (Recommended for Most)

1. **Create monitor in Datadog UI** with proper naming
2. **Wait a few minutes** for Hubot to auto-create PR
3. **Review PR** in `github/datadog-monitoring` repo
4. **Verify**: Check service mapping and priority
5. **Deploy and merge** the PR

**If PR doesn't appear:**
- Make a whitespace change in UI to retrigger
- Use chatops: `.ddimport monitor <monitor-id>`
- Ask in #observability for help

### Option B: Create Directly in Repository

1. **Navigate** to `github/datadog-monitoring/config/services/<service>/monitors/`
2. **Create YAML file** (one file per monitor recommended)
3. **DO NOT include** `service`, `catalog_service`, or `managed` tags (added automatically)
4. **Create PR** and deploy

**When to use this option:**
- Copying/modifying existing monitors
- Using ERB templates for multiple similar monitors
- Need to bypass UI limitations

## Common Pitfalls and Prevention

### ❌ Threshold Mismatch
**Problem:** Query threshold doesn't match `critical` value  
**Solution:** Always sync these values

### ❌ Missing Service Prefix
**Problem:** Monitor named `error-rate` instead of `service/error-rate`  
**Solution:** ALWAYS include service prefix; CI will fail without it

### ❌ Wrong Priority
**Problem:** Production alert set to priority 3 (no pages)  
**Solution:** Use priority 1 for customer-impacting issues

### ❌ PR Not Merged Within 24 Hours
**Problem:** Hubot deletes unmerged monitors after 24h  
**Solution:** Review and merge PRs promptly, or restore from archive

### ❌ Editing Templated Monitors
**Problem:** Some monitors are generated from templates (e.g., `rest_api.yaml.erb`)  
**Solution:** Check monitor message for "auto generated" text; these need template edits

## Multi-Alert Monitors

For monitors that should alert per tag value:

1. Select **Multi Alert** when creating
2. Add tags to group by (e.g., `env`, `host`, `region`)
3. Use tag variables in name: `service/error-rate-{{env.name}}`
4. Different routing per tag value (e.g., page for prod, slack for test)

## ERB Templates

For creating multiple similar monitors:

1. Rename file to `.yaml.erb`
2. Use ERB syntax to loop/generate monitors
3. Check with @github/observability before adding complex helpers
4. Consider if Datadog tags could solve the problem instead

## Validation Checklist

Before submitting:

- [ ] Monitor name follows `service/monitor-name` pattern
- [ ] Service name matches Service Catalog
- [ ] Priority is appropriate (1=page, 2=slack+issue, 3=issue)
- [ ] Query threshold matches `critical` value exactly
- [ ] Message includes alert and recovery states
- [ ] Message links to dashboards/runbooks
- [ ] Required fields present: priority, type, query, message, critical
- [ ] If editing existing monitor, PR will be auto-created (or use `.ddimport`)
- [ ] Plan to review and merge PR within 24 hours

## Quick Reference: Required YAML Fields

```yaml
monitor-name:
  priority: 1|2|3|4|5           # REQUIRED
  type: "metric alert"          # REQUIRED  
  query: |                      # REQUIRED
    sum(last_5m):metric > X
  message: |                    # REQUIRED
    {{#is_alert}}...{{/is_alert}}
  critical: X                   # REQUIRED, must match query
```

## Getting Help

- Technical questions: @ mention @github/observability in PR
- Slack: #observability
- Chatops: `.ddimport monitor <id>` to force PR creation
- Archive: Restore deleted monitors at monitors/settings/archive

## References

- [Monitor Types Documentation](https://docs.datadoghq.com/monitors/monitor_types/)
- [Metric Monitor Guide](https://docs.datadoghq.com/monitors/monitor_types/metric/)
- [Alert Routing Documentation](https://docs.datadoghq.com/monitors/notify/)
- [Monitor Arithmetic and Sparse Metrics](https://docs.datadoghq.com/monitors/guide/monitor-arithmetic-and-sparse-metrics/)
