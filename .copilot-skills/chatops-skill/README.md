# ChatOps Skill

Look up and explain GitHub's ChatOps (Hubot) commands, syntax, and workflows - access to 1,000+ commands for deployments, incident response, sparkles, and more.

## When to Use This Skill

- Finding ChatOps commands by name or function
- Learning Hubot command syntax and arguments
- Getting guidance on deployment, incident response, or other workflows
- Discovering what commands are available for specific systems
- Adding Hubot to a Slack channel
- Giving sparkles or using social commands
- Practicing ChatOps in a safe environment

## Prerequisites

This skill uses GitHub CLI to fetch documentation from `github/thehub`:

```bash
# Verify gh is installed and authenticated
gh auth status
```

The skill fetches documentation from these key locations:
- `docs/guides/hubot.md` - Common commands guide
- `docs/epd/engineering/products-and-services/internal/chatops/` - Full ChatOps documentation
- `docs/security/policy-desk/standards/chatops-command-security-and-risk-standard.md` - Security standards

## Installation

### Using gh-hubber-skills (Recommended)

```bash
# Install the extension
gh extension install github/gh-hubber-skills

# Install the skill
gh hubber-skills install chatops-skill
```

### Manual Installation

**Personal Skills**
```bash
cp -r chatops-skill ~/.copilot/skills/
```

**Project Skills**
```bash
cp -r chatops-skill /path/to/repo/.github/skills/
```

## Usage

This skill activates when you ask Copilot to:
- "How do I deploy with chatops?"
- "What's the hubot command for X?"
- "Show me the deploy commands"
- "How do I give someone sparkles?"
- "What chatops commands are available for search?"
- "How do I add hubot to a channel?"
- "How do I use .ci commands?"

The skill will:
1. Search thehub documentation for the command
2. Show exact syntax with examples
3. Explain required and optional arguments
4. Provide security warnings for sensitive commands
5. Suggest practice environment (`#learn-hubot`)
6. Link to relevant documentation

## Features

- **Command Lookup** - Find commands by name or function
- **Syntax Help** - Get exact command syntax and arguments
- **Workflow Guidance** - Step-by-step for deployments, sparkles, etc.
- **Namespace Discovery** - Explore available command namespaces
- **Security Awareness** - Warnings for production-impacting commands
- **Practice Environment** - Points users to `#learn-hubot` for safe testing

## Common Commands

| Command | Description |
|---------|-------------|
| `.help` | Hubot help glossary |
| `.deploy <app> to <env>` | Deploy applications |
| `.ci (build\|status\|list) ...` | Janky CI operations |
| `.sparkle @user for [reason]` | Give sparkles ✨ |
| `.zoom` | Start instant Zoom meeting |
| `.time me [city]` | Check time in a city |
| `hubot rpc list` | List command namespaces |

## Examples

### Find a deployment command
```
User: "How do I deploy github to production with chatops?"
Agent: Fetches deployment command syntax, shows safety warnings, provides examples
```

### Give sparkles
```
User: "How do I give someone sparkles?"
Agent: Shows sparkle command syntax, examples with and without reasons, mentions leaderboard
```

### Command discovery
```
User: "What chatops commands are available for CI?"
Agent: Lists .ci namespace commands, shows syntax, explains usage
```

## Security Notes

⚠️ **Production-Impacting Commands**

Some commands affect production systems:
- `.deploy` - Deployments
- `.instance` - Infrastructure provisioning
- MySQL commands - Database operations

The skill will:
- Warn about security implications
- Reference security standards from thehub
- Recommend testing in `#learn-hubot` first
- Verify user has appropriate access

## Documentation Sources

This skill references documentation from `github/thehub`:
- ChatOps overview and architecture
- Full Hubot commands reference
- System-specific guides (MySQL, Workflow, etc.)
- Security standards and best practices
- Getting started guides

## Practice Environment

**#learn-hubot channel** - Safe place to:
- Test new commands
- Learn syntax
- Experiment without risk
- Get familiar with ChatOps

The skill always recommends practicing here first!

## Tips

- Commands use `.` prefix (`.deploy`) or `hubot` prefix (`hubot help`)
- Use quotes for multi-word arguments: `.sparkle @user for "great work"`
- Check `hubot rpc list` to discover available command namespaces
- Always verify environment names in deployment commands
- Practice sensitive commands in `#learn-hubot` before production use

---

**Required:** GitHub CLI (`gh`) with access to `github/thehub` repository
