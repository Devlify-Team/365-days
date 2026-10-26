# Badge example README

This small example shows optional README badges for neutral, manually maintained metadata. The written description is the source of truth; badges are a compact supplement and may become stale.

## At a glance

[![Documentation format: Markdown](https://img.shields.io/badge/docs-Markdown-blue)](https://www.markdownguide.org/basic-syntax/)
![Runtime dependencies: none](https://badgen.net/badge/dependencies/none/green)
![Workbook area: Month 1 foundations](https://img.shields.io/badge/workbook-Month%201%20foundations-informational)

This example is a Markdown README in the Day 008 workbook. It uses no third-party runtime dependencies. The badges above are neutral documentation metadata selected for this example; they do not report tests, builds, deployment, releases, licensing, readiness, uptime, privacy, or any service-level agreement.

## Why the badges are optional

A reader should understand this example from the sentences above even if badge images fail to load, the badge provider changes, or the badges are removed. Keep useful prose and written alternatives. Add a badge only when its meaning is clear, its value is maintained, and its accessibility cost is acceptable.

## Static badge URL pattern

The primary service is [Shields.io](https://shields.io/). Its [Static Badge documentation](https://shields.io/badges/static-badge) describes a URL path shaped like `label-message-color` (with an optional label). For example:

```text
https://img.shields.io/badge/docs-Markdown-blue
```

Spaces may be encoded as `_` or `%20`; other special characters may need URL encoding. The backup service is [Badgen.net](https://badgen.net/).

## Optional link markup

A badge may be wrapped in a link when the destination gives useful context. The first badge above links to a Markdown syntax reference. The link is optional, and the alt text still needs to explain what the image communicates:

```markdown
[![Documentation format: Markdown](https://img.shields.io/badge/docs-Markdown-blue)](https://www.markdownguide.org/basic-syntax/)
```

## Workflow badge syntax (future documentation only)

The [Shields.io GitHub Actions Workflow Status documentation](https://shields.io/badges/git-hub-actions-workflow-status) describes badges using an owner, repository, and workflow filename. This workbook example has no workflow, so the following is intentionally a **fenced placeholder**, not an active badge:

```markdown
![Latest workflow result](https://github.com/<owner>/<repo>/actions/workflows/<workflow>.yml/badge.svg)
```

Do not publish this placeholder as an image. Do not invent a workflow or a test, build, deployment, release, license, or readiness indicator. Replace every placeholder only after a real workflow and repository have been verified.

## Limitations

The Day 008 checker is a local static markup check. It checks recognized badge hosts, absolute HTTP(S) image URLs, missing or very generic alt text, and unresolved owner/repository placeholders in active markup. It ignores fenced examples like the workflow syntax above.

A passing check cannot verify the truth or freshness of a badge claim, render its colors, assess the full reader experience, validate remote responses, inspect workflow history, or make any request to a remote service. Review badges manually and remove stale ones. No badge here promises provider availability, privacy, uptime, or an SLA.

## Run from the repository root

Audit this README:

```bash
python3 -B 008/badge_audit.py 008/examples/README-with-badges.md
```

Run the Day 008 tests:

```bash
python3 -B -m unittest discover -s 008/tests -p 'test_*.py' -v
```
