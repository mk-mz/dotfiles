# Command Reference

Quick reference for all GitHub CLI commands related to assigning and monitoring Copilot.

## Core Assignment Commands

### Assign Copilot to an Issue

```bash
# Basic assignment
gh issue edit ISSUE_NUMBER --add-assignee @copilot

# Assign to issue in specific repo
gh issue edit ISSUE_NUMBER --repo OWNER/REPO --add-assignee @copilot

# Assign yourself AND Copilot
gh issue edit ISSUE_NUMBER --add-assignee @me,@copilot
```

### Remove Copilot Assignment

```bash
# Unassign Copilot
gh issue edit ISSUE_NUMBER --remove-assignee @copilot

# Remove Copilot and yourself as assignees
gh issue edit ISSUE_NUMBER --remove-assignee @copilot,@me
```

## Verification Commands

### Check Issue Assignment

```bash
# View all assignees
gh issue view ISSUE_NUMBER --json assignees --jq '.assignees[].login'

# Check if Copilot is assigned
gh issue view ISSUE_NUMBER --json assignees --jq '.assignees[] | select(.login == "Copilot")'

# Full issue details
gh issue view ISSUE_NUMBER --json number,title,assignees,state,labels
```

### List Issues Assigned to Copilot

```bash
# All issues assigned to Copilot
gh issue list --assignee Copilot

# Open issues only
gh issue list --assignee Copilot --state open

# With JSON output
gh issue list --assignee Copilot --json number,title,state,updatedAt
```

## Monitoring Commands

### Check for Copilot's PRs

```bash
# PRs by Copilot that reference an issue
gh pr list --author Copilot --search "issue #123"

# All open PRs by Copilot
gh pr list --author Copilot --state open

# Recent PRs with full details
gh pr list --author Copilot --limit 10 --json number,title,url,state,createdAt
```

### View PR Details

```bash
# Basic PR view
gh pr view PR_NUMBER

# JSON format
gh pr view PR_NUMBER --json number,title,body,state,author

# View files changed
gh pr view PR_NUMBER --json files --jq '.files[].path'

# View PR diff
gh pr diff PR_NUMBER
```

### Monitor CI Checks

```bash
# Watch checks (blocks until complete)
gh pr checks PR_NUMBER --watch

# Watch required checks only
gh pr checks PR_NUMBER --required --watch

# Check status without watching
gh pr checks PR_NUMBER

# Get JSON output
gh pr checks PR_NUMBER --json name,conclusion,status
```

## Batch Operations

### Batch Assign Issues

```bash
# Sequential assignment
for issue in 100 101 102 103; do
  gh issue edit "$issue" --add-assignee @copilot
  sleep 1
done

# Assign all issues with a label
gh issue list --label "ready-for-copilot" --json number --jq '.[].number' | \
  while read -r issue; do
    gh issue edit "$issue" --add-assignee @copilot
    sleep 1
  done

# Parallel assignment (with rate limit consideration)
echo "100 101 102" | xargs -n 1 -P 3 -I {} gh issue edit {} --add-assignee @copilot
```

### Batch Check Status

```bash
# Check multiple issues
for issue in 100 101 102; do
  echo "Issue #$issue:"
  gh issue view "$issue" --json assignees,state --jq '{assignees: (.assignees | map(.login)), state: .state}'
done

# Check all Copilot PRs
gh pr list --author Copilot --json number,title,state | jq -r '.[] | "\(.number): \(.title) - \(.state)"'
```

## Issue Creation

### Create Issue with Template

```bash
# Create simple issue
gh issue create --title "Issue title" --body "Issue description"

# Create and assign to Copilot immediately
gh issue create \
  --title "Add feature X" \
  --body "Detailed description..." \
  --assignee @copilot

# Create with labels
gh issue create \
  --title "Bug fix" \
  --body "Description" \
  --label "bug,priority:high" \
  --assignee @copilot

# Create from file
gh issue create \
  --title "Feature request" \
  --body-file issue-template.md \
  --assignee @copilot
```

### Create Issue from PR

```bash
# Link issue to PR
gh issue create \
  --title "Implement feature from PR discussion" \
  --body "Based on discussion in PR #123" \
  --assignee @copilot
```

## Search and Filter

### Search Issues

```bash
# Search for issues by text
gh issue list --search "authentication"

# Search by label
gh issue list --label "bug"

# Search by state
gh issue list --state closed

# Complex search
gh issue list --search "rate limiting is:open label:enhancement"
```

### Search PRs

```bash
# Search PRs by title/body
gh pr list --search "rate limiting"

# PRs by author and search term
gh pr list --author Copilot --search "authentication"

# PRs in specific state
gh pr list --state merged --author Copilot

# PRs created in last 7 days
gh pr list --search "created:>=$(date -d '7 days ago' +%Y-%m-%d)"
```

## Advanced Queries

### Get Issues Ready for Copilot

```bash
# Issues with no assignees
gh issue list --assignee "" --state open --json number,title

# Issues labeled "good first issue" without Copilot
gh issue list --label "good first issue" --json number,title,assignees | \
  jq '.[] | select(.assignees | length == 0)'
```

### Track Copilot's Progress

```bash
# Get all Copilot's work today
TODAY=$(date +%Y-%m-%d)
gh pr list --author Copilot --search "created:>=$TODAY" --json number,title,createdAt
```

### Check Repository Activity

```bash
# List all issues (open and closed)
gh issue list --state all --limit 100

# List all PRs by all authors
gh pr list --state all --limit 100

# Get repository info
gh repo view --json name,owner,description
```

## Workflow Automation

### Complete Assignment Workflow

```bash
#!/bin/bash
# assign-and-monitor.sh

ISSUE=$1

# 1. Assign Copilot
echo "Assigning Copilot to issue #$ISSUE..."
gh issue edit "$ISSUE" --add-assignee @copilot

# 2. Wait for Copilot to start
echo "Waiting for Copilot to open PR..."
for i in {1..20}; do
  sleep 30
  PR=$(gh pr list --author Copilot --search "issue #$ISSUE" --json number --jq '.[0].number')
  
  if [ -n "$PR" ]; then
    echo "✅ Copilot opened PR #$PR!"
    break
  fi
  
  echo "⏳ Waiting... (attempt $i/20)"
done

# 3. Monitor PR if created
if [ -n "$PR" ]; then
  echo "Monitoring PR #$PR checks..."
  gh pr checks "$PR" --watch
else
  echo "⚠️ Copilot hasn't opened a PR yet"
  exit 1
fi
```

### Bulk Status Report

```bash
#!/bin/bash
# copilot-status-report.sh

echo "Copilot Activity Report"
echo "======================="
echo ""

# Issues assigned to Copilot
ASSIGNED=$(gh issue list --assignee Copilot --json number,title,state)
ASSIGNED_COUNT=$(echo "$ASSIGNED" | jq 'length')

echo "Assigned Issues: $ASSIGNED_COUNT"
echo "$ASSIGNED" | jq -r '.[] | "  #\(.number): \(.title) [\(.state)]"'
echo ""

# PRs opened by Copilot
OPEN_PRS=$(gh pr list --author Copilot --state open --json number,title)
OPEN_COUNT=$(echo "$OPEN_PRS" | jq 'length')

echo "Open PRs: $OPEN_COUNT"
echo "$OPEN_PRS" | jq -r '.[] | "  #\(.number): \(.title)"'
echo ""

# Merged PRs (last 7 days)
MERGED=$(gh pr list --author Copilot --state merged --search "merged:>=$(date -d '7 days ago' +%Y-%m-%d)" --json number,title)
MERGED_COUNT=$(echo "$MERGED" | jq 'length')

echo "Merged PRs (last 7 days): $MERGED_COUNT"
echo "$MERGED" | jq -r '.[] | "  #\(.number): \(.title)"'
```

## Error Handling

### Check Authentication

```bash
# Verify logged in
gh auth status

# Refresh auth token
gh auth refresh

# Login if needed
gh auth login
```

### Handle Missing Issues/PRs

```bash
# Check if issue exists before assigning
if gh issue view "$ISSUE" &>/dev/null; then
  gh issue edit "$ISSUE" --add-assignee @copilot
else
  echo "Error: Issue #$ISSUE not found"
  gh issue list --limit 10
fi
```

### Test Copilot Availability

```bash
# Try assigning and check error
output=$(gh issue edit "$ISSUE" --add-assignee @copilot 2>&1)
status=$?

if [ "$status" -ne 0 ]; then
  if echo "$output" | grep -qi "not found"; then
    echo "❌ Copilot is not available for this repository"
    echo "Contact repository admin to enable Copilot coding agent"
  else
    echo "❌ Failed to assign Copilot to issue #$ISSUE"
    echo "$output"
  fi
  exit 1
else
  echo "✅ Copilot assigned successfully"
fi
```

## JQ Recipes

### Extract Specific Fields

```bash
# Get just issue numbers
gh issue list --assignee Copilot --json number --jq '.[].number'

# Get number and title
gh issue list --json number,title --jq '.[] | "\(.number): \(.title)"'

# Filter by criteria
gh pr list --author Copilot --json number,state,createdAt | \
  jq '.[] | select(.state == "OPEN") | select(.createdAt > "2024-01-01")'
```

### Count and Aggregate

```bash
# Count open issues
gh issue list --assignee Copilot --state open --json number --jq 'length'

# Group by state
gh pr list --author Copilot --json state | jq 'group_by(.state) | map({state: .[0].state, count: length})'
```

## Environment Variables

```bash
# Set default repo
export GH_REPO="owner/repo"

# Now you can omit --repo flag
gh issue edit 123 --add-assignee @copilot

# Set default pager
export GH_PAGER=""  # Disable paging

# Debug mode
export GH_DEBUG=1
gh issue view 123
```

## Useful Aliases

Add to `~/.gitconfig` or `~/.bash_aliases`:

```bash
# Assign Copilot to issue
gh-assign-copilot() {
  gh issue edit "$1" --add-assignee @copilot
}

# Check Copilot PRs
alias gh-copilot-prs='gh pr list --author Copilot'

# Copilot status
alias gh-copilot-status='gh issue list --assignee Copilot && gh pr list --author Copilot'
```

## Notes

- All commands require GitHub CLI (`gh`) v2.40.0+
- `@copilot` is case-insensitive but conventionally lowercase
- Rate limiting: Add 1-second delays between bulk operations
- Not supported on GitHub Enterprise Server (GHES)
