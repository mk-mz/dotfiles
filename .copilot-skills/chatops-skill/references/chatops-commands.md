# ChatOps Commands Reference

A categorized reference of common GitHub ChatOps (Hubot) commands. For complete documentation, refer to `github/thehub`.

## General & Help

| Command | Description | Example |
|---------|-------------|---------|
| `.help` | Display Hubot help glossary | `.help` |
| `.help <command>` | Get help for a specific command | `.help deploy` |
| `.glossary me <term>` | Look up a glossary term | `.glossary me OTP` |
| `hubot rpc list` | List all available RPC namespaces | `hubot rpc list` |
| `hubot rpc help <namespace>` | Get help for a namespace | `hubot rpc help deploy` |

## Deployment Commands (Heaven)

| Command | Description | Example |
|---------|-------------|---------|
| `.deploy <app> to <env>` | Deploy application to environment | `.deploy github to production` |
| `.deploy <app> to <env> with <options>` | Deploy with options | `.deploy github to staging with migrations` |
| `.deploy locks` | Show active deployment locks | `.deploy locks` |
| `.deploy status <app>` | Check deployment status | `.deploy status github` |
| `.deploy history <app> <env>` | View deployment history | `.deploy history github production` |
| `.deploy rollback <app> <env>` | Rollback last deployment | `.deploy rollback github production` |
| `.deploy help` | Get deployment help | `.deploy help` |

**⚠️ Security Note:** Deployment commands affect production. Always verify environment names and have a rollback plan.

## CI/CD Commands (Janky)

| Command | Description | Example |
|---------|-------------|---------|
| `.ci build <job>` | Trigger a CI build | `.ci build integration-tests` |
| `.ci status <job>` | Check build status | `.ci status unit-tests` |
| `.ci list` | List available CI jobs | `.ci list` |
| `.ci history <job>` | View build history | `.ci history smoke-tests` |
| `.ci cancel <build-id>` | Cancel a running build | `.ci cancel 12345` |
| `.ci help` | Get CI help | `.ci help` |

## Infrastructure Commands (Instance)

| Command | Description | Example |
|---------|-------------|---------|
| `.instance create <name>` | Create an instance | `.instance create staging-test` |
| `.instance destroy <name>` | Destroy an instance | `.instance destroy staging-test` |
| `.instance list` | List instances | `.instance list` |
| `.instance status <name>` | Check instance status | `.instance status my-instance` |
| `.instance help` | Get instance help | `.instance help` |

**⚠️ Security Note:** Instance commands provision infrastructure. Verify before running.

## Sparkles ✨ (Recognition)

| Command | Description | Example |
|---------|-------------|---------|
| `.sparkle @username` | Give someone sparkles | `.sparkle @octocat` |
| `.sparkle @username for [reason]` | Give sparkles with reason | `.sparkle @octocat for great code review` |
| `.sparkle @user for "[multi-word]"` | Use quotes for multi-word reasons | `.sparkle @octocat for "fixing production bug"` |
| `.sparkle leaderboard` | Display sparkle leaderboard | `.sparkle leaderboard` |
| `.sparkle stats` | View sparkle statistics | `.sparkle stats` |
| `.sparkle me` | See your own sparkles | `.sparkle me` |

**💡 Pro Tip:** Always include a reason to make sparkles more meaningful!

## Social & Information Commands

| Command | Description | Example |
|---------|-------------|---------|
| `.remote me` | Show remote hubbers | `.remote me` |
| `.time me <city>` | Get time in a city | `.time me Tokyo` |
| `.where is @username` | Find a hubber's location | `.where is @octocat` |
| `.weather me <location>` | Get current weather | `.weather me San Francisco` |
| `.zoom` | Start an instant Zoom meeting | `.zoom` |

## Memory & Resources

| Command | Description | Example |
|---------|-------------|---------|
| `.rem <keywords>` | Recall a saved URL/image/GIF | `.rem success kid` |
| `.save <url> as <keywords>` | Save a resource | `.save https://... as deployment guide` |

## Database Commands (MySQL)

| Command | Description | Example |
|---------|-------------|---------|
| `.mysql <cluster> status` | Check cluster status | `.mysql production status` |
| `.mysql <cluster> query <sql>` | Run a query (read-only) | `.mysql staging query SELECT COUNT(*) FROM users` |
| `.mysql list` | List available clusters | `.mysql list` |

**⚠️ SECURITY CRITICAL:** MySQL commands access production data. Requires special access and audit logging.

**Documentation:** `docs/epd/engineering/products-and-services/internal/chatops/mysql-commands.md`

## Workflow Commands (GitHub Actions)

| Command | Description | Example |
|---------|-------------|---------|
| `.workflow run <name>` | Trigger a workflow | `.workflow run deploy-staging` |
| `.workflow status <name>` | Check workflow status | `.workflow status build` |
| `.workflow list` | List workflows | `.workflow list` |
| `.workflow cancel <run-id>` | Cancel a workflow run | `.workflow cancel 12345` |

**Documentation:** `docs/epd/engineering/products-and-services/internal/chatops/workflow-chatops.md`

## Namespace Organization

ChatOps commands are organized into namespaces using the RPC (Remote Procedure Call) system:

### Core Namespaces

- **deploy** - Heaven deployment system
- **ci** - Janky CI/CD integration
- **instance** - Infrastructure provisioning
- **mysql** - Database operations
- **workflow** - GitHub Actions workflows
- **sparkle** - Recognition system

### Discovering Namespaces

```bash
# List all available namespaces
hubot rpc list

# Get help for a specific namespace
hubot rpc help <namespace>

# Example
hubot rpc help deploy
```

## Command Syntax Conventions

### Required vs Optional Arguments

- `<required>` - Required parameter
- `[optional]` - Optional parameter
- `<choice1|choice2>` - Choose one option

### Command Prefixes

- `.command` - Dot prefix (most common)
- `hubot command` - Full prefix (equivalent to dot)

**Example:** These are equivalent:
```
.help
hubot help
```

### Multi-word Arguments

Use quotes for arguments with spaces:
```
.sparkle @user for "excellent code review and thorough testing"
```

## Security Levels

Commands are categorized by risk level:

### 🟢 Low Risk
- Information queries (`.time`, `.where is`, `.weather`)
- Sparkles (`.sparkle`)
- Help commands (`.help`, `.glossary`)

### 🟡 Medium Risk
- CI builds (`.ci build`)
- Staging deployments (`.deploy X to staging`)
- Non-production operations

### 🔴 High Risk
- Production deployments (`.deploy X to production`)
- Infrastructure provisioning (`.instance`)
- Database operations (`.mysql`)

**Practice High-Risk Commands:** Always test in `#learn-hubot` first!

## Getting Help

### In Slack

```bash
# General help
.help

# Command-specific help
.help deploy
.help ci

# Namespace help
hubot rpc help deploy

# List all commands in a namespace
hubot rpc help ci
```

### Documentation Locations

All documentation lives in `github/thehub`:

**Main Guides:**
- `docs/guides/hubot.md` - Quick reference guide
- [Complete reference](https://thehub.github.com/epd/engineering/products-and-services/internal/chatops/hubot/commands-reference/)

**System-Specific:**
- `docs/epd/engineering/products-and-services/internal/chatops/mysql-commands.md`
- `docs/epd/engineering/products-and-services/internal/chatops/workflow-chatops.md`

**Getting Started:**
- `docs/epd/engineering/products-and-services/internal/chatops/hubot/getting-started-with-hubot.md`
- `docs/epd/engineering/products-and-services/internal/chatops/hubot/adding-hubot-to-a-new-slack-channel.md`

**Security:**
- `docs/security/policy-desk/standards/chatops-command-security-and-risk-standard.md`

### Fetching Documentation

Prefer reading from a local `github/thehub` clone when available. Fall back to the GitHub API if the repo is not cloned locally.

```bash
# GitHub API (fallback)
gh api "repos/github/thehub/contents/docs/epd/engineering/products-and-services/internal/chatops/hubot/commands-reference.md" --jq '.content' | base64 -d

# Search for specific topics
gh search code "TOPIC" --repo github/thehub --filename "*.md" --include-path "chatops"
```

## Practice Environment

### #learn-hubot Channel

A safe space to practice ChatOps commands:

**What you can do:**
- Test any command syntax
- Experiment without production impact
- Learn command responses
- Get familiar with Hubot's behavior
- Make mistakes safely

**How to use it:**
1. Join `#learn-hubot` in Slack
2. Try commands: `.help`, `.sparkle @hubot`, etc.
3. Experiment with different syntax
4. Ask questions if stuck

**Example Practice Flow:**
```
# In #learn-hubot
.help
.sparkle @hubot for being helpful
.ci list
.deploy help
hubot rpc list
```

## Common Workflows

### Deployment Workflow
1. Check locks: `.deploy locks`
2. Verify status: `.deploy status <app>`
3. Deploy: `.deploy <app> to <env>`
4. Monitor: Watch channel for completion
5. If needed: `.deploy rollback <app> <env>`

### CI Workflow
1. List jobs: `.ci list`
2. Trigger build: `.ci build <job>`
3. Check status: `.ci status <job>`
4. View results: Check linked build logs

### Sparkles Workflow
1. Identify person to recognize
2. Give sparkles: `.sparkle @user for [reason]`
3. Check leaderboard: `.sparkle leaderboard`

## Tips & Best Practices

### Do's ✅
- Always verify environment names in deployment commands
- Include reasons when giving sparkles
- Practice new commands in `#learn-hubot`
- Check for locks before deploying
- Use `.help` when unsure
- Double-check production commands

### Don'ts ❌
- Don't deploy to production without verification
- Don't skip the practice environment
- Don't use database commands without proper access
- Don't forget to monitor deployment progress
- Don't assume command syntax - look it up

## Related Systems

ChatOps integrates with:
- **Heaven** - Deployment orchestration
- **Janky** - CI/CD system
- **RPC Controllers** - Custom command backends
- **Sparkles** - Recognition tracking
- **GitHub Actions** - Workflow automation
- **Slack** - Chat interface

## Related Repositories

- `github/hubot-classic` - Hubot implementation
- `github/hubot-rpc-config` - RPC configuration
- `github/chatops-controller` - ChatOps controller
- `github/heaven` - Deployment system
- `github/janky` - CI system

---

**Last Updated:** 2026-02-09
**Source:** `github/thehub` ChatOps documentation
**Practice:** `#learn-hubot` on Slack
