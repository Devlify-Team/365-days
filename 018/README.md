# Day 18 — Code review best practices

**365 Days GitHub Challenge · Collaboration · Month 1: Foundations & GitHub Basics**

- **Primary GitHub topic:** `code-review`
- **Alternative:** GitLab code review
- **Slug:** `code-review-best-practices`

## Goal

Learn how to inspect a change carefully and write review notes that help an author act. Day 017 covered the pull-request review/revision lifecycle; Day 018 focuses on the inspection itself: understanding design and intent, reading changed lines in context, finding correctness and edge-case risks, and communicating evidence-based feedback without perfectionism.

GitHub's review flow supports examining files one by one and then submitting **Approve** or **Request changes** (along with comments): [GitHub — Reviewing proposed changes in a pull request](https://docs.github.com/en/pull-requests/how-tos/review-pull-requests/reviewing-proposed-changes-in-a-pull-request). On GitLab, reviews support comments, suggestions, and decisions, while project configuration determines approval and merge-blocking requirements: [GitLab — Merge request reviews](https://docs.gitlab.com/user/project/merge_requests/reviews/).

## What to inspect

Use [`review-checklist.md`](review-checklist.md) as a thinking aid, not as a demand that every change be perfect. Follow repository-specific rules, conventions, and review scope first.

1. **Understand the intent.** Read the description and linked issue, identify the intended behavior, and check that the change belongs in the component. If intent is unclear, ask a question before treating an assumption as a defect.
2. **Read the diff in context.** Inspect the full diff one file at a time, then open surrounding code, callers, data flow, and relevant configuration when the changed lines alone do not explain behavior. Google’s reviewer standard emphasizes design, context, and reviewing every assigned line: [Google — The Standard of Code Review](https://google.github.io/eng-practices/review/reviewer/standard.html).
3. **Check correctness and boundaries.** Consider normal behavior plus empty, invalid, unusually large, failure, and concurrent inputs when relevant. Ask whether the implementation actually solves the stated problem and whether error handling is safe.
4. **Check maintainability.** Look at complexity, names, comments, documentation, style, and whether the tests cover changed behavior and meaningful edge cases. Prefer a simpler, understandable solution over speculative generality. Google’s review guidance summarizes these dimensions and what to look for: [Google — What to look for in a code review](https://google.github.io/eng-practices/review/reviewer/looking-for.html).
5. **Check sensitive risk in scope.** Consider security, privacy, permissions, trust boundaries, secrets, user-visible effects, generated files, and risky operations when the change touches them. Consider parallelism or concurrency when it can affect correctness; do not invent out-of-scope audits.
6. **Separate signal from preference.** Distinguish an objective correctness, safety, or requirement blocker from a non-blocking suggestion, nit, or personal style preference. Google specifically recommends distinguishing nits and personal preferences; do not block sound work over taste.
7. **Write actionable notes.** Point to observable behavior, explain the impact, and give a practical next step or question. Use evidence from the code, diff, tests, or requirements. Include positive notes where useful, and state what you did not review or could not verify.

## Practice exercise

1. Read [`review-checklist.md`](review-checklist.md) and choose a small, real or imagined diff.
2. Inspect the change one file at a time. Read changed lines in surrounding context and record the files, behavior, and checks you actually examined.
3. Look for design and functionality problems, edge cases, unnecessary complexity, weak tests, unclear names/comments/docs, and security, privacy, or parallelism concerns where relevant.
4. Fill in [`review-note-template.md`](review-note-template.md). Use **Approve**, **Comment**, or **Request changes** according to the repository's actual policy. For a finding, include its impact and a suggested action. If there are no actionable issues, write exactly `No findings.` in Findings.
5. Add an explicit unreviewed scope, such as deployment, performance, or an area outside your expertise. Do not imply that a green local check proves correctness or merge eligibility.
6. Rewrite comments until they are respectful, specific, evidence-based, and actionable. Keep optional polish separate from blockers, and include a useful positive observation when appropriate.

## Offline validation

From the repository root, the starter template intentionally fails until its TODOs are replaced:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -B 018/check_review.py 018/review-note-template.md
```

That command intentionally returns exit `1` for the starter. After completing a reviewer note, the checker returns `0` when the required structure and finding blocks are valid, `1` when it finds issues, and `2` when the input cannot be read:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -B 018/check_review.py /path/to/completed-review-note.md
```

Run the six standard-library unit tests with:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -B -m unittest discover -s 018/tests -p 'test_*.py' -v
```

`check_review.py` is offline, read-only, and standard-library only. It checks Markdown structure, decisions, placeholders, and finding blocks; it does not analyze code, verify correctness, inspect evidence, run the project's tests, check approvals or merge requirements, or access GitHub/GitLab. It never submits a review. No review was posted. Keep required final reviewer notes under `018/`. The template is local to this exercise and is not installed to the repository.

## Exact file tree

```text
018/
├── .gitignore
├── README.md
├── check_review.py
├── review-checklist.md
├── review-note-template.md
└── tests/
    └── test_check_review.py
```

## Primary sources

- [GitHub — Reviewing proposed changes in a pull request](https://docs.github.com/en/pull-requests/how-tos/review-pull-requests/reviewing-proposed-changes-in-a-pull-request)
- [Google — The Standard of Code Review](https://google.github.io/eng-practices/review/reviewer/standard.html)
- [Google — What to look for in a code review](https://google.github.io/eng-practices/review/reviewer/looking-for.html)
- [GitLab — Merge request reviews](https://docs.gitlab.com/user/project/merge_requests/reviews/)

This exercise documents review practice and performs local structural validation only. It does not post or submit a GitHub/GitLab review.
