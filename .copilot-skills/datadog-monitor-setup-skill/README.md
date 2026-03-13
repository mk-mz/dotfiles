# Datadog Monitor Setup Skill

Guide users through setting up Datadog monitors following GitHub's conventions and best practices.

## What This Skill Does

This skill helps you create well-structured Datadog monitors by:
- Validating monitor naming conventions (`service/monitor-name` pattern)
- Selecting appropriate priority levels
- Structuring monitor queries and messages correctly
- Avoiding common configuration mistakes
- Understanding the workflow from UI creation to PR merge

## When to Use This Skill

Use this skill when you need to:
- Create a new Datadog monitor
- Ensure monitor configuration follows GitHub conventions
- Understand monitor priority levels and their impact
- Set up proper alerting for a service
- Validate monitor YAML structure

## Installation

Copy or symlink the skill to your Copilot CLI skills directory:

```bash
# Using symlink (recommended for development)
ln -s "$(pwd)/datadog-monitor-setup-skill" ~/.copilot/skills/

# Or copy the directory
cp -r datadog-monitor-setup-skill ~/.copilot/skills/
```

## Usage

Trigger this skill by asking:
- "Help me set up a Datadog monitor"
- "Create a Datadog monitor for my service"
- "What's the correct format for a Datadog monitor?"
- "Validate my Datadog monitor configuration"

## Examples

See the [examples directory](./examples/) for sample monitor configurations and common patterns.

## Related Skills

- **datadog-troubleshooting-skill**: Debug Datadog monitor deployment issues
