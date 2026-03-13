# Example: Giving Sparkles

Help users recognize team members using the sparkles system.

## Scenario

A developer wants to thank a colleague for a great code review and give them sparkles.

## User Request

> "How do I give @octocat sparkles for an awesome code review?"

## Agent Response - Step 1: Explain Sparkles

```
Great! Sparkles ✨ are GitHub's way of recognizing and appreciating teammates.
Let me show you how to give sparkles.

📋 Sparkles System:
• Recognize contributions and help
• Build team morale
• Track recognition via leaderboard
• Can include a reason (highly encouraged!)
```

## Agent Response - Step 2: Fetch Sparkles Commands

The agent checks if `github/thehub` is cloned locally. If found, it searches the commands reference directly. Otherwise, it falls back to the GitHub API:

```bash
# Fallback: fetch via GitHub API
gh api "repos/github/thehub/contents/docs/epd/engineering/products-and-services/internal/chatops/hubot/commands-reference.md" --jq '.content' | base64 -d | grep -i -A 10 "sparkle"
```

## Agent Response - Step 3: Show Sparkle Commands

```
📋 ChatOps Command: Sparkle

Syntax:
  .sparkle @username
  .sparkle @username for [reason]
  .sparkle leaderboard

Examples:
  .sparkle @octocat
  .sparkle @octocat for excellent code review
  .sparkle @octocat for "helping me debug that tricky issue"

💡 Pro Tips:
• Including a reason makes sparkles more meaningful
• Use quotes for multi-word reasons
• Sparkles appear in Slack and on the leaderboard
• Everyone loves recognition!

✨ For your case:
  .sparkle @octocat for excellent code review

Or be more specific:
  .sparkle @octocat for "thorough code review that caught critical bugs"
```

## Agent Response - Step 4: Additional Sparkle Features

```
📊 Other Sparkle Commands:

View Leaderboard:
  .sparkle leaderboard

See Who's Sparkling:
  .sparkle stats

Your Sparkles:
  .sparkle me

🎯 When to Give Sparkles:
• Great code reviews
• Helping with debugging
• Excellent documentation
• Going above and beyond
• Being a great teammate
• Sharing knowledge
• Fixing production issues
• Any positive contribution!

💬 Practice in #learn-hubot:
Try the command first to get comfortable:
  .sparkle @hubot for being helpful
```

## Success Response

```
Perfect! Here's what will happen:

1. Run this command in any Slack channel where Hubot is present:
   .sparkle @octocat for excellent code review

2. Hubot will confirm the sparkle:
   "✨ @octocat got a sparkle from @you for excellent code review"

3. @octocat will be notified

4. The sparkle will appear on the leaderboard

Want to see the leaderboard? Run:
  .sparkle leaderboard
```

## Key Points

- **Include reasons** - Makes sparkles more meaningful
- **Be specific** - Explain what they did well
- **Use quotes** - For multi-word reasons
- **Encourage use** - Sparkles boost morale
- **Show features** - Leaderboard, stats, etc.
- **Low barrier** - Easy command, high impact

## Variations

### Simple Sparkle
```
User: "Give someone sparkles"
Agent: ".sparkle @username"
```

### Sparkle with Detailed Reason
```
User: "I want to thank Sarah for fixing the production bug"
Agent: ".sparkle @sarah for quickly fixing the production bug that was affecting customers"
```

### View Leaderboard
```
User: "Who has the most sparkles?"
Agent: ".sparkle leaderboard"
```

### Check Your Sparkles
```
User: "How many sparkles do I have?"
Agent: ".sparkle me"
```

## Related Commands

- `.sparkle @username` - Give sparkles
- `.sparkle @username for [reason]` - Give sparkles with reason
- `.sparkle leaderboard` - View sparkle leaderboard
- `.sparkle stats` - View sparkle statistics
- `.sparkle me` - See your own sparkles

## Cultural Notes

**Sparkles Culture at GitHub:**
- Widely used for recognition
- Encourages positive team interactions
- Everyone can give sparkles
- No limit on how many you can give
- Visible and celebrated
- Part of GitHub's appreciation culture

**Best Practices:**
- Give sparkles generously
- Be genuine and specific
- Don't wait for "big" things - small helps count too
- Use it to build team culture
- Check the leaderboard regularly
- Celebrate others' recognition

## Documentation Reference

For more details on sparkles:
- `docs/epd/engineering/products-and-services/internal/chatops/hubot/sparkles-internal.md`
- `docs/guides/hubot.md` - Sparkles section

Practice in: `#learn-hubot`
