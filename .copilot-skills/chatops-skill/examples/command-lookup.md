# Example: Command Lookup

Help users find ChatOps commands by searching documentation.

## Scenario

A developer heard about ChatOps commands for CI but doesn't know the exact syntax.

## User Request

> "What chatops commands are available for running CI tests?"

## Agent Response - Step 1: Acknowledge Request

```
I'll help you find the CI-related ChatOps commands. Let me search the documentation.

🔍 Searching thehub for CI commands...
```

## Agent Response - Step 2: Search Documentation

The agent checks if `github/thehub` is cloned locally. If found, it searches the commands reference file directly. Otherwise, it falls back to the GitHub API:

```bash
# Fallback: fetch via GitHub API
gh api "repos/github/thehub/contents/docs/epd/engineering/products-and-services/internal/chatops/hubot/commands-reference.md" --jq '.content' | base64 -d | grep -F -i -A 15 '.ci'
```

## Agent Response - Step 3: Present Found Commands

```
📋 ChatOps CI Commands (Janky)

The `.ci` namespace provides continuous integration commands through Janky:

Basic Syntax:
  .ci <action> [options]

Common CI Commands:
  .ci build <job>              - Trigger a build
  .ci status <job>             - Check build status
  .ci list                     - List available jobs
  .ci help                     - Show CI help
  .ci history <job>            - View build history
  .ci cancel <build-id>        - Cancel a running build

Examples:
  .ci build integration-tests
  .ci status unit-tests
  .ci list
  .ci history smoke-tests

💡 Discovering Available Jobs:
First, list available CI jobs:
  .ci list

Then run your desired job:
  .ci build <job-name>
```

## Agent Response - Step 4: Additional Context

```
🎯 Common Use Cases:

Run Integration Tests:
  .ci build integration-tests

Check Test Status:
  .ci status integration-tests

View Recent Builds:
  .ci history integration-tests

Cancel Hanging Build:
  .ci cancel 12345

📚 Related Documentation:
• https://thehub.github.com/epd/engineering/products-and-services/internal/chatops/hubot/commands-reference/
• CI/CD section in thehub

💬 Practice First:
Try discovering available jobs in #learn-hubot:
  .ci list
  .ci help

Once you know the job names, run them in your team's channel.
```

## Agent Response - Step 5: Namespace Discovery

```
🔍 Want to Explore More Commands?

List All Available Namespaces:
  hubot rpc list

Get Help for Specific Namespace:
  hubot rpc help ci
  hubot rpc help deploy
  hubot rpc help instance

Common Namespaces:
• .ci - Continuous Integration (Janky)
• .deploy - Deployments (Heaven)
• .instance - Infrastructure
• .workflow - GitHub Actions
• .mysql - Database operations

Each namespace has its own set of commands!
```

## Key Points

- **Search first** - Use gh search to find commands
- **Multiple sources** - Check both guides and full reference
- **Show syntax** - Clear command structure
- **Examples** - Practical use cases
- **Discovery** - Teach how to find more commands
- **Practice** - Recommend safe environment
- **Context** - Explain when to use each command

## Variations

### Find Deployment Commands
```
User: "What are the deployment commands?"
Agent: Searches for .deploy namespace, shows deployment syntax
```

### Find MySQL Commands
```
User: "How do I query the database with chatops?"
Agent: 
  ⚠️  Security Warning - Database commands are sensitive
  Searches mysql-commands.md in thehub
  Shows commands with extra caution
```

### General Command Search
```
User: "What can hubot do?"
Agent:
  Shows .help command
  Lists major namespaces
  Points to hubot rpc list for exploration
```

## Search Strategies

### 1. Local Search (preferred)

If `github/thehub` is cloned locally, search the chatops docs directory directly with `grep` or read files with `cat`.

### 2. GitHub API Search (fallback)
```bash
gh search code "KEYWORD" --repo github/thehub --filename "*.md" --include-path "chatops"
```

### 3. Fetch Command Reference
```bash
gh api "repos/github/thehub/contents/docs/epd/engineering/products-and-services/internal/chatops/hubot/commands-reference.md" --jq '.content' | base64 -d
```

### 4. List All ChatOps Files
```bash
gh api 'repos/github/thehub/git/trees/main?recursive=1' --jq '.tree[].path' | grep -i chatops
```

## Response Template for Unknown Commands

```
🔍 Searching for: <user's query>

Found in namespace: <namespace>

📋 Command: <command name>

Syntax:
  <command syntax>

Description:
  <what it does>

Examples:
  <examples>

[Security/Access Notes if applicable]

📚 Documentation:
<link to thehub docs>

💬 Practice:
Test in #learn-hubot: <safe example>

💡 Need more commands?
• .help - General help
• hubot rpc list - List all namespaces
• hubot rpc help <namespace> - Namespace help
```

## When Command Not Found

```
🔍 I searched thehub but couldn't find a specific command for that.

Here's what you can try:

1. Explore Available Namespaces:
   hubot rpc list

2. Check General Help:
   .help

3. Search thehub Directly:
   Visit github.com/github/thehub and search for your topic

4. Ask in Slack:
   • #chat-ops - ChatOps help channel
   • #learn-hubot - Practice and questions

5. Browse Command Reference:
   https://thehub.github.com/epd/engineering/products-and-services/internal/chatops/hubot/commands-reference/

Would you like me to help you search for something specific?
```

## Related Examples

- **Deployment**: See [deployment-workflow.md](./deployment-workflow.md)
- **Sparkles**: See [sparkles.md](./sparkles.md)
- **Adding Hubot**: Reference the thehub guide for channel setup
