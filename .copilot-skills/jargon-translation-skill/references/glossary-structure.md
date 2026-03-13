# GitHub Glossary Repository Structure

Reference documentation for the [github/glossary](https://github.com/github/glossary) repository.

## Repository Layout

```
github/glossary/
├── README.md                      # Main glossary (~2000 lines, most terms)
├── archive.md                     # Retired/archived terms
├── contributing.md                # How to add new terms
├── actions/
│   └── README.md                  # GitHub Actions-specific terms (Azure, infrastructure)
├── codespaces/
│   └── README.md                  # Codespaces-specific terms
├── copilot/
│   └── README.md                  # Copilot-specific terms (AI, models, APIs)
├── education/
│   └── README.md                  # Education program terms
├── product-development/
│   └── README.md                  # Product development methodology terms
└── professional-services/
    └── README.md                  # Professional services terms
```

## Entry Format

Entries follow this markdown pattern:

```markdown
* ### TERM
  * Definition text
```

With optional link:

```markdown
* ### [TERM](https://link-to-more-info)
  * Definition text
```

## Related Glossaries (External)

The main glossary links to these additional glossaries in other repos:

| Glossary | Repository |
|----------|-----------|
| Accessibility | `github/accessibility-audit-guide` |
| Actions (C2C) | `github/c2c-actions` |
| Actions Framework | `github/c2c-actions` (framework manual) |
| Actions Service | `github/c2c-actions` (service terminology) |
| Azure DevOps | `github/c2c-actions` (ADO wiki) |
| CodeQL | `github/codeql-core` |
| Open Source | `github/ecoss` |
| Professional Services | `github/services` |
| Public Docs | `help.github.com/en/articles/github-glossary` |
| Help Docs | `github/help-docs` (data/glossaries) |

## ChatOps Integration

Glossary definitions can also be queried via [Glossary ChatOps](https://github.com/github/glossary-chatops) using `.glossary me <term>` in supported channels.

For copilot-specific terms, use `.glossary me copilot/<term>`.
