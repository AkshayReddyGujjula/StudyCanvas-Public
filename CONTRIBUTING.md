# Contributing

Thank you for taking the time to look through StudyCanvas.

This is a documentation-only engineering portfolio. The production application is developed in a private repository, so this project does not accept application-code pull requests.

## Useful contributions

Public issues and pull requests are welcome for:

- a broken local link or missing image
- an architecture section that is unclear
- a spelling, grammar or accessibility problem
- a question that a technical reviewer would reasonably expect the report to answer
- a correction where a public claim is inconsistent with the live product

Please do not submit copied production source, reverse-engineered prompts, credentials, invite codes or private user material.

## Style rules

Documentation in this repository should:

- use UK spelling
- use direct, specific language
- explain the constraint and trade-off, not only the chosen tool
- separate measured evidence from opinion
- include an as-at date for facts that will change
- avoid em dashes throughout
- avoid claims that files never leave the device, because explicit upload and AI actions can send relevant content for processing
- avoid describing Exam Forecast as a guaranteed prediction system

## Before opening a pull request

Run the documentation check:

```powershell
python scripts/check_docs.py
```

Then inspect the Markdown in GitHub's preview, especially Mermaid diagrams and image layout.

## Reporting security issues

Do not open a public issue for a vulnerability. Follow [SECURITY.md](SECURITY.md) instead.
