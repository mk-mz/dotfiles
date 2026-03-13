# Example: Assign Copilot to a Single Issue

Complete workflow for delegating a single issue to the Copilot coding agent.

## Scenario

You have an issue that needs implementation and want to delegate it to Copilot. The issue already has a clear description and acceptance criteria.

## User Request

> "Assign Copilot to issue #456"

## Agent Response

```
🤖 Assigning Copilot to issue #456...

Issue Details:
Title: Add rate limiting to /api/users endpoint
URL: https://github.com/owner/repo/issues/456
Current Assignees: None

Running: gh issue edit 456 --add-assignee @copilot
```

## Assignment Confirmation

```
✅ Successfully assigned Copilot to issue #456!

What happens next:
• Copilot will review the issue (typically within 1-5 minutes)
• Copilot will open a PR when implementation is complete
• You'll be notified when the PR is ready for review

You can check progress with:
  gh pr list --author Copilot --search "issue #456"
```

## Checking Progress (After 2 Minutes)

**User Request:**
> "Has Copilot started on issue #456 yet?"

**Agent Response:**
```
🔍 Checking Copilot's progress on issue #456...

Running: gh pr list --author Copilot --search "issue #456" --json number,title,state

⏳ No PR found yet. Copilot is likely still analyzing the issue.

Typical timeline:
• 0-2 min: Copilot reviews the issue
• 2-10 min: Copilot implements the changes
• 10+ min: PR is opened

I'll check again in 3 minutes.
```

## PR Opened (After 5 Minutes)

```
✅ Copilot opened PR #567 for issue #456!

PR Details:
Title: feat: Add rate limiting to /api/users endpoint (#456)
URL: https://github.com/owner/repo/pull/567
State: OPEN
Files changed: 4
Commits: 3

Modified files:
• src/api/routes/users.js
• src/middleware/rateLimiter.js  
• tests/api/users.test.js
• docs/api.md

Next steps:
• Review the code: gh pr view 567
• Check CI status: gh pr checks 567
• Approve when ready: gh pr review 567 --approve
• Merge: gh pr merge 567 --squash
```

## Monitoring CI Checks

**User Request:**
> "Watch the CI checks on Copilot's PR"

**Agent Response:**
```
📊 Monitoring CI checks for PR #567...

Current status:
✓ build (2m 14s)
✓ test (4m 32s)
○ lint (pending)
○ security-scan (pending)

Running: gh pr checks 567 --watch --required

I'll notify you when all checks complete.
```

## CI Completion

```
✅ All required checks passed for PR #567!

Final status:
✓ build (2m 14s)
✓ test (4m 32s)
✓ lint (1m 03s)
✓ security-scan (45s)

The PR is ready to merge:
  gh pr merge 567 --squash --delete-branch

Would you like me to review the code changes first?
```

## Complete Command Sequence

```bash
# 1. Assign Copilot
gh issue edit 456 --add-assignee @copilot

# 2. Verify assignment
gh issue view 456 --json assignees --jq '.assignees[].login'

# 3. Wait and check for PR (after a few minutes)
gh pr list --author Copilot --search "issue #456" --json number,title,url

# 4. View PR details
PR_NUM=567
gh pr view $PR_NUM

# 5. Monitor CI checks
gh pr checks $PR_NUM --watch

# 6. Review and merge
gh pr review $PR_NUM --approve
gh pr merge $PR_NUM --squash --delete-branch
```

## Notes

- **Timing:** Copilot typically takes 2-10 minutes from assignment to PR
- **Issue Quality:** Well-written issues with clear acceptance criteria get better results
- **Multiple Assignees:** You can assign both yourself and Copilot: `--add-assignee @me,@copilot`
- **Monitoring:** Use watch-ci-skill for automated monitoring of Copilot's PR
