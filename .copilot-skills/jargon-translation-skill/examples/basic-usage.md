# Example: Jargon Translation

## Scenario 1: Single Term Lookup

### User Request
> "What does PRU mean?"

### Agent Response
```
Looking up "PRU" in github/glossary...

📖 **PRU** — Premium Request Unit (i.e., Copilot Premium Requests)
   🔗 https://docs.github.com/en/copilot/concepts/copilot-billing/understanding-and-managing-requests-in-copilot
   Source: github/glossary (main)
```

### Outcome
User gets a quick, sourced definition without leaving their workflow.

---

## Scenario 2: Multiple Terms

### User Request
> "I keep seeing these acronyms — what do CAPI, AOAI, and CCA mean?"

### Agent Response
```
Looking up 3 terms in github/glossary...

📖 Glossary Results:

| Term | Definition | Source |
|------|-----------|--------|
| CAPI | Copilot API — the GitHub service that serves OpenAI ML endpoints to GitHub Copilot projects | copilot glossary |
| AOAI | Azure OpenAI — OpenAI's code run by Microsoft on Azure | copilot glossary |
| CCA | Copilot Coding Agent | main glossary |

🔗 Full glossary: https://github.com/github/glossary
```

### Outcome
User gets all three definitions in a scannable table format.

---

## Scenario 3: Term with Context

### User Request
> "Someone said our service needs to be dialtone — what does that mean?"

### Agent Response
```
Looking up "dialtone" in github/glossary...

📖 **dialtone** — Highest service tier. Services that are foundational to
   GitHub's uptime-guaranteed services.
   🔗 https://thehub.github.com/epd/engineering/fundamentals/service-tiers/
   Source: github/glossary (main)

In context: They're saying your service needs to meet GitHub's highest
reliability standards — the same tier as core GitHub.com functionality.
```

### Outcome
User gets both the definition and contextual interpretation.

---

## Scenario 4: Term Not Found

### User Request
> "What does YOLO mean in our codebase?"

### Agent Response
```
Looking up "YOLO" in github/glossary...

❓ Term "YOLO" not found in github/glossary.

Suggestions:
• Check if it's team-specific jargon
• Search the glossary directly: https://github.com/github/glossary
• Consider contributing the definition: https://github.com/github/glossary/blob/master/contributing.md
• Other glossaries to check:
  - GitHub Public Glossary: https://help.github.com/en/articles/github-glossary
```

### Outcome
User knows the term isn't in the official glossary and gets pointers for next steps.

---

## Scenario 5: Domain-Specific Lookup

### User Request
> "What's a devcontainer?"

### Agent Response
```
Looking up "devcontainer" in github/glossary...

📖 **devcontainer** — A devcontainer.json file in your project tells
   Codespaces how to access (or create) a development container with a
   well-defined tool and runtime stack.
   Source: github/glossary (codespaces)

🔗 Full Codespaces glossary: https://github.com/github/glossary/tree/master/codespaces
```

### Outcome
The skill found the term in the domain-specific Codespaces glossary.
