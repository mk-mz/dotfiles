---
name: copilot-usage-stats
description: >
  Generate AI usage metrics from Copilot CLI session history. Produces Summary Totals and Artifacts Produced tables
  covering sessions, PRs, issues, commits, files, agents, and skills. Use this skill when the user asks for
  "usage stats", "AI metrics", "session metrics", "copilot stats", "how much AI have I used", or "generate metrics".
---

# Usage Stats Skill

Generate AI usage metrics from the Copilot CLI `session_store` database. Produces two standardized tables — **Summary Totals** and **Artifacts Produced** — covering a configurable time window (default: 7 days).

## Input

- **days** (optional): Number of days to look back. Default is `7`. The user may say "last 30 days", "last 2 weeks" (14 days), "this month" (30 days), etc. Parse accordingly.

## Steps

### Step 1: Determine Time Window

Parse the user's input for a day count. If not specified, use `7`.

Calculate the ISO 8601 cutoff date:
```
cutoff = date('now', '-<days> days')
```

### Step 2: Reindex — Gather Raw Metrics

Run ALL of the following SQL queries against `database: "session_store"` in **parallel**:

**Query 1 — Session count:**
```sql
SELECT COUNT(*) as total_sessions FROM sessions WHERE created_at >= date('now', '-<days> days')
```

**Query 2 — Conversation turns:**
```sql
SELECT COUNT(*) as total_turns FROM turns t JOIN sessions s ON t.session_id = s.id WHERE s.created_at >= date('now', '-<days> days')
```

**Query 3 — PRs created:**
```sql
SELECT COUNT(DISTINCT sr.ref_value) as pr_count FROM session_refs sr JOIN sessions s ON sr.session_id = s.id WHERE sr.ref_type = 'pr' AND s.created_at >= date('now', '-<days> days')
```

**Query 4 — Issues referenced:**
```sql
SELECT COUNT(DISTINCT sr.ref_value) as issue_count FROM session_refs sr JOIN sessions s ON sr.session_id = s.id WHERE sr.ref_type = 'issue' AND s.created_at >= date('now', '-<days> days')
```

**Query 5 — Commits made:**
```sql
SELECT COUNT(DISTINCT sr.ref_value) as commit_count FROM session_refs sr JOIN sessions s ON sr.session_id = s.id WHERE sr.ref_type = 'commit' AND s.created_at >= date('now', '-<days> days')
```

**Query 6 — Files created/edited:**
```sql
SELECT tool_name, COUNT(*) as count FROM session_files sf JOIN sessions s ON sf.session_id = s.id WHERE s.created_at >= date('now', '-<days> days') GROUP BY tool_name
```

**Query 7 — Unique files touched:**
```sql
SELECT COUNT(DISTINCT file_path) as unique_files FROM session_files sf JOIN sessions s ON sf.session_id = s.id WHERE s.created_at >= date('now', '-<days> days')
```

**Query 8 — Repos worked across:**
```sql
SELECT COUNT(DISTINCT repository) as repo_count FROM sessions WHERE repository IS NOT NULL AND repository != '' AND created_at >= date('now', '-<days> days')
```

**Query 9 — Custom agents referenced (count distinct agent names):**
```sql
SELECT COUNT(DISTINCT agent_name) as agent_count FROM (
  SELECT 'fundamental-builder' as agent_name, session_id FROM turns WHERE (assistant_response LIKE '%fundamental-builder%' OR user_message LIKE '%fundamental builder%') UNION ALL
  SELECT 'fundamental-investigator', session_id FROM turns WHERE (assistant_response LIKE '%fundamental-investigator%' OR user_message LIKE '%fundamental investigator%') UNION ALL
  SELECT 'oncall-orchestrator', session_id FROM turns WHERE (assistant_response LIKE '%oncall-orchestrator%' OR user_message LIKE '%oncall orchestrator%') UNION ALL
  SELECT 'create-finding-issue', session_id FROM turns WHERE (assistant_response LIKE '%create-finding-issue%' OR user_message LIKE '%create finding issue%') UNION ALL
  SELECT 'copilot-builder', session_id FROM turns WHERE (assistant_response LIKE '%copilot-builder%' OR user_message LIKE '%copilot builder%') UNION ALL
  SELECT 'documentation', session_id FROM turns WHERE assistant_response LIKE '%documentation agent%' UNION ALL
  SELECT 'okr-updater', session_id FROM turns WHERE (assistant_response LIKE '%okr-updater%' OR user_message LIKE '%okr%updater%') UNION ALL
  SELECT 'snippet-builder', session_id FROM turns WHERE (assistant_response LIKE '%snippet-builder%' OR user_message LIKE '%snippet%builder%')
) sub
JOIN sessions s ON sub.session_id = s.id
WHERE s.created_at >= date('now', '-<days> days')
```

**Query 10 — Custom skills referenced (count distinct skill names):**
```sql
SELECT COUNT(DISTINCT skill_name) as skill_count FROM (
  SELECT 'write-adr' as skill_name, session_id FROM turns WHERE assistant_response LIKE '%write-adr%' AND assistant_response LIKE '%skill%' UNION ALL
  SELECT 'investigate-finding', session_id FROM turns WHERE assistant_response LIKE '%investigate-finding%' AND assistant_response LIKE '%skill%' UNION ALL
  SELECT 'investigate-resource', session_id FROM turns WHERE assistant_response LIKE '%investigate-resource%' AND assistant_response LIKE '%skill%' UNION ALL
  SELECT 'finding-review', session_id FROM turns WHERE assistant_response LIKE '%finding-review%' AND assistant_response LIKE '%skill%' UNION ALL
  SELECT 'wiz-finding-builder', session_id FROM turns WHERE assistant_response LIKE '%wiz-finding-builder%' AND assistant_response LIKE '%skill%' UNION ALL
  SELECT 'import-wiz', session_id FROM turns WHERE assistant_response LIKE '%import-wiz%' AND assistant_response LIKE '%skill%' UNION ALL
  SELECT 'custom-ccr-creator', session_id FROM turns WHERE assistant_response LIKE '%custom-ccr-creator%' AND assistant_response LIKE '%skill%' UNION ALL
  SELECT 'custom-graph-creator', session_id FROM turns WHERE assistant_response LIKE '%custom-graph-creator%' AND assistant_response LIKE '%skill%' UNION ALL
  SELECT 'wizcli-scanner', session_id FROM turns WHERE assistant_response LIKE '%wizcli-scanner%' AND assistant_response LIKE '%skill%' UNION ALL
  SELECT 'oncall-handoff-review', session_id FROM turns WHERE assistant_response LIKE '%oncall-handoff%' AND assistant_response LIKE '%skill%' UNION ALL
  SELECT 'oncall-sla-monitoring', session_id FROM turns WHERE assistant_response LIKE '%oncall-sla%' AND assistant_response LIKE '%skill%' UNION ALL
  SELECT 'oncall-security-exception', session_id FROM turns WHERE assistant_response LIKE '%oncall-security-exception%' AND assistant_response LIKE '%skill%' UNION ALL
  SELECT 'oncall-update-atb', session_id FROM turns WHERE assistant_response LIKE '%oncall-update-atb%' AND assistant_response LIKE '%skill%' UNION ALL
  SELECT 'oncall-wiz-connector', session_id FROM turns WHERE assistant_response LIKE '%oncall-wiz-connector%' AND assistant_response LIKE '%skill%' UNION ALL
  SELECT 'secure-infrastructure', session_id FROM turns WHERE assistant_response LIKE '%secure-infrastructure%' AND assistant_response LIKE '%skill%' UNION ALL
  SELECT 'vulnerable-infrastructure', session_id FROM turns WHERE assistant_response LIKE '%vulnerable-infrastructure%' AND assistant_response LIKE '%skill%' UNION ALL
  SELECT 'mcp-setup-assistant', session_id FROM turns WHERE assistant_response LIKE '%mcp-setup%' AND assistant_response LIKE '%skill%' UNION ALL
  SELECT 'copilot-agent-assignment', session_id FROM turns WHERE assistant_response LIKE '%copilot-agent-assignment%' AND assistant_response LIKE '%skill%'
) sub
JOIN sessions s ON sub.session_id = s.id
WHERE s.created_at >= date('now', '-<days> days')
```

### Step 3: Compute Derived Metrics

From the raw data, calculate:
- **Sessions per day** = total_sessions / days (round to 1 decimal)
- **PRs per day** = pr_count / days (round to 1 decimal)
- **Files created** = count from Query 6 where tool_name = 'create'
- **Files edited** = count from Query 6 where tool_name = 'edit'

### Step 4: Format Output

Produce exactly two markdown tables with a header showing the time window.

**Output format:**

```markdown
## 📊 AI Usage Metrics (last <days> days)

### Summary Totals

| Metric | Count |
|--------|-------|
| **Copilot Sessions** | <total_sessions> (~<per_day>/day) |
| **Conversation Turns** | <total_turns> |
| **Custom Agents Used** | <agent_count> |
| **Custom Skills Used** | <skill_count> |
| **Repositories Worked** | <repo_count> |

### Artifacts Produced

| Artifact | Count |
|----------|-------|
| **Pull Requests** | <pr_count> (~<pr_per_day>/day) |
| **Issues Updated** | <issue_count> |
| **Commits** | <commit_count> |
| **Unique Files Touched** | <unique_files> |
| **Files Created** | <files_created> |
| **Files Edited** | <files_edited> |
```

### Step 5: Return Results

Return ONLY the formatted markdown tables. Do not add commentary unless the user asks questions about the data.

## Error Handling

- If `session_store` queries return 0 for everything, note "No session data found for the last <days> days" and suggest expanding the window.
- If a single query fails, skip that metric and mark it as `N/A` in the output.
- Continue with available data — never fail the entire skill for a single query error.

## Boundaries

**Will:**
- Query session_store for historical session metrics
- Format results as two standardized markdown tables
- Accept custom time windows

**Will Not:**
- Modify any session data (read-only)
- Query external APIs or GitHub
- Include personally identifiable information beyond usernames
