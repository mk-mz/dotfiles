---
name: assign-issue-to-copilot
description: This skill should be used when the user asks to "assign Copilot to this issue", "have Copilot work on issue", "give this to Copilot", "let Copilot handle this", "assign the coding agent", "write an issue for Copilot", or needs to delegate GitHub issues to the Copilot coding agent.
---

# Assign Issue to Copilot - Delegate Work to the Coding Agent

Teaches agents how to assign GitHub issues to Copilot (the coding agent) and write issues that Copilot can work from effectively.

## When to Use This Skill

- User wants to delegate an issue to Copilot for implementation
- Need to assign Copilot to one or multiple issues
- Writing new issues that Copilot will pick up
- Checking if Copilot has started working on an assigned issue
- Monitoring Copilot's progress on an issue
- Verifying that a repository has Copilot coding agent enabled

## Core Functionality

### 1. Assign Copilot to an Issue

**The assignee username is `@copilot` (special value, not case-sensitive but conventionally lowercase)**

**Command:**
```bash
# Assign Copilot to a single issue
gh issue edit ISSUE_NUMBER --repo OWNER/REPO --add-assignee @copilot

# Assign Copilot to an issue in the current repo
gh issue edit ISSUE_NUMBER --add-assignee @copilot

# Assign yourself AND Copilot (for collaboration)
gh issue edit ISSUE_NUMBER --add-assignee @me,@copilot
```

**Expected output:**
```
✓ Edited issue #123
```

**Important notes:**
- Use `@copilot` as the assignee (with @ symbol)
- The special `@copilot` value is NOT the same as a user named "Copilot" or "copilot"
- Not supported on GitHub Enterprise Server (GHES)
- Repository must have Copilot coding agent enabled

### 2. Verify Assignment

**Check if Copilot is assigned:**
```bash
# View issue assignees
gh issue view ISSUE_NUMBER --json assignees --jq '.assignees[].login'

# Check specific issue details
gh issue view ISSUE_NUMBER --json number,title,assignees,state
```

**Expected output (if assigned):**
```json
{
  "number": 123,
  "title": "Add user authentication",
  "assignees": [
    {
      "login": "Copilot"
    }
  ],
  "state": "OPEN"
}
```

### 3. Batch Assign Copilot to Multiple Issues

**Assign to multiple issues sequentially:**
```bash
# Using a loop
for issue in 123 456 789; do
  echo "Assigning Copilot to issue #$issue..."
  gh issue edit "$issue" --add-assignee @copilot
  sleep 1  # Brief delay to avoid rate limiting
done

# Using xargs for parallel execution (be cautious with rate limits)
echo "123 456 789" | xargs -n 1 -P 3 -I {} gh issue edit {} --add-assignee @copilot
```

**Assign to all open issues with a specific label:**
```bash
# Get all issues with label "good first issue" and assign Copilot
gh issue list --label "good first issue" --state open --json number --jq '.[].number' | \
  while read -r issue; do
    echo "Assigning Copilot to issue #$issue..."
    gh issue edit "$issue" --add-assignee @copilot
  done
```

### 4. Check if Copilot Has Started Working

**Check for PRs created by Copilot for an issue:**
```bash
# Search for PRs by Copilot that reference the issue
gh pr list --author Copilot --search "issue #ISSUE_NUMBER" --json number,title,url,state

# Alternative: Search in PR bodies
gh pr list --author Copilot --state all --json number,title,body,url | \
  jq --arg issue "#ISSUE_NUMBER" '.[] | select(.body | contains($issue))'
```

**Expected output (if PR exists):**
```json
[
  {
    "number": 234,
    "title": "Fix: Add user authentication (#123)",
    "url": "https://github.com/owner/repo/pull/234",
    "state": "OPEN"
  }
]
```

**Check Copilot's progress:**
```bash
# Get PR details and check status
PR_NUM=$(gh pr list --author Copilot --search "issue #123" --json number --jq '.[0].number')

if [ -n "$PR_NUM" ]; then
  echo "✅ Copilot opened PR #$PR_NUM"
  gh pr view "$PR_NUM"
  
  # Check CI status
  gh pr checks "$PR_NUM"
else
  echo "⏳ Copilot hasn't opened a PR yet"
fi
```

### 5. Verify Repository Has Copilot Enabled

**There's no direct CLI command to check if Copilot is enabled, but you can:**

1. **Try to assign and handle errors gracefully:**
```bash
ASSIGN_ERR_OUTPUT=$(gh issue edit ISSUE_NUMBER --add-assignee @copilot 2>&1 >/dev/null)
ASSIGN_STATUS=$?

if [ $ASSIGN_STATUS -ne 0 ]; then
  if echo "$ASSIGN_ERR_OUTPUT" | grep -qi "not found"; then
    echo "❌ Copilot is not available for this repository"
    echo "The repository may not have Copilot coding agent enabled"
    echo "Contact your repository admin to enable Copilot"
  else
    echo "❌ Failed to assign Copilot:"
    echo "$ASSIGN_ERR_OUTPUT"
  fi
  exit $ASSIGN_STATUS
else
  echo "✅ Successfully assigned Copilot"
fi
```

2. **Check if Copilot has been assigned to any issues/PRs before:**
```bash
# Look for any issues assigned to Copilot
COPILOT_ISSUES=$(gh issue list --assignee Copilot --json number --jq 'length')

if [ "$COPILOT_ISSUES" -gt 0 ]; then
  echo "✅ Repository has Copilot activity ($COPILOT_ISSUES issues found)"
else
  echo "⚠️  No existing Copilot assignments found"
  echo "Repository may not have Copilot enabled, or this is the first assignment"
fi
```

## Writing Copilot-Friendly Issues

When creating issues for Copilot to pick up, follow these best practices:

### Essential Elements

**1. Clear, Specific Title**
```markdown
✅ Good: "Add rate limiting to /api/users endpoint"
❌ Bad: "Fix API issues"
```

**2. Detailed Description with Context**
```markdown
## Problem
The /api/users endpoint currently has no rate limiting, which could 
lead to abuse and performance degradation.

## Proposed Solution
Implement rate limiting using the existing RateLimiter middleware:
- Limit: 100 requests per minute per IP
- Return 429 status code when limit exceeded
- Include Retry-After header in response

## Acceptance Criteria
- [ ] Rate limiter applied to /api/users endpoint
- [ ] Tests added for rate limiting behavior
- [ ] Documentation updated with rate limit information
```

**3. Specific File Paths (When Possible)**
```markdown
## Files to Modify
- `src/api/routes/users.js` - Add rate limiter middleware
- `src/middleware/rateLimiter.js` - May need to adjust configuration
- `tests/api/users.test.js` - Add rate limiting tests
- `docs/api.md` - Document the rate limit
```

**4. Test Expectations**
```markdown
## Testing
- All existing tests should pass
- Add new test: "should return 429 when rate limit exceeded"
- Add new test: "should include Retry-After header"
```

**5. Dependencies and Prerequisites**
```markdown
## Dependencies
- Uses existing `express-rate-limit` package (already installed)
- Requires Redis for distributed rate limiting (already configured)

## Prerequisites
- None, all dependencies are already set up
```

### Issue Template for Copilot

Use this template when writing issues for Copilot:

```markdown
## Problem
[Clear description of what needs to be done and why]

## Proposed Solution
[Specific approach, including technology/libraries to use]

## Files to Modify/Create
- `path/to/file1.js` - [what needs to change]
- `path/to/file2.js` - [what needs to change]

## Acceptance Criteria
- [ ] [Specific, testable requirement]
- [ ] [Another specific requirement]
- [ ] All existing tests pass
- [ ] New tests added for new functionality

## Testing
[Describe how to test the changes, including specific test cases]

## Additional Context
[Links to related issues, documentation, or examples]
```

### Tips for Better Issues

**DO:**
- ✅ Be specific about file paths and line numbers when relevant
- ✅ Include code snippets or examples of expected behavior
- ✅ Specify the programming language and framework versions
- ✅ Mention any coding standards or conventions to follow
- ✅ Link to related issues, PRs, or documentation
- ✅ Include error messages or logs if fixing a bug
- ✅ Specify test coverage expectations

**DON'T:**
- ❌ Use vague language like "fix the thing" or "make it better"
- ❌ Combine multiple unrelated changes in one issue
- ❌ Omit acceptance criteria
- ❌ Forget to specify testing requirements
- ❌ Leave out context about why the change is needed

## Monitoring Copilot Progress

### Workflow: Assign and Monitor

```bash
# 1. Assign Copilot
echo "Assigning Copilot to issue #123..."
gh issue edit 123 --add-assignee @copilot

# 2. Wait a few minutes for Copilot to start
echo "✅ Copilot assigned. Waiting for Copilot to start working..."
echo "This typically takes 1-5 minutes."

# 3. Check for PR (poll every 30 seconds for up to 10 minutes)
for i in {1..20}; do
  sleep 30
  PR=$(gh pr list --author Copilot --search "issue #123" --json number --jq '.[0].number')
  
  if [ -n "$PR" ]; then
    echo "✅ Copilot opened PR #$PR!"
    gh pr view "$PR"
    break
  else
    echo "⏳ Still waiting for Copilot... (attempt $i/20)"
  fi
done

# 4. Monitor PR checks (if PR was created)
if [ -n "$PR" ]; then
  echo ""
  echo "Monitoring CI checks for PR #$PR..."
  gh pr checks "$PR" --watch
fi
```

### Integration with watch-ci-skill

After Copilot opens a PR, use the watch-ci-skill to monitor build status:

```bash
# Get Copilot's PR number
PR=$(gh pr list --author Copilot --search "issue #123" --json number --jq '.[0].number')

if [ -n "$PR" ]; then
  echo "Copilot opened PR #$PR. Watching CI..."
  # This would trigger the watch-ci-skill
  gh pr checks "$PR" --required --watch
fi
```

## Error Handling

### Error: Assignee Not Found

```bash
gh issue edit 123 --add-assignee @copilot
# Error: assignee not found: copilot
```

**Cause:** Using lowercase `copilot` or repository doesn't have Copilot enabled

**Solution:**
```bash
# Use @copilot (with @ symbol)
gh issue edit 123 --add-assignee @copilot

# If that fails, Copilot is not enabled for this repository
if ! gh issue edit 123 --add-assignee @copilot 2>&1; then
  echo "❌ Failed to assign Copilot"
  echo ""
  echo "Possible reasons:"
  echo "1. Repository does not have Copilot coding agent enabled"
  echo "2. You're using GitHub Enterprise Server (not supported)"
  echo "3. Organization settings prevent Copilot assignments"
  echo ""
  echo "Contact your repository administrator to enable Copilot."
fi
```

### Error: Permission Denied

```bash
# Error: Resource not accessible by integration
```

**Cause:** Insufficient permissions to edit issues

**Solution:**
```bash
# Check authentication
gh auth status

# Refresh with proper scopes
gh auth refresh -s repo

# Verify you have write access
gh repo view OWNER/REPO --json viewerPermission
```

### Error: Issue Not Found

```bash
# Error: issue #999 not found
```

**Solution:**
```bash
# Verify issue exists
if ! gh issue view 999 &>/dev/null; then
  echo "❌ Issue #999 not found"
  echo "Available open issues:"
  gh issue list --limit 10
  exit 1
fi
```

### Issue Stuck: Copilot Not Starting

**Symptoms:** Issue assigned to Copilot but no PR opened after 15+ minutes

**Troubleshooting:**
```bash
# 1. Verify assignment
gh issue view 123 --json assignees

# 2. Check if issue is well-formed
echo "Review the issue to ensure it has:"
echo "- Clear title and description"
echo "- Specific acceptance criteria"
echo "- Actionable requirements"

# 3. Check repository activity
echo "Recent Copilot activity:"
gh pr list --author Copilot --limit 5

# 4. Try unassigning and reassigning
gh issue edit 123 --remove-assignee @copilot
sleep 5
gh issue edit 123 --add-assignee @copilot

echo "If Copilot still doesn't start, the issue may need more detail"
```

## Output Formats

### Assignment Confirmation

```
🤖 Assigning Copilot to issue #123

Issue: Add user authentication
URL: https://github.com/owner/repo/issues/123

✅ Copilot assigned successfully!

Next steps:
• Copilot typically starts work within 1-5 minutes
• Check for PR: gh pr list --author Copilot --search "issue #123"
• Monitor progress: I'll check back in 2 minutes
```

### Batch Assignment Summary

```
📋 Batch assigning Copilot to 5 issues...

✅ Issue #123 - Add authentication
✅ Issue #124 - Fix login bug  
✅ Issue #125 - Update documentation
❌ Issue #126 - Failed (permission denied)
✅ Issue #127 - Add tests

Summary: 4/5 issues assigned successfully
Failed: #126 (check permissions)
```

### Progress Check

```
🔍 Checking Copilot's progress on issue #123...

Copilot Status:
✅ Assigned: Yes (2 minutes ago)
✅ PR Opened: #234
📊 CI Status: ✓ 3/3 checks passed
📝 Review Status: Awaiting review

PR Details:
Title: Fix: Add user authentication (#123)
URL: https://github.com/owner/repo/pull/234
Files changed: 4
Commits: 3

Next steps:
• Review the PR: gh pr view 234
• Approve: gh pr review 234 --approve
• Merge: gh pr merge 234 --squash
```

## Boundaries

**Will:**
- Assign Copilot to issues using the correct `@copilot` assignee
- Verify assignments and check for Copilot activity
- Monitor for PRs opened by Copilot
- Provide guidance on writing Copilot-friendly issues
- Handle batch assignments to multiple issues
- Integrate with watch-ci-skill for PR monitoring

**Will Not:**
- Work on GitHub Enterprise Server (GHES) - Copilot assignments not supported
- Enable Copilot for repositories (requires admin permissions)
- Force Copilot to start immediately (depends on Copilot's availability)
- Guarantee Copilot will work on every assigned issue
- Review or merge Copilot's PRs without user approval
- Modify issue descriptions without user confirmation

## Best Practices

1. **Always use `@copilot`** - The @ symbol and lowercase convention is important
2. **Write detailed issues** - More context = better Copilot results
3. **Include acceptance criteria** - Helps Copilot understand completion goals
4. **Specify file paths** - Guides Copilot to the right locations
5. **Add test expectations** - Ensures Copilot includes proper tests
6. **Monitor progress** - Check within 5-10 minutes to ensure Copilot started
7. **One concern per issue** - Don't combine multiple unrelated changes
8. **Link related context** - Reference docs, related issues, or examples

## Quick Reference

**Common Commands:**
```bash
# Assign Copilot to an issue
gh issue edit ISSUE_NUMBER --add-assignee @copilot

# Verify assignment
gh issue view ISSUE_NUMBER --json assignees --jq '.assignees[].login'

# Check for Copilot's PR
gh pr list --author Copilot --search "issue #ISSUE_NUMBER"

# Monitor PR checks
gh pr checks PR_NUMBER --watch

# Batch assign (issues 100-105)
for i in {100..105}; do gh issue edit $i --add-assignee @copilot; done

# Unassign Copilot
gh issue edit ISSUE_NUMBER --remove-assignee @copilot
```

**Issue Quality Checklist:**
- [ ] Clear, specific title
- [ ] Problem statement with context
- [ ] Proposed solution or approach
- [ ] Specific file paths (when applicable)
- [ ] Acceptance criteria (checkbox list)
- [ ] Testing requirements
- [ ] Links to related resources
- [ ] Coding standards or conventions noted

## Integration with Other Skills

| Skill | When to Combine |
|-------|-----------------|
| **watch-ci** | After Copilot opens a PR, use watch-ci to monitor build status |
| **github-discussions** | Discuss Copilot results or coordinate on complex issues |
| **slack-context** (with caution) | When issue context comes from Slack discussions |

## Examples

See the `examples/` directory for complete workflow scenarios:
- `assign-single-issue.md` - Basic assignment workflow
- `batch-assign.md` - Assigning Copilot to multiple issues
- `write-issue.md` - Creating a Copilot-ready issue
