---
name: session-portability
description: This skill should be used when the user asks to "transfer my session", "move session to codespace", "sync session", "port session", "resume session in codespace", "copy session to codespace", "move session to local", or needs to migrate Copilot CLI session state between local and Codespace environments.
---

# Session Portability

Continue Copilot CLI work across environments (local ↔ Codespace) by generating a handoff prompt that carries context into a new session.

## Why Handoff Prompts Instead of File Transfer

`copilot --resume <uuid>` does **not** restore conversation history from a transferred `events.jsonl`. It creates a fresh session that reuses the UUID, overwriting the transferred data. See [github/copilot-cli#1635](https://github.com/github/copilot-cli/issues/1635) for the upstream feature request.

Instead, this skill captures the current session's context and generates a self-contained prompt the user can paste into a new `copilot` session in the target environment.

## When to Use

- User wants to continue a local Copilot CLI session in a Codespace (or vice versa)
- User asks about transferring, syncing, or porting session state
- User wants to resume work started in a different environment
- User wants a snapshot of current session progress to hand off

## Process

### Step 1: Gather Session Context

Collect the following from the current session:

| Context | How to Gather |
|---------|---------------|
| **Current branch** | `git branch --show-current` |
| **Recent commits** | `git --no-pager log --oneline -10` |
| **Uncommitted changes** | `git --no-pager diff --stat` |
| **Session plan** | Read `~/.copilot/session-state/<current-session-uuid>/plan.md` if it exists (the agent has access to its own session state directory) |
| **Todo status** | Use the agent's built-in SQL tool to query the session database: `SELECT id, title, status FROM todos` (this is an in-process query, not an external command) |
| **Working directory** | `pwd` and `git rev-parse --show-toplevel` |
| **Repository** | `gh repo view --json nameWithOwner -q .nameWithOwner` |
| **Modified files** | `git --no-pager diff --name-only` and `git --no-pager diff --cached --name-only` |
| **Stashed work** | `git stash list` (if any) |

### Step 2: Generate the Handoff Prompt

Assemble the gathered context into a self-contained prompt using this template:

```markdown
# Session Handoff

## Repository & Branch
- **Repo:** <owner/repo>
- **Branch:** <branch-name>
- **Last commit:** <short-sha> <commit-message>

## What Was Being Worked On
<Summary of the task, pulled from plan.md or conversation context>

## Current Progress
<List completed and in-progress items from todos or conversation>

### Completed
- <done item 1>
- <done item 2>

### In Progress
- <in-progress item — describe what's left>

### Not Started
- <pending item 1>

## Uncommitted Changes
<Output of `git diff --stat`, or "None — all changes committed">

## Key Files
<List the most important files that were created or modified>

## Next Steps
<What should be done next to continue this work>

## Notes
<Any gotchas, decisions made, or context that would be lost>
```

### Step 3: Deliver the Handoff

Present the handoff prompt to the user and explain how to use it:

1. **Push the branch** so it's available in the target environment:
   ```bash
   git push origin <branch-name>
   ```

2. **Create a conversation backup** (optional but recommended):
   ```
   Use /share to create a gist of this conversation for reference.
   ```

3. **In the target environment**, start a new `copilot` session, check out the branch, and paste the handoff prompt:
   ```bash
   cd /path/to/repo
   git checkout <branch-name>
   git pull origin <branch-name>
   copilot
   ```
   Then paste the handoff prompt into the new session.

## ⚠️ Security Considerations

### Handoff Prompt Content

The generated handoff prompt may contain:
- File paths and repository structure details
- Task descriptions that reference internal systems
- Commit messages with sensitive context

**You MUST:**
- Warn the user to review the handoff prompt before sharing it outside their own environments
- Never include secrets, tokens, or credentials in the handoff prompt
- Redact any sensitive values that appeared in conversation context
- If the user wants to share the prompt (e.g., via gist), remind them to review for sensitive content first

### `/share` and Gist Privacy

When recommending `/share` for a conversation backup:
- Gists created by `/share` are **secret** (unlisted) by default, but anyone with the URL can view them
- Remind the user that secret gists are not truly private
- For sensitive work, suggest the user review and delete the gist after the handoff is complete

## Troubleshooting

### Branch Not Available in Target Environment

**Problem:** The branch doesn't exist in the target Codespace or local clone.

```bash
# Make sure the branch is pushed
git push origin <branch-name>

# In the target environment
git fetch origin
git checkout <branch-name>
```

### Uncommitted Changes Won't Transfer

**Problem:** There are local changes that aren't committed.

Options:
1. **Commit the work-in-progress:**
   ```bash
   git add -A && git commit -m "WIP: <description>"
   git push origin <branch-name>
   ```
2. **Create a patch file and transfer it:**
   ```bash
   git diff > /tmp/session-changes.patch
   # Transfer via gist or gh cs cp
   ```

### Missing Context After Handoff

**Problem:** The new session doesn't have enough context.

The handoff prompt is a best-effort summary. To preserve full conversation history, use `/share` before switching environments. The gist URL can be included in the handoff prompt for the agent to reference.

### SQL Database State Not Transferred

**Problem:** Todo items and session database state are lost.

The handoff prompt includes todo status as plain text. In the new session, recreate the SQL state:
```sql
INSERT INTO todos (id, title, status) VALUES
  ('task-1', 'Description of task', 'done'),
  ('task-2', 'Description of next task', 'in_progress');
```

## Boundaries

**This skill WILL:**
- Gather current session context (branch, plan, progress, changes)
- Generate a self-contained handoff prompt for the target environment
- Guide the user through pushing branches and starting a new session
- Recommend `/share` for full conversation backup

**This skill will NOT:**
- Transfer session files between environments (this approach doesn't work — see above)
- Use `copilot --resume` (it overwrites transferred session data)
- Sync sessions automatically or continuously
- Manage Codespace creation or configuration
- Transfer the entire `~/.copilot/` directory
