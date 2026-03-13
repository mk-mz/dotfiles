---
name: jargon-translation
description: This skill should be used when the user asks to "define this term", "what does X mean", "translate this jargon", "look up this acronym", "what is PRU", "define dialtone", "glossary lookup", or encounters unfamiliar GitHub-internal terminology, acronyms, or jargon.
---

# Jargon Translation - GitHub Glossary Lookup

Translates GitHub-internal jargon, acronyms, and terminology by looking them up in the [github/glossary](https://github.com/github/glossary) repository.

## When to Use This Skill

**Appropriate use cases:**
- User asks what a term or acronym means
- User encounters unfamiliar jargon in docs, Slack, or code
- User wants to look up multiple terms at once
- User is onboarding and needs quick definitions
- Agent encounters jargon it doesn't recognize in user-provided context

## Process

### Step 1: Identify Terms to Look Up

Detect jargon from the user's request:
- Explicit: "What does PRU mean?"
- Implicit: User provides text containing unknown acronyms
- Batch: "Define CAPI, AOAI, and CCA"

### Step 2: Search the Glossary

The `github/glossary` repo has this structure:
- `README.md` — Main glossary (largest, ~2000 lines, covers most terms)
- `actions/README.md` — GitHub Actions-specific terms
- `copilot/README.md` — Copilot-specific terms
- `codespaces/README.md` — Codespaces-specific terms
- `education/README.md` — Education-specific terms
- `product-development/README.md` — Product development terms
- `professional-services/README.md` — Professional services terms
- `archive.md` — Retired/archived terms

Each glossary entry follows this markdown format:
```markdown
* ### TERM
  * Definition text
```

Or with a link:
```markdown
* ### [TERM](https://link)
  * Definition text
```

**Search the main glossary first:**
```bash
gh api repos/github/glossary/contents/README.md --jq '.content' | base64 -d | grep -i -A 2 "### .*SEARCH_TERM"
```

**If not found, search domain-specific glossaries:**
```bash
for dir in actions copilot codespaces education product-development professional-services; do
  echo "=== $dir ==="
  gh api "repos/github/glossary/contents/$dir/README.md" --jq '.content' | base64 -d | grep -i -A 2 "### .*SEARCH_TERM"
done
```

**For broad searches (when the exact term is uncertain):**
```bash
gh api repos/github/glossary/contents/README.md --jq '.content' | base64 -d | grep -i -A 2 "SEARCH_TERM"
```

### Step 3: Format and Present Results

**Single term:**
```
📖 **PRU** — Premium Request Unit (i.e., Copilot Premium Requests)
   Source: [github/glossary](https://github.com/github/glossary/blob/master/README.md)
```

**Multiple terms:**
```
📖 Glossary Results:

| Term | Definition | Source |
|------|-----------|--------|
| PRU | Premium Request Unit (Copilot Premium Requests) | [main](https://github.com/github/glossary) |
| CAPI | Copilot API — the GitHub service that serves OpenAI ML endpoints | [copilot](https://github.com/github/glossary/tree/master/copilot) |
| CCA | Copilot Coding Agent | [main](https://github.com/github/glossary) |
```

**Term not found:**
```
❓ Term "XYZ" not found in github/glossary.

Suggestions:
• Check spelling or try alternative forms
• Search the glossary directly: https://github.com/github/glossary
• The term may be team-specific jargon not yet in the glossary
• Consider contributing it: https://github.com/github/glossary/blob/master/contributing.md
```

### Step 4: Provide Context When Relevant

If the term has a link in the glossary entry, include it:
```
📖 **dialtone** — Highest service tier. Services that are foundational to
   GitHub's uptime-guaranteed services.
   🔗 https://thehub.github.com/epd/engineering/fundamentals/service-tiers/
   Source: [github/glossary](https://github.com/github/glossary)
```

## Error Handling

### Repository Not Accessible
```bash
if ! gh api repos/github/glossary --silent 2>/dev/null; then
    echo "❌ Cannot access github/glossary repository"
    echo "Ensure you have access and are authenticated: gh auth status"
fi
```

### API Rate Limiting
If making many lookups, batch them by fetching the full glossary once:
```bash
# Fetch once, search locally
GLOSSARY=$(gh api repos/github/glossary/contents/README.md --jq '.content' | base64 -d)
echo "$GLOSSARY" | grep -i -A 2 "### .*TERM1"
echo "$GLOSSARY" | grep -i -A 2 "### .*TERM2"
```

### Term Ambiguity
Some terms appear in multiple glossaries with different meanings. When this happens:
- Present all definitions
- Note which glossary each comes from
- Let the user determine which is relevant to their context

## Other Glossaries

The main glossary README links to additional specialized glossaries hosted in other repos:

- [Accessibility Glossary](https://github.com/github/accessibility-audit-guide/blob/main/glossary.md)
- [Actions Glossary](https://github.com/github/c2c-actions/blob/main/docs/glossary.md)
- [CodeQL Glossary](https://github.com/github/codeql-core/blob/main/wiki/glossary.md)
- [Open Source Glossary](https://github.com/github/ecoss/blob/master/open-source-glossary.md)
- [GitHub's Public Documentation Glossary](https://help.github.com/en/articles/github-glossary)

If a term is not found in `github/glossary`, mention these as additional resources.

## Boundaries

**Will:**
- Look up terms in `github/glossary` and its subdirectories
- Handle single or batch term lookups
- Provide source links to glossary entries
- Suggest contributing missing terms
- Point to related specialized glossaries

**Will Not:**
- Define terms not in the glossary from memory (always check the source)
- Modify the glossary repository
- Access glossaries in other repos without user confirmation
- Guess at definitions for terms not found

## Quick Reference

```bash
# Look up a term in the main glossary
gh api repos/github/glossary/contents/README.md --jq '.content' | base64 -d | grep -i -A 2 "### .*TERM"

# Look up in copilot glossary
gh api repos/github/glossary/contents/copilot/README.md --jq '.content' | base64 -d | grep -i -A 2 "### .*TERM"

# Search all glossaries
for dir in . actions copilot codespaces education product-development professional-services; do
  file="README.md"; [ "$dir" = "." ] && path="$file" || path="$dir/$file"
  gh api "repos/github/glossary/contents/$path" --jq '.content' | base64 -d | grep -i -A 2 "### .*TERM" 2>/dev/null
done

# List all terms (main glossary)
gh api repos/github/glossary/contents/README.md --jq '.content' | base64 -d | grep "^\* ###" | sed 's/\* ### //'
```
