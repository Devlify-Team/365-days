# Day 10 — Find good first issues

**Tracker:** Day 10 · Month 1: Foundations & GitHub Basics
**Project:** Open Source
**Primary:** GitHub good-first-issue
**Alternative:** GitLab issues
**Suggested repository name:** `find-good-first-issues`

## Goal

Use the read-only Python CLI in [`find_issues.py`](./find_issues.py) to discover current GitHub Search API results for `good first issue`. The output is dynamic open-issue data, not a recommendation or a claim that any task is suitable, active, unassigned, or safe to undertake.

From the repository root, use Python 3.9 or newer. The finder uses only the standard library and needs an internet connection for its live, unauthenticated read-only query; the unit tests are offline and use a mocked response.

Run it with:

```bash
python3 -B 010/find_issues.py --language Python --limit 5
python3 -B 010/find_issues.py --repo owner/name
```

Run the mock-unit tests with:

```bash
python3 -B -m unittest discover -s 010/tests -p 'test_*.py' -v
```

Requests are unauthenticated and limited to 10 per minute according to the [GitHub Search API documentation](https://docs.github.com/en/rest/search/search). This project needs no secret, token, login, or credential.

## Review before considering a contribution

Labels are signals, not guarantees. Before investing time, check that the issue is still open, not a duplicate, recently active, unassigned (if that matters to the project), and not already covered by a pull request. Read the issue description and comments, then read the repository's `CONTRIBUTING` guide, Code of Conduct, license, environment setup, and relevant CI/tests. Confirm the reproduction or acceptance details and understand any skill, environment, privacy, security, or license risk. Do not use production data or run destructive experiments.

Clarify questions in the issue only when the project's policy expects it. Do not claim work, request assignment by default, or comment, assign, submit an issue or pull request, begin a checkout, or offer a contribution on someone else's behalf. The user decides whether to proceed or pass.

## References

- [GitHub label guidance](https://docs.github.com/en/communities/setting-up-your-project-for-healthy-contributions/encouraging-helpful-contributions-to-your-project-with-labels)
- [GitHub search issues and pull requests](https://docs.github.com/en/issues/tracking-your-work-with-issues/filtering-and-searching-issues-and-pull-requests)
- [GitHub `good-first-issue` topic](https://github.com/topics/good-first-issue)
- [goodfirstissue.dev](https://goodfirstissue.dev/)
- [GitLab contributor issue finder](https://contributors.gitlab.com/issues) — look for `quick win::first-time contributor`; read the issue, comment only as project policy directs, and follow its “assign me” then MR workflow if you later choose to participate.
- [GitLab contribution guide](https://docs.gitlab.com/development/contributing/) — starts with a tutorial and explains contribution workload.

Use the [issue evaluation template](./issue-evaluation-template.md) to record a candidate without implying that it is a recommendation or that any work has begun. Adding project notes requires no live legal or credential access.
