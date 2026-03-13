---
name: chatops
description: This skill should be used when the user asks "how do I deploy with chatops?", "what's the hubot command for X?", "how do I give someone sparkles?", "show me the deploy chatops commands", "how do I add hubot to a channel?", "what chatops commands are available?", "how do I use .ci commands?", "what are the hubot commands for X?", or needs help finding or using GitHub ChatOps/Hubot commands and workflows.
---

# ChatOps Reference - GitHub Hubot Command Lookup

Helps agents look up and explain GitHub's ChatOps (Hubot) commands, syntax, and workflows. Provides access to the 1,000+ Hubot commands used across GitHub for deployments, incident response, sparkles, and more.

## When to Use This Skill

- User needs to find a ChatOps command by name or function
- Asking about Hubot command syntax or arguments
- Requesting guidance on ChatOps workflows (deployment, incident response, etc.)
- Wants to know what commands are available for a specific system
- Needs help adding Hubot to a Slack channel
- Learning about ChatOps for the first time
- Wants to give someone sparkles or use social commands

## Core Functionality

### 1. Command Lookup Process

When a user asks about a ChatOps command:

**Step 1: Identify the Need**
- What is the user trying to accomplish?
- Do they know the command name or just the function?
- Is this for a specific system (deploy, CI, instance, etc.)?

**Step 2: Search Command Documentation**

The primary reference is `docs/epd/engineering/products-and-services/internal/chatops/hubot/commands-reference.md` in the `github/thehub` repository.

**Option A: Local thehub clone (preferred)**

Check if `github/thehub` is cloned locally (e.g. using `find` or `locate`). If found, read the commands reference file directly and use `grep` to search for specific commands.

**Option B: Fetch via GitHub API (fallback)**

If the repo is not available locally:

```bash
# Get the full commands reference
gh api "repos/github/thehub/contents/docs/epd/engineering/products-and-services/internal/chatops/hubot/commands-reference.md" --jq '.content' | base64 -d

# Search for a specific command
gh search code "COMMAND_NAME" --repo github/thehub --filename "*.md" --include-path "chatops"
```

**Web reference:** https://thehub.github.com/epd/engineering/products-and-services/internal/chatops/hubot/commands-reference/

**Step 3: Present the Command**
- Show the exact syntax
- Explain required and optional arguments
- Provide usage examples
- Link to relevant documentation
- Note any security considerations

### 2. Common Commands Quick Reference

Keep these frequently-used commands readily available:

| Command | Description | Example |
|---------|-------------|---------|
| `.help` | Hubot help glossary | `.help` |
| `.glossary me <term>` | Look up a glossary term | `.glossary me OTP` |
| `.deploy <app> to <env>` | Heaven deployment chatops | `.deploy github to production` |
| `.ci <command> [args]` | Janky CI chatops | `.ci build github@master` |
| `.instance <action>` | Provisioning chatops | `.instance create staging` |
| `.sparkle [username]` | Give someone sparkles ✨ | `.sparkle @octocat` |
| `.sparkle [user] for [reason]` | Sparkle with a reason | `.sparkle @octocat for great review` |
| `.sparkle leaderboard` | Display sparkle leaderboard | `.sparkle leaderboard` |
| `.remote me` | Show remote hubbers | `.remote me` |
| `.time me [city]` | Time in a given city | `.time me Tokyo` |
| `.where is [username]` | Current location of a hubber | `.where is @octocat` |
| `.weather me [location]` | Current weather | `.weather me San Francisco` |
| `.zoom` | Start an instant Zoom meeting | `.zoom` |
| `.rem [keywords]` | Recall a saved URL/image/GIF | `.rem success kid` |
| `hubot rpc list` | List all ChatOps RPC namespaces | `hubot rpc list` |

### 3. Workflow Guidance

For multi-step workflows:

#### Deployment Workflow
1. Verify current environment status
2. Check for any locks or ongoing deploys
3. Use appropriate `.deploy` command
4. Monitor deployment progress
5. Verify successful deployment
6. Reference: https://thehub.github.com/epd/engineering/products-and-services/internal/chatops/hubot/commands-reference/

#### Sparkles Workflow
1. Identify the person to recognize
2. Craft a meaningful reason (optional but encouraged)
3. Use `.sparkle @username for [reason]`
4. Check leaderboard with `.sparkle leaderboard`
5. Reference: `docs/epd/engineering/products-and-services/internal/chatops/hubot/sparkles-internal.md`

#### Adding Hubot to a Channel
1. Invite Hubot to the Slack channel: `/invite @hubot`
2. Test with a simple command: `.help`
3. Configure channel-specific commands if needed
4. Reference: `docs/epd/engineering/products-and-services/internal/chatops/hubot/adding-hubot-to-a-new-slack-channel.md`

### 4. Namespace Discovery

Help users explore available command namespaces:

```bash
# List all RPC namespaces
hubot rpc list

# Get help for a specific namespace
hubot rpc help <namespace>
```

Common namespaces:
- `deploy` - Heaven deployment system
- `ci` - Janky CI integration
- `instance` - Infrastructure provisioning
- `mysql` - MySQL database operations
- `workflow` - GitHub Actions workflow operations

## Security Considerations

⚠️ **IMPORTANT: Security-Sensitive Commands**

Some ChatOps commands have security implications:

**High-Risk Commands:**
- `.deploy` - Production deployments
- `.instance` - Infrastructure provisioning
- MySQL commands - Database operations
- Any command that modifies production systems

**Before suggesting these commands:**
1. Verify the user has appropriate access
2. Reference security standards: `docs/security/policy-desk/standards/chatops-command-security-and-risk-standard.md`
3. Recommend testing in safe environments first
4. Suggest practicing in `#learn-hubot` channel

**Safety Tips:**
- Always double-check environment names in deploy commands
- Use dry-run or preview flags when available
- Verify locks and deployment status before deploying
- Practice new commands in `#learn-hubot` first

## Documentation Sources

Primary documentation locations in `github/thehub`:

**Core ChatOps Docs:**
- `docs/epd/engineering/products-and-services/internal/chatops/index.md` - ChatOps overview
- [Full command reference](https://thehub.github.com/epd/engineering/products-and-services/internal/chatops/hubot/commands-reference/)
- `docs/guides/hubot.md` - Common commands guide

**Getting Started:**
- `docs/epd/engineering/products-and-services/internal/chatops/hubot/getting-started-with-hubot.md`
- `docs/epd/engineering/products-and-services/internal/chatops/hubot/adding-hubot-to-a-new-slack-channel.md`

**System-Specific:**
- `docs/epd/engineering/products-and-services/internal/chatops/mysql-commands.md` - MySQL ChatOps
- `docs/epd/engineering/products-and-services/internal/chatops/workflow-chatops.md` - Workflow ChatOps

**Operations:**
- `docs/epd/engineering/products-and-services/internal/chatops/hubot/restarting-hubot.md`
- `docs/epd/engineering/products-and-services/internal/chatops/hubot/becoming-hubot.md` - Contributing

**Security:**
- `docs/security/policy-desk/standards/chatops-command-security-and-risk-standard.md`

## Fetching Documentation

Always prefer reading from a local clone of `github/thehub` when available. Check if the repo exists locally before making API calls. Fall back to the GitHub API only if the repo is not cloned locally.

**GitHub API (fallback):**

```bash
# Fetch specific documentation file
gh api "repos/github/thehub/contents/docs/epd/engineering/products-and-services/internal/chatops/hubot/commands-reference.md" --jq '.content' | base64 -d

# List all chatops-related files
gh api 'repos/github/thehub/git/trees/main?recursive=1' --jq '.tree[].path' | grep -i chatops

# Search for specific commands or topics
gh search code "SEARCH_TERM" --repo github/thehub --filename "*.md" --include-path "chatops"
```

## Command Syntax Notes

**Command Prefix:**
- Commands use `.` prefix (e.g., `.deploy`)
- The `.` prefix is synonymous with `hubot` (`.help` = `hubot help`)
- Some commands may use the full `hubot` prefix

**Arguments:**
- `<required>` - Required argument
- `[optional]` - Optional argument
- Multiple word arguments may need quotes: `.sparkle @user for "amazing work"`

## Practice Environment

**Recommend `#learn-hubot` for:**
- Testing new commands
- Learning command syntax
- Experimenting without risk
- Getting familiar with ChatOps

## Response Template

When providing command help, use this structure:

```
📋 ChatOps Command: <command name>

Syntax:
  <full command syntax>

Description:
  <what the command does>

Examples:
  <1-2 practical examples>

[Security Note: <if applicable>]

Documentation: <link to thehub docs>

Practice: Try it in #learn-hubot first!
```

## Common Pitfalls

**Avoid:**
- ❌ Suggesting commands without verifying syntax
- ❌ Assuming users have access to security-sensitive commands
- ❌ Recommending production commands without safety warnings
- ❌ Forgetting to mention practice environment

**Instead:**
- ✅ Look up exact syntax from documentation
- ✅ Note access requirements for sensitive commands
- ✅ Always include safety warnings for production operations
- ✅ Point users to `#learn-hubot` for practice

## Related Systems

ChatOps integrates with:
- **Heaven** - Deployment system
- **Janky** - CI/CD system
- **RPC Controllers** - Custom command processors
- **Sparkles** - Recognition system
- **GitHub Actions** - Workflow automation

**Related repositories:**
- `github/hubot-classic` - Hubot implementation
- `github/hubot-rpc-config` - RPC configuration
- `github/chatops-controller` - ChatOps controller

## Validation Checklist

Before providing a command recommendation:
- [ ] Verified command syntax from documentation
- [ ] Checked for security implications
- [ ] Provided usage examples
- [ ] Mentioned practice environment if appropriate
- [ ] Linked to relevant documentation
- [ ] Included any necessary warnings or prerequisites
