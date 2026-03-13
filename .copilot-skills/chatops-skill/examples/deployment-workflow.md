# Example: Deployment Workflow

Guide a user through deploying an application using ChatOps.

## Scenario

A developer needs to deploy a hotfix to production and wants to use ChatOps to do it safely.

## User Request

> "I need to deploy a hotfix to production. How do I do this with chatops?"

## Agent Response - Step 1: Explain Deployment Process

```
I'll help you deploy using ChatOps. Here's the deployment workflow:

⚠️  PRODUCTION DEPLOYMENT WARNING
Deploying to production requires careful attention. Let's go through this step-by-step.

📋 Prerequisites:
• Ensure you have deployment access
• Verify the change is ready (tests passing, reviewed)
• Check for any active deployment locks
• Have rollback plan ready
```

## Agent Response - Step 2: Fetch Command Reference

The agent checks if `github/thehub` is cloned locally. If found, it searches the commands reference directly. Otherwise, it falls back to the GitHub API:

```bash
# Fallback: fetch via GitHub API
gh api "repos/github/thehub/contents/docs/epd/engineering/products-and-services/internal/chatops/hubot/commands-reference.md" --jq '.content' | base64 -d | grep -i -A 5 "deploy"
```

## Agent Response - Step 3: Provide Deployment Command

```
📋 ChatOps Command: Deploy

Syntax:
  .deploy <application> to <environment>
  .deploy <application> to <environment> with <options>

Common Applications:
  • github - Main GitHub application
  • api - GitHub API
  • pages - GitHub Pages
  • actions - GitHub Actions

Common Environments:
  • production
  • staging
  • canary

Examples:
  .deploy github to production
  .deploy api to staging
  .deploy github to production with migrations

⚠️  Security Note:
Production deployments are high-risk operations. Always:
• Double-check the application and environment names
• Verify no one else is deploying
• Have a rollback plan ready
• Monitor the deployment closely

📝 Practice First:
Before deploying to production, test the command in #learn-hubot:
  .deploy help

📚 Documentation:
See: https://thehub.github.com/epd/engineering/products-and-services/internal/chatops/hubot/commands-reference/
```

## Agent Response - Step 4: Pre-Deployment Checks

```
Before you deploy, let's check a few things:

1. Verify no deployment locks:
   Run: .deploy locks

2. Check current deployment status:
   Run: .deploy status github

3. Review recent deployments:
   Run: .deploy history github production

Once you've verified everything looks good, you can run:
  .deploy github to production
```

## Agent Response - Step 5: Post-Deployment

```
After deploying:

✅ Monitor Progress:
• Watch the deployment in the chat channel
• Check for any error messages
• Verify success confirmation from Hubot

✅ Verify Deployment:
• Check application metrics
• Test key functionality
• Monitor error rates

✅ If Something Goes Wrong:
• Run: .deploy rollback github production
• Alert the team in relevant channels
• Document the issue

Need help with rollback? Ask me: "How do I rollback a deployment?"
```

## Key Points

- **Safety first** - Emphasize production deployment risks
- **Step-by-step** - Break down the process into manageable steps
- **Pre-checks** - Encourage verification before deploying
- **Clear syntax** - Show exact command format with examples
- **Documentation links** - Point to authoritative sources
- **Practice environment** - Recommend testing in `#learn-hubot`
- **Post-deployment** - Guide on monitoring and troubleshooting

## Variations

### Staging Deployment
```
User: "How do I deploy to staging?"
Agent: "Here's the staging deployment command..."
  .deploy github to staging
  (Less security warnings, focus on testing)
```

### Deployment with Options
```
User: "I need to deploy with migrations"
Agent: "Add options to your deploy command..."
  .deploy github to production with migrations
```

### Check Deployment Status
```
User: "How do I check if a deployment is running?"
Agent: "Use the status command..."
  .deploy status github
  .deploy locks
```

## Related Commands

- `.deploy locks` - Check for active deployment locks
- `.deploy status <app>` - Check deployment status
- `.deploy history <app> <env>` - View deployment history
- `.deploy rollback <app> <env>` - Rollback a deployment
- `.deploy help` - Get deployment help
