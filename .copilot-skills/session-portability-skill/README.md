# Session Portability

Continue Copilot CLI work across environments (local ↔ Codespace) by generating a handoff prompt that carries context into a new session.

## Why Not File Transfer?

`copilot --resume <uuid>` does **not** restore conversation history from a transferred `events.jsonl` — it creates a fresh session that overwrites the transferred data. This skill uses a **handoff prompt** approach instead: capture context, generate a prompt, paste it into a new session in the target environment.

## When to Use This Skill

- You started a Copilot CLI session locally and want to continue it in a Codespace
- You started a session in a Codespace and want to bring it back to your local machine
- You need to pick up where you left off after switching environments

## Prerequisites

- [GitHub CLI](https://cli.github.com/) (`gh`) installed and authenticated
- [Copilot CLI](https://docs.github.com/en/copilot/github-copilot-in-the-cli) installed
- A Git branch pushed to the remote so it's available in both environments
- A target environment (e.g., a running GitHub Codespace or a local clone) to continue work in

## Installation

### Personal Skill

```bash
cp -r session-portability-skill ~/.copilot/skills/
```

### Project Skill

```bash
cp -r session-portability-skill /path/to/repo/.github/skills/
```

## Usage

Trigger this skill by asking Copilot to transfer or migrate a session:

- "Transfer my session to my Codespace"
- "Move this session to Codespace"
- "Resume this session in Codespace"
- "Copy my Codespace session to local"
- "Port my session to local"

The agent will:

1. Gather your current session context (branch, plan, progress, uncommitted changes)
2. Generate a self-contained handoff prompt
3. Guide you to push your branch and start a new session in the target environment
4. Recommend using `/share` for a full conversation backup

## How It Works

Instead of copying session files (which doesn't work with `copilot --resume`), the skill:

- Reads `plan.md`, todo status, branch info, and uncommitted changes
- Assembles a structured handoff prompt with everything the new session needs
- The user pushes their branch, opens the target environment, and pastes the prompt

This preserves the important context (what was being done, what's left, key decisions) without relying on broken session-resume functionality.

## Security

⚠️ The handoff prompt may contain file paths, task descriptions, or commit messages that reference internal systems. The skill:

- Warns users to review the prompt before sharing outside their own environments
- Never includes secrets, tokens, or credentials in the handoff prompt
- Reminds users that `/share` gists are secret (unlisted) but viewable by anyone with the URL

See the [Security Considerations section in SKILL.md](SKILL.md#security-considerations) for full details.

## Examples

See [examples/example-transfer.md](examples/example-transfer.md) for a complete walkthrough.

---

**Required:** GitHub CLI (`gh`) with Copilot extension
