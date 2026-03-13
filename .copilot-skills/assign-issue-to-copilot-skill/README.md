# Assign Issue to Copilot Skill

Delegate GitHub issues to Copilot (the coding agent) and write issues optimized for Copilot to work on effectively.

## When to Use This Skill

- Assigning Copilot to work on issues
- Creating issues that Copilot can pick up automatically
- Monitoring Copilot's progress on assigned issues
- Batch-assigning multiple issues to Copilot
- Checking if Copilot has opened a PR for an issue

## Installation

### Using gh-hubber-skills CLI (Recommended)

```bash
# Install the skill
gh hubber-skills install assign-issue-to-copilot-skill

# Install to your project
gh hubber-skills install assign-issue-to-copilot-skill --project
```

### Manual Installation

**Personal skills** (available across all your projects):
```bash
cp -r assign-issue-to-copilot-skill ~/.copilot/skills/
```

**Project-specific skills**:
```bash
cp -r assign-issue-to-copilot-skill /path/to/your/repo/.github/skills/
```

## Usage

This skill activates when you ask Copilot to:
- "Assign Copilot to this issue"
- "Have Copilot work on issue #123"
- "Give this to Copilot"
- "Let Copilot handle this"
- "Assign the coding agent to these issues"
- "Write an issue for Copilot to pick up"

The skill will:
1. Assign Copilot using the correct `@copilot` assignee syntax
2. Verify the assignment succeeded
3. Monitor for when Copilot opens a PR
4. Check CI status on Copilot's PR
5. Guide you on writing Copilot-friendly issues

## Features

- **Correct assignee syntax** - Uses `@copilot` (not `Copilot` or `copilot`)
- **Batch assignments** - Assign multiple issues at once
- **Progress monitoring** - Check if Copilot has started working
- **Error handling** - Detects when Copilot isn't available for a repo
- **Issue writing guidance** - Templates and best practices for Copilot-ready issues
- **Integration with watch-ci** - Monitor Copilot's PR checks

## Quick Examples

### Assign a Single Issue

```bash
# User: "Assign Copilot to issue #123"
# Agent: Assigning Copilot to issue #123...
gh issue edit 123 --add-assignee @copilot
# ✅ Copilot assigned successfully!
```

### Write a Copilot-Ready Issue

```bash
# User: "Create an issue for Copilot to add rate limiting to the API"
# Agent creates issue with:
# - Clear problem statement
# - Specific solution approach
# - File paths to modify
# - Acceptance criteria
# - Testing requirements
```

### Batch Assign Multiple Issues

```bash
# User: "Assign Copilot to issues #100, #101, and #102"
# Agent: Batch assigning Copilot...
for issue in 100 101 102; do
  gh issue edit $issue --add-assignee @copilot
done
# ✅ Assigned Copilot to 3 issues
```

### Monitor Copilot's Progress

```bash
# User: "Has Copilot started working on issue #123?"
# Agent: Checking for PR...
gh pr list --author Copilot --search "issue #123"
# ✅ Copilot opened PR #234
```

## Writing Good Issues for Copilot

Use this template when creating issues for Copilot:

```markdown
## Problem
[Clear description of what needs to be done and why]

## Proposed Solution
[Specific approach, including libraries/tools to use]

## Files to Modify/Create
- `path/to/file.js` - [what needs to change]

## Acceptance Criteria
- [ ] [Specific, testable requirement]
- [ ] All existing tests pass
- [ ] New tests added

## Testing
[How to test the changes]
```

### Best Practices

✅ **DO:**
- Be specific about file paths and locations
- Include clear acceptance criteria
- Specify test expectations
- Link to related docs or examples
- Mention coding standards to follow

❌ **DON'T:**
- Use vague language like "fix the thing"
- Combine multiple unrelated changes
- Omit testing requirements
- Forget to provide context

## Prerequisites

- GitHub CLI (`gh`) installed and authenticated
- Repository must have Copilot coding agent enabled
- Write access to the repository
- **Not supported on GitHub Enterprise Server (GHES)**

## Tips

- Copilot typically starts working within 1-5 minutes of assignment
- Use `@copilot` as the assignee (with @ symbol)
- More detailed issues = better Copilot results
- Monitor progress using `gh pr list --author Copilot`
- Combine with watch-ci-skill to monitor Copilot's PR checks

## Common Issues

### "assignee not found" error

**Problem:** Using wrong assignee format

**Solution:** Use `@copilot` (with @ symbol):
```bash
gh issue edit 123 --add-assignee @copilot
```

### Copilot not starting

**Problem:** Issue lacks detail or repo doesn't have Copilot enabled

**Solution:** 
1. Ensure issue has clear description and acceptance criteria
2. Verify repo has Copilot coding agent enabled (contact admin)
3. Check: `gh pr list --author Copilot` to confirm Copilot is available

### Permission denied

**Problem:** Insufficient GitHub permissions

**Solution:**
```bash
gh auth refresh -s repo
```

## Examples

See the `examples/` directory for detailed scenarios:
- **assign-single-issue.md** - Complete workflow for assigning one issue
- **batch-assign.md** - Assigning multiple issues efficiently
- **write-issue.md** - Creating a Copilot-ready issue from scratch

---

**Note:** This skill requires GitHub CLI (`gh`) v2.40.0+ and works with GitHub.com repositories that have Copilot coding agent enabled.
