# Day 008: Add Badges and Shields

This workbook entry demonstrates how to add small, accessible status or metadata badges to a project README without letting decorative indicators replace useful documentation.

## Overview

Day 008 belongs to **Month 1: Foundations & GitHub Basics** and the **Documentation** theme. The suggested project name is `add-badges-and-shields`. The primary badge service is [Shields.io](https://shields.io/); [Badgen.net](https://badgen.net/) is a backup option.

Badges are optional. They can summarize stable, useful metadata, but they can also become stale or be misunderstood. Keep the core README sentences, headings, and written alternatives even when a badge is present. Do not add a badge merely because an image looks polished.

### Workbook metadata

- **Day:** 008
- **Theme:** Documentation
- **Month:** 1 — Foundations & GitHub Basics
- **Workbook source path:** `008/`
- **Suggested repository name:** `add-badges-and-shields`
- **Primary source:** [Shields.io Static Badge](https://shields.io/badges/static-badge)
- **Workflow source:** [Shields.io GitHub Actions Workflow Status](https://shields.io/badges/git-hub-actions-workflow-status)
- **Backup badge service:** [Badgen.net](https://badgen.net/)

## Learning goals

By the end of this exercise, you should be able to:

1. Decide whether a badge adds information that the README does not already communicate well.
2. Create a static Shields badge with a truthful label, message, and color.
3. Give each badge informative alternative text that makes sense without images.
4. Distinguish a real workflow status badge from a documented future placeholder.
5. Explain why badges need maintenance and why they never replace prose, tests, or release documentation.

## What is demonstrated

The [sample README](examples/README-with-badges.md) demonstrates:

- static Shields.io badges for neutral, manually maintained metadata;
- a Badgen.net alternative;
- accessible alt text that states what each badge communicates;
- optional link markup around a badge;
- the URL shape for a real GitHub Actions workflow badge, shown only in a fenced Markdown example because this repository has no such workflow; and
- written text that remains meaningful if badges fail to load or are removed.

The sample deliberately does **not** claim tests, builds, deployment, licensing, releases, production readiness, uptime, privacy, or a service-level agreement. Never invent an indicator for an unknown workflow or unsupported fact.

## Static Shields URL format

The [official static badge documentation](https://shields.io/badges/static-badge) defines a path containing `label-message-color`, with the label optional. Spaces can be represented by `_` or `%20`; special characters may need URL encoding. For example:

```text
https://img.shields.io/badge/docs-Markdown-blue
```

That URL says only that the author chose the label `docs`, message `Markdown`, and color `blue`; it does not verify an external fact. Pick a value you can maintain, use a color with adequate contrast, and write an alt label that explains the badge's meaning rather than saying only “badge” or “image.”

A badge can be linked when the destination provides useful context, for example:

```markdown
[![Documentation format: Markdown](https://img.shields.io/badge/docs-Markdown-blue)](https://www.markdownguide.org/basic-syntax/)
```

Linking is optional. A link should lead somewhere relevant; a badge does not need a click target just for decoration.

## Workflow badges: document the pattern, do not fake the result

The [official GitHub Actions workflow status documentation](https://shields.io/badges/git-hub-actions-workflow-status) uses an owner, repository, and workflow filename. A real example must identify an existing workflow and repository, such as `https://github.com/OWNER/REPO/actions/workflows/WORKFLOW.yml/badge.svg` after replacing every placeholder with verified values.

This exercise has no workflow to report. Therefore, the sample keeps the following syntax inside a fenced Markdown block so it is documentation, not a live unknown badge:

```markdown
![Latest workflow result](https://github.com/<owner>/<repo>/actions/workflows/<workflow>.yml/badge.svg)
```

Do not publish that placeholder as an active image, and do not replace it with an invented workflow, build, test, deployment, or readiness claim. Add a live workflow badge only after the workflow exists and its scope and maintenance owner are clear.

## Getting started

All commands below run from the repository root. Python 3.9+ and the standard library are sufficient.

Inspect the example and checker:

```bash
sed -n '1,240p' 008/examples/README-with-badges.md
```

Run the local checker against the sample:

```bash
python3 -B 008/badge_audit.py 008/examples/README-with-badges.md
```

Run the Day 008 tests:

```bash
python3 -B -m unittest discover -s 008/tests -p 'test_*.py' -v
```

The local links for this exercise are [the sample README](examples/README-with-badges.md), [the static checker](badge_audit.py), and the [Day 008 tests](tests/).

## Audit scope and limitations

The checker is intentionally safe and static. It recognizes badge image markup hosted on Shields.io, Badgen.net, or a GitHub Actions workflow badge URL; checks for absolute HTTP(S) URLs; flags empty or very generic alt text; and flags owner/repository placeholders in active image markup. It ignores image examples inside fenced code blocks, which is why the workflow syntax above can be documented safely.

A passing audit does **not** establish badge veracity, accessibility of the rendered colors, correctness of the linked destination, or whether a remote service is available. It does not render Markdown, make remote requests, validate URL responses, inspect workflow history, prove that a claim is current, or replace human proofreading and screen-reader review. Badges may get stale; review or remove them when the underlying metadata changes. The audit also does not promise service availability, privacy, uptime, or any SLA.

## Practical checklist

Before adding a badge, confirm that:

- the badge communicates a truthful, maintained fact or clearly labeled neutral metadata;
- the surrounding prose explains the same idea in words;
- alt text is informative for someone who cannot see the image;
- a link is present only when it provides useful context;
- no unknown workflow, build, test, deployment, license, release, or readiness status is implied;
- the image URL is absolute and contains no unresolved placeholders; and
- the badge can be removed without making the README's instructions incomplete.

## Source notes

The URL construction guidance and parameter examples come from [Shields.io Static Badge](https://shields.io/badges/static-badge). The workflow path and required `user`, `repo`, and `workflow` parameters come from [Shields.io GitHub Actions Workflow Status](https://shields.io/badges/git-hub-actions-workflow-status). [Badgen.net](https://badgen.net/) is listed only as a backup service; this workbook does not treat either service as a guarantee of uptime or correctness.
