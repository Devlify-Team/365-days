# Day 17 — Learn pull request workflow

**365 Days GitHub Challenge · Collaboration · Month 1: Foundations & GitHub Basics**

- **Primary GitHub topic:** `pull-requests`
- **Alternative:** GitLab merge requests
- **Slug:** `learn-pull-request-workflow`

## Goal

Learn the full review-and-revision lifecycle of a pull request (PR), rather than only how to open one. You will prepare a meaningful change summary, distinguish a **draft** from a **ready for review** PR, give actionable review feedback, respond to comments with evidence, request re-review, and merge only when the project’s checks and approval rules permit it. GitLab calls the equivalent collaboration object a **merge request (MR)** and provides the same broad lifecycle: open as draft, review discussions, revise, re-review, and merge.

Day 004 already covers general Git workflow best practices and a generic PR template. Day 017 focuses specifically on the conversation and decision loop between author and reviewers.

## Learning steps

1. **Prepare the change and its context.** Keep the branch focused and the diff small enough to review. Before opening the PR, know the problem, intended outcome, validation performed, and known risks. Do not describe work as complete when important evidence is still missing.
2. **Write a useful description.** Explain what changed and why, identify the validation actually run, call out limitations, and tell reviewers where attention is most useful. A summary should help a reviewer understand the change without reconstructing the entire issue from the diff.
3. **Use draft status honestly.** Open as a draft while the change is still being shaped or when you want early, non-final feedback. Convert it to ready for review only when the description and diff are reviewable and you are asking for a formal review. A ready PR is a request for review, not a claim that the change is automatically safe to merge.
4. **Review for action, not preference.** Anchor comments to a file, line, behavior, or requirement. Explain the impact, state the requested change, and distinguish blockers from non-blocking suggestions. Ask a question when the intent is unclear; do not present an unverified assumption as a defect.
5. **Respond and revise.** Reply to each substantive comment with what you changed, why you chose that approach, or why no change is needed. Push a focused revision, update the description when scope or evidence changes, and rerun relevant checks. Keep the discussion readable so a later reviewer can follow the decision.
6. **Request re-review deliberately.** After revisions, point reviewers to the new commits or affected files and summarize what feedback was addressed. Resolve a discussion only when the concern is answered—not merely to make the conversation look finished. Reviewers should re-check the changed behavior and any nearby regression risk.
7. **Merge and close the loop.** Merge only after required approvals, automated checks, conflict resolution, and repository policy are satisfied. Choose the team-approved merge method, then confirm the result and clean up the branch if appropriate. If the PR is not ready, leave it open or close it with a clear explanation instead of forcing a merge.

## Practice exercise

Use [`pull-request-body-template.md`](pull-request-body-template.md) to draft a realistic PR description. Replace every `TODO` with substantive text in all six required H2 sections:

- **Summary** — the proposed outcome in clear sentences.
- **Motivation** — the problem, goal, or linked issue.
- **Changes** — the meaningful scope of the diff.
- **Validation** — exact checks run and honest outcomes.
- **Risks and limitations** — compatibility, security, deployment, or evidence limits.
- **Review focus** — files, assumptions, trade-offs, or behavior that deserve attention.

Then role-play the lifecycle: mark the draft as not ready, ask one reviewer for early feedback, revise the description or example, mark it ready, write two actionable review comments on the imagined diff, answer those comments as the author, and record what a re-review should verify before merge. For GitLab, substitute **merge request**, **Draft**, **Ready**, discussion threads, and **re-review**; the communication principles remain the same.

## Offline validation

From the repository root, run the supplied structure check against a completed copy of the template:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -B 017/check_pr_body.py /path/to/completed-pr-body.md
```

The checker reads one Markdown body and exits `0` when all six required sections contain substantive text and none contains `TODO`, `TBD`, `FILL IN`, or `PLACEHOLDER`. It exits `1` when it finds missing, empty, duplicate, or unfinished sections, and `2` when the body file cannot be read.

Run the six offline unit tests with:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -B -m unittest discover -s 017/tests -p 'test_*.py' -v
```

This validation checks description structure only. It does **not** verify evidence, test runs, reviewers, approvals, branch protections, conflicts, or merge eligibility. The template is scoped to Day 017 and is not automatically installed or active in the repository.

## Review lifecycle checklist

- [ ] The change has a focused scope and a meaningful Summary and Motivation.
- [ ] Draft status accurately reflects whether the PR is ready for formal review.
- [ ] Changes, validation evidence, risks, and Review focus are specific rather than boilerplate.
- [ ] Reviewer comments identify impact and an actionable request or question.
- [ ] The author responds to every substantive comment and records the resulting revision.
- [ ] Re-review covers the new commits, resolved discussions, and regression risk.
- [ ] Required checks and approvals are confirmed under the actual repository policy.
- [ ] The merge method and post-merge branch cleanup follow team practice.

## Exact file tree

```text
017/
├── .gitignore
├── README.md
├── check_pr_body.py
├── pull-request-body-template.md
└── tests/
    └── test_check_pr_body.py
```

## Primary sources

- [GitHub: About pull requests](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/about-pull-requests)
- [GitHub: Creating a pull request](https://docs.github.com/articles/creating-a-pull-request)
- [GitHub: Review changes](https://docs.github.com/en/pull-requests/how-tos/review-pull-requests/reviewing-proposed-changes-in-a-pull-request)
- [GitLab: Merge request reviews](https://docs.gitlab.com/user/project/merge_requests/reviews/)

This exercise is documentation and offline validation only. It opens no PR or MR and makes no remote API, repository configuration, branch protection, or merge changes.
