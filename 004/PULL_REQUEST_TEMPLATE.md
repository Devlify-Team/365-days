# Pull request: Git workflow best practices

> **Example only.** This file is a workbook template; it is not auto-installed and does not imply that repository protections or approvals are configured.

## What changed?

<!-- State the smallest useful summary and link the issue/task if one exists. -->

## Why?

<!-- Explain the workflow or behavior this change demonstrates. -->

## Evidence

- [ ] Staged diff reviewed with `git diff --cached`
- [ ] Read-only preflight run: `python3 004/check_workflow.py --repo .`
- [ ] Tests run: `python3 -B -m unittest discover -s 004 -p 'test_*.py' -v`
- [ ] Results or limitations:

## Review notes

- [ ] No unrelated files or secrets are included.
- [ ] Conflicts and staged whitespace errors are resolved.
- [ ] Branch is short-lived; shared `main`/`master` was not force-pushed.
- [ ] Reviewer feedback is addressed, or follow-up work is recorded.

## Merge note

Recommended protections (reviews, required checks, and no force-push) are hypothetical guidance for this workbook, not verified repository configuration. Merge only under the project’s actual policy.
