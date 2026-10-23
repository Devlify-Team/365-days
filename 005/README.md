# Day 005 — Create Your First Repository

- **Workbook:** `365_Days_GitHub_Challenge_Tracker.xlsx`
- **Workbook area:** All Projects · Day 5
- **Track:** Month 1 — Foundations & GitHub Basics
- **Primary GitHub lesson:** `hello-world`
- **Backup:** Any Git platform
- **Topic:** Repo Management
- **Original suggested repository name:** `create-your-first-repository`; delivered inside `005/` instead.

## Goal

Learn the local Git workflow behind a first repository: initialize a repository, stage a deliberate set of files, create a commit, inspect the result, and keep generated or secret-like files out of version control.

This is a **local implementation lesson**, not a replacement for GitHub's complete web tutorial. The challenge uses the existing `Devlify-Team/365-days` repository: **do not create a new remote repository, and do not run `git init` inside this challenge folder or any of its day folders.** Day 005 must not contain a nested `.git` directory. The demo is isolated and disposable so it cannot change the caller repository, remote configuration, or global Git settings.

## Concepts

- **Repository:** A directory whose `.git` metadata records project history.
- **`git init`:** Creates repository metadata; `--initial-branch=main` makes the initial branch explicit.
- **Working tree and staging area:** Edited files live in the working tree; `git add` selects the exact snapshot for the next commit.
- **Commit:** A local snapshot with an identity, message, and tracked tree. A local commit alone is not an off-device backup.
- **Local versus remote:** The demo repository has one local commit and **no remotes**. A remote such as GitHub is a separate collaboration and publishing destination; nothing is pushed by this exercise.
- **Ignore rules:** `.gitignore` excludes matching untracked files from ordinary staging; it does not remove tracked files, encrypt secrets, or prevent forced staging. The demo's `.env` is a dummy fixture, not a real credential.

## Files

| File | Purpose |
| --- | --- |
| `hello.py` | Greeting CLI. `greet(name)` strips surrounding whitespace and raises `ValueError` for a blank name; the CLI defaults to `world` and accepts `--name`. |
| `init_demo.py` | Creates a temporary folder, copies `hello.py` and `.gitignore`, writes a small local README, initializes Git, commits the explicit file set, verifies the clean `main` state with no remotes, demonstrates that `.env` is ignored, prints the graph and `PASS`, then removes the folder. |
| `.gitignore` | Ignore rules used by the disposable repository, including `.env`. |
| `README.md` | This Day 005 lesson and runbook. |
| `test_project.py` | Eight tests cover greetings, CLI errors, the initial commit, ignore rules, repeatability, cleanup, and caller/environment isolation. |

## Run it

From the challenge repository root (`/workspace/365-days`):

```bash
python3 005/hello.py
python3 005/hello.py --name John
python3 -B 005/init_demo.py
python3 -B -m unittest discover -s 005 -p 'test_*.py' -v
```

The implementation targets **Python 3.9+**, **Git 2.28+**, and the Python standard library only. The demo uses a local Git identity supplied for that temporary repository; it makes no global Git configuration changes and performs no network access.

**Verified result:** Both greeting commands and the initialization demo completed successfully; all eight tests passed. Earlier day folders were unchanged and no nested `.git` was created in `005/`.

## Expected workflow checklist

- [ ] Confirm work is in the existing `Devlify-Team/365-days` repository.
- [ ] Keep Day 005 free of a nested `.git` directory.
- [ ] Run the greeting with the default and a named value.
- [ ] Run the disposable initialization demo.
- [ ] Confirm the demo stages only `README.md`, `hello.py`, and `.gitignore` for its initial commit.
- [ ] Confirm the demo has one clean commit on `main` and no remotes.
- [ ] Confirm a local `.env` remains ignored and is not tracked.
- [ ] Run the isolated unittest discovery command.

## References

- [GitHub Hello World](https://docs.github.com/en/get-started/start-your-journey/hello-world)
- [Git Guide: git init](https://github.com/git-guides/git-init)
