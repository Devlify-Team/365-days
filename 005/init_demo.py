#!/usr/bin/env python3
"""Create and verify a first commit in an automatically removed temporary repo."""

import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile


def run_demo(verbose=True):
    if shutil.which("git") is None:
        raise RuntimeError("Install Git 2.28+ to run this lesson")
    # Isolate inherited repository paths, templates, hooks and signing settings.
    env = {key: value for key, value in os.environ.items() if not key.startswith("GIT_")}
    env.update(GIT_CONFIG_NOSYSTEM="1", GIT_CONFIG_GLOBAL=os.devnull,
               GIT_TERMINAL_PROMPT="0", LC_ALL="C")
    source = Path(__file__).resolve().parent
    with tempfile.TemporaryDirectory(prefix="day005-first-repo-") as directory:
        repo = Path(directory)

        def git(*args, expected=0):
            result = subprocess.run(
                ["git", "-c", "core.hooksPath=" + os.devnull, *args],
                cwd=repo, env=env, capture_output=True, text=True, timeout=30,
            )
            if verbose:
                print("$ git " + " ".join(args))
                if result.stdout.strip():
                    print(result.stdout.strip())
            if result.returncode != expected:
                raise RuntimeError(f"Git command {args!r} failed: {result.stderr.strip()}")
            return result.stdout

        shutil.copyfile(source / "hello.py", repo / "hello.py")
        shutil.copyfile(source / ".gitignore", repo / ".gitignore")
        (repo / "README.md").write_text(
            "# My first repository\n\nRun `python3 hello.py --name John`.\n"
            "This disposable lesson has no remote repository.\n", encoding="utf-8",
        )
        git("init", "--initial-branch=main", "--template=")
        git("config", "--local", "user.name", "First Repository Learner")
        git("config", "--local", "user.email", "learner@example.invalid")
        git("config", "--local", "commit.gpgSign", "false")
        git("add", "--", "README.md", "hello.py", ".gitignore")
        git("commit", "-m", "Create first repository with a Hello World program")
        tracked = git("ls-files", "-z").split("\0")
        tracked = sorted(name for name in tracked if name)
        count = int(git("rev-list", "--count", "HEAD").strip())
        branch = git("branch", "--show-current").strip()
        remotes = git("remote").splitlines()
        # A dummy fixture, never an actual credential. Ignoring is not encryption.
        (repo / ".env").write_text("DEMO_ONLY=not-a-secret\n", encoding="utf-8")
        ignored = git("check-ignore", ".env").strip() == ".env"
        clean = not git("status", "--porcelain").strip()
        graph = git("log", "--oneline", "--decorate")
        if not (tracked == [".gitignore", "README.md", "hello.py"]
                and count == 1 and branch == "main" and not remotes and ignored and clean):
            raise RuntimeError("First-repository verification failed")
        result = dict(tracked=tracked, commit_count=count, branch=branch,
                      remotes=remotes, env_ignored=ignored, clean=clean,
                      graph=graph, sandbox=str(repo))
    if verbose:
        print("PASS: one initial commit on main, expected files tracked, .env ignored, no remotes.")
        print("Temporary repository removed; the shared challenge repository was not changed.")
    return result


def main():
    try:
        run_demo()
    except (RuntimeError, OSError, subprocess.TimeoutExpired) as error:
        print(f"Initialization lesson failed: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
