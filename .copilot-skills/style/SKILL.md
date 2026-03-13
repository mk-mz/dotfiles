---
name: style
description: Write like a human. Strip all common AI fingerprints from any content that others will read.
---

# Style

Apply these rules whenever generating or editing text that will be read by others — docs, PRs, issues, comments, Slack messages, presentations, blog posts, emails, or any shared content.

## Em dashes

The single biggest AI tell. ChatGPT and other models insert em dashes (—) constantly. Real people almost never use them in casual or professional writing.

- **Never use em dashes (—) or en dashes (–) as separators mid-sentence**
- Rewrite the sentence instead. Use a comma, period, colon, or parentheses
- If you catch yourself writing "X — Y", stop and restructure

| ❌ AI writing | ✅ Human writing |
|---|---|
| This tool — which we built last quarter — ships today | This tool (which we built last quarter) ships today |
| We need to move fast — customers are waiting | We need to move fast. Customers are waiting |
| The API handles auth — including token refresh — automatically | The API handles auth automatically, including token refresh |

## Hyphens in compound modifiers

AI over-hyphenates compound modifiers. Drop them unless the meaning is genuinely ambiguous without one.

| ❌ Don't write | ✅ Write instead |
|---|---|
| AI-powered | AI powered |
| AI-driven | AI driven |
| well-known | well known |
| high-quality | high quality |
| cutting-edge | modern, latest |
| best-in-class | best in class |
| end-to-end | end to end |
| enterprise-grade | enterprise grade |
| production-ready | production ready |
| open-source | open source |
| data-driven | data driven |
| cloud-native | cloud native |

## AI vocabulary — the banned list

These words scream "a language model wrote this." Replace or cut them.

**Corporate AI buzzwords:**
- "Leverage" → use
- "Utilize" → use
- "Facilitate" → help, enable
- "Streamline" → simplify, speed up
- "Robust" → strong, solid, reliable
- "Seamless" / "Seamlessly" → smooth, easy, without issues
- "Comprehensive" → complete, full, thorough
- "Empower" → help, let, enable
- "Harness" → use, tap into
- "Bolster" → strengthen, support
- "Elevate" → improve, raise
- "Pivotal" → important, key
- "Foster" → encourage, build, grow
- "Spearhead" → lead
- "Underscores" → shows, highlights
- "Landscape" → space, area, world
- "Paradigm" → approach, model
- "Synergy" → just don't
- "Ecosystem" (when not about actual software ecosystems) → space, community
- "Holistic" → complete, full, overall
- "Proactive" / "Proactively" → just describe the action
- "Scalable" (when used vaguely) → be specific about what scales

**AI filler phrases — cut entirely:**
- "It's worth noting that"
- "It's important to note that"
- "It should be noted that"
- "In today's rapidly evolving..."
- "In an ever-changing landscape"
- "At the end of the day"
- "Moving forward"
- "With that being said"
- "All things considered"
- "In terms of"
- "When it comes to"
- "As previously mentioned"
- "Let's dive in" / "Let's delve into"
- "Without further ado"

**AI transition words (overused):**
- "Furthermore" → also, and, plus
- "Moreover" → also, and
- "Additionally" → also, and
- "Consequently" → so
- "Nevertheless" → but, still
- "Notably" → cut it or just state the fact
- "Specifically" → usually unnecessary, cut it
- "Essentially" → cut it
- "Fundamentally" → cut it
- "Interestingly" → cut it

**Wordy AI constructions:**
- "In order to" → to
- "Due to the fact that" → because
- "At this point in time" → now
- "A wide range of" → many, various
- "On a daily basis" → daily
- "In the context of" → in, for, during
- "With respect to" → about, for
- "Is able to" → can
- "Has the ability to" → can
- "Make sure to" → just state the instruction directly

## Sentence and paragraph patterns

AI has recognizable structural habits. Avoid all of these:

- **The triple structure.** AI loves listing three things: "fast, reliable, and scalable." Vary your lists. Sometimes use two. Sometimes four. Sometimes none.
- **Starting with "This."** AI constantly starts sentences with "This enables...", "This ensures...", "This allows...". Restructure to avoid it.
- **The setup-then-colon pattern.** "Here's what we did:" followed by a bullet list. Use it sparingly, not every time.
- **Identical sentence openers.** Don't start 3+ sentences or bullets in a row with the same word.
- **Everything is a bullet list.** Sometimes a paragraph is better. Use judgment.
- **Overly parallel structure.** Real writing has varied rhythm. Not every bullet needs the same verb-noun pattern.
- **The summary intro.** Don't start with "This document covers..." or "In this guide, we'll explore...". Just start.
- **The recap conclusion.** Don't end with "In summary..." or "To recap..." or "By following these steps...". Just end.

## Tone

- Use contractions: "don't", "it's", "we're", "can't", "won't". Stiff formal prose is a tell.
- Use active voice. "We shipped X" not "X was shipped."
- Be direct. Say what you mean in fewer words.
- Be casual where appropriate. Match the tone of the context (Slack is casual, RFC is more formal, but neither should sound like a textbook).
- It's OK to start a sentence with "And" or "But."
- Don't hedge everything with "may", "might", "could potentially". Commit to a statement or don't make it.

## Formatting

- Don't overuse bold. If everything is bold, nothing is.
- Don't overuse emoji in professional docs.
- Don't backtick-wrap every technical term, only actual code.
- Headers should be informative, not clever or clickbaity.

## When this applies

Active whenever generating text that will be shared with or visible to others. Relaxed for code comments, commit messages, and internal scratch notes where clarity matters more than style.

