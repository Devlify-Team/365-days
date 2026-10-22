# 004 — Git workflow best practices

**365 Days GitHub Challenge · Version Control · Month 1: Foundations & GitHub Basics**

- **Workbook source:** `365_Days_GitHub_Challenge_Tracker.xlsx`, sheet `All Projects`, Day 4
- **Primary GitHub topic:** `git-workflow`
- **Backup topic:** Trunk-based development
- **Suggested repository:** `git-workflow-best-practices`

## Goal

Practice a small, reviewable Git change: inspect the working tree, review the staged diff, run scoped tests, make an explicit commit, open a pull request, respond to review, and merge safely. Keep branches short-lived; avoid force-pushing a shared `main` branch. Trunk-based development is the fallback model: integrate small changes to the trunk frequently, using short-lived branches when review or CI requires them.

## Day 4 preflight CLI

`check_workflow.py` is a **read-only** staged-change preflight. It does not validate tests, secrets, PR approvals, or repository policy. It does not mutate files or configuration, and it never stages, commits, or pushes.

```text
python3 004/check_workflow.py --repo .
python3 004/check_workflow.py --repo . --json
```

- Requires **Python 3.9+** and **Git**; no third-party dependencies.
- `--repo PATH` defaults to `.`. `--json` emits machine-readable output.
- Checks: staged changes exist; unresolved conflicts; `git diff --cached --check` whitespace errors and conflict markers.
- Exit `0`: no blocking issues. Exit `1`: blocking issues. Exit `2`: invocation or Git error.
- `main`, `master`, and detached `HEAD` are **warnings only**, not blockers.

## Suggested flow

```text
git status --short
git diff
git switch -c <short-branch>
# edit only the scoped files
git diff --check
git add <intentional-files>
git diff --cached
python3 004/check_workflow.py --repo .
python3 -B -m unittest discover -s 004 -p 'test_*.py' -v
git commit -m "feat: describe the focused change"
git push -u origin <short-branch>
# open a PR, request review, address feedback, merge, then delete the branch
git switch main
git pull --ff-only
```

Review staged content—not just the file list—before committing. If the preflight reports conflicts or whitespace errors, fix them, restage, and rerun it. A clean preflight is not proof that tests pass or that a PR is approved.

## Protection guidance (not repository configuration)

A team might **recommend** protected `main`/`master`, required reviews and status checks, linear history, no force-push, and automatic branch deletion. Those are hypothetical best practices for this workbook. **This project changes none of them and makes no claim about the actual repository configuration.** The templates below are examples only; they are not auto-installed.

## Tests

```text
python3 -B -m unittest discover -s 004 -p 'test_*.py' -v
```

Run the focused tests after reviewing the staged diff and before opening the PR. Record any limitations in the PR description.

**Delivered validation:** All seven integration tests passed in disposable repositories, covering ready/unstaged states, whitespace, real merge conflicts, default/detached branch warnings, JSON/exit codes, inherited Git environment isolation, and unchanged index/HEAD during inspection.

## Manual verification checklist

- [ ] `git status --short` is understood; unrelated edits remain unstaged.
- [ ] The branch is short-lived and is not shared `main`/`master`.
- [ ] `git diff --cached` contains only the intended change.
- [ ] `check_workflow.py` returns exit `0` with no blocking issue.
- [ ] Conflict markers and staged whitespace errors are absent.
- [ ] The scoped unittest command passes, or failures are documented.
- [ ] Commit subject is clear and the commit contains no secrets.
- [ ] PR explains intent, evidence, and review/testing limits.
- [ ] Review feedback is addressed; merge uses the team’s approved policy.
- [ ] No force-push is used on shared trunk; local branch is cleaned up afterward.

## Source map

- **Workbook:** `365_Days_GitHub_Challenge_Tracker.xlsx` → `All Projects` → Day 4
- **Official GitHub flow:** [GitHub flow](https://docs.github.com/en/get-started/using-github/github-flow)
- **Official Git reference:** [`git diff`](https://git-scm.com/docs/git-diff)
- **Project files:** [check_workflow.py](check_workflow.py), [test_workflow.py](test_workflow.py), [PULL_REQUEST_TEMPLATE.md](PULL_REQUEST_TEMPLATE.md), and [COMMIT_MESSAGE_TEMPLATE.txt](COMMIT_MESSAGE_TEMPLATE.txt).

This exercise stays inside `Devlify-Team/365-days/004/`, adds no production configuration changes, and creates no schedule or automation.
