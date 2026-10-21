# Day 003 — Learn Git branching strategies

**Track:** Version Control  ·  **Month 1:** Foundations & GitHub Basics  
**Primary GitHub:** `git-branching`  ·  **Suggested repository:** `learn-git-branching-strategies`  
**Backup topic:** GitLab Flow

**Source workbook:** `365_Days_GitHub_Challenge_Tracker.xlsx`, `All Projects`, Day 3. Delivered inside `Devlify-Team/365-days/003/`; no separate repository is needed.

## Source mapping

- **Git branching and merging:** [Git Branching — Basic Branching and Merging](https://git-scm.com/book/en/v2/Git-Branching-Basic-Branching-and-Merging)
- **Pull-request-oriented collaboration:** [GitHub Flow](https://docs.github.com/en/get-started/using-github/github-flow)
- **Alternative/backup:** [GitLab branching strategies](https://docs.gitlab.com/user/project/repository/branches/strategies/)

## Run the lab

From the repository root:

```bash
python3 003/demo.py
python3 -B -m unittest discover -s 003 -p 'test_*.py' -v
```

**Requirements:** Git >= 2.28 and Python >= 3.9. No extra packages are needed.

The demo creates a fully isolated temporary Git repository, sets a local-only demo identity, makes a `main` baseline, merges a feature with `--no-ff`, then creates a hotfix and a competing feature that edit the same greeting line. It produces a real merge conflict, resolves it with a combined greeting, removes merged branches, prints the commit graph, and ends with `PASS`. The temporary repository is deleted on exit. It uses no network and changes no global Git configuration.

This is deliberately a **local mechanics demo**: it creates no pull request and no branches in the real GitHub repository.

## Concepts

- A **feature branch** is a short-lived pointer for isolated work. It lets a change be developed and reviewed without moving `main` prematurely.
- **`main`** is the shared, releasable baseline. Keep it buildable and integrate small changes frequently.
- A **merge conflict** occurs when Git cannot safely combine competing edits—commonly, two branches changing the same lines. A developer must inspect the conflict markers, choose or combine the intended content, stage the resolution, and complete the merge.
- A local merge exercises Git’s history and conflict mechanics. A **real pull request** additionally provides hosted review, automated checks, discussion, approvals, and a protected-branch integration decision.

## Strategy comparison

| Strategy | Shape | Strength | Trade-off |
|---|---|---|---|
| **GitHub Flow** | Short-lived branch → pull request → `main` | Simple, reviewable, and continuous-delivery friendly | Requires discipline and effective checks; unfinished work needs flags or draft PRs |
| **Trunk-based development** | Very short branches or direct, reviewed trunk changes | Small integrations reduce drift and merge pain; excellent for a daily monorepo | Needs strong tests, ownership, and feature flags for incomplete work |
| **Gitflow** | Long-lived `develop`, release, feature, hotfix branches | Explicit release trains and parallel stabilization | More ceremony and branch drift than most continuously delivered products need |

**Recommendation for a daily monorepo:** use a lightweight GitHub-Flow/trunk-based hybrid: one protected `main`, small short-lived branches, one focused pull request, required CI, frequent merges, and feature flags for incomplete functionality. Reserve release branches for a concrete release or stabilization need rather than creating them by default.

## Manual exercise (disposable repository only)

Run these commands in a throwaway directory—not in the workbook repository or any shared/production checkout:

```bash
TMP_REPO="$(mktemp -d)" || exit 1
cd "$TMP_REPO"
git init -b main
git config user.name 'Practice User'
git config user.email 'practice@example.invalid'
printf 'Hello\n' > greeting.txt
git add greeting.txt && git commit -m 'baseline'
git switch -c feature/welcome
printf 'Hello from the feature\n' > greeting.txt
git add greeting.txt && git commit -m 'feature greeting'
git switch main
git merge --no-ff feature/welcome -m 'merge feature'
git log --oneline --graph --decorate --all
```

To practice a conflict, create two disposable branches from the same commit, change the same line differently, merge one branch into `main`, then merge the other. Inspect `greeting.txt` and resolve the `<<<<<<<`, `=======`, and `>>>>>>>` markers by writing the desired combined greeting; then run:

```bash
git add greeting.txt
git commit -m 'resolve greeting conflict'
git status
```

Clean up only after checking the exercise is disposable (in the same shell):

```bash
cd /
rm -rf "$TMP_REPO"
```

## Questions checklist

- Why does `--no-ff` leave a visible feature-merge commit?
- Which exact lines caused the conflict, and what should the combined greeting preserve?
- What should be tested before opening or approving a pull request?
- When would a feature flag be safer than a long-lived branch?
- Which branch protections and CI checks should `main` require in your monorepo?
- When would Gitflow’s release branch justify its extra ceremony?

**Validation:** The executable lab completed successfully, and all five automated tests passed, including repeat runs, temporary-folder cleanup, and isolation from inherited Git environment variables.
