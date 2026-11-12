# Contribute to documentation

- **Day:** 025
- **Month:** 1 — Foundations & GitHub Basics
- **Category:** Community
- **Primary GitHub:** `doc-contributions`
- **Alternative:** Wiki contributions
- **Slug:** `contribute-to-documentation`

A practical kit for making a small, reviewable documentation contribution. It includes a contributor workflow, plain-language style guide, issue and pull-request templates, a Markdown checker for common structural problems, and tests. It is a learning lab; it does not submit changes to another repository.

## What's included

- `CONTRIBUTING.md` — find project-specific rules, make a focused change, validate it, and ask for review.
- `DOC_STYLE_GUIDE.md` — quick checks for audience, structure, examples, links, and accessibility.
- `templates/` — reusable issue and pull-request outlines.
- `docs/CONTRIBUTION_EXERCISE.md` — a small sample page to edit and check.
- `scripts/check_markdown.py` — a dependency-free checker for one top-level heading, closed fenced code blocks, and existing relative link targets.
- `tests/` — standard-library unit tests for valid and invalid Markdown.

## Try the contribution workflow

From this folder, inspect `docs/CONTRIBUTION_EXERCISE.md`, make a small clarity or link improvement, then run:

```bash
python3 scripts/check_markdown.py docs/
python3 -m unittest discover -s tests -v
```

The checker verifies local structure only. It does not fetch external links, spell-check, render every Markdown extension, or judge whether instructions are accurate; review and preview the change in the target project before opening a pull request. Read that repository's contribution rules first, and ask maintainers before taking on broad or unclaimed work.

## References

The workflow reflects GitHub's [guidance for contributing to GitHub Docs](https://docs.github.com/en/contributing/collaborating-on-github-docs/about-contributing-to-github-docs), including checking issue status and reviewing a content change before requesting review. GitHub also explains how to make [contribution guidelines discoverable](https://docs.github.com/en/communities/setting-up-your-project-for-healthy-contributions/setting-guidelines-for-repository-contributors) and provides a [style guide](https://docs.github.com/en/contributing/style-guide-and-content-model/style-guide). For a general fork-and-branch walkthrough, see [Contributing to open source](https://docs.github.com/en/get-started/exploring-projects-on-github/contributing-to-open-source).
