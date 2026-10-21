#!/usr/bin/env python3
"""Practice real Git branching inside a disposable repository, never the caller's."""

import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile


def run_demo(verbose=True):
    """Return verified outcomes; remove the entire sandbox even when a step fails."""
    if shutil.which("git") is None:
        raise RuntimeError("Git is required. Install Git 2.28 or newer and retry.")
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    env.update(GIT_CONFIG_NOSYSTEM="1", GIT_CONFIG_GLOBAL=os.devnull,
               GIT_TERMINAL_PROMPT="0", GIT_EDITOR="true", LC_ALL="C")
    with tempfile.TemporaryDirectory(prefix="day003-branching-") as directory:
        repo = Path(directory)

        def git(*args, expected=0):
            result = subprocess.run(
                ["git", "-c", "core.hooksPath=" + os.devnull, *args],
                cwd=repo, env=env, text=True, capture_output=True, timeout=30,
            )
            if verbose:
                print("$ git " + " ".join(args))
                if result.stdout.strip():
                    print(result.stdout.strip())
            if result.returncode != expected:
                raise RuntimeError(
                    f"Git command {args!r} returned {result.returncode}, "
                    f"expected {expected}: {result.stderr.strip()}"
                )
            return result.stdout

        def commit_file(filename, content, message):
            (repo / filename).write_text(content, encoding="utf-8")
            git("add", "--", filename)
            git("commit", "-m", message)

        git("init", "--initial-branch=main", "--template=")
        git("config", "--local", "user.name", "Branching Lab")
        git("config", "--local", "user.email", "branching-lab@example.invalid")
        git("config", "--local", "commit.gpgSign", "false")
        git("config", "--local", "tag.gpgSign", "false")
        commit_file("greeting.txt", "Hello, builder!\n", "Start the branching lab")

        git("switch", "-c", "feature/add-notes")
        commit_file("notes.txt", "Keep branches focused and short-lived.\n", "Add learning notes")
        git("switch", "main")
        git("merge", "--no-ff", "feature/add-notes", "-m", "Merge learning notes")
        git("branch", "-d", "feature/add-notes")

        # Two branches change the same original line, forcing a real conflict.
        git("switch", "-c", "feature/friendly-greeting")
        commit_file("greeting.txt", "Hello, curious builder!\n", "Make the greeting friendlier")
        git("switch", "main")
        git("switch", "-c", "hotfix/team-greeting")
        commit_file("greeting.txt", "Hello, Devlify-Team!\n", "Address the team")
        git("switch", "main")
        git("merge", "--no-ff", "hotfix/team-greeting", "-m", "Merge team greeting hotfix")
        git("branch", "-d", "hotfix/team-greeting")
        git("merge", "--no-ff", "feature/friendly-greeting", "-m", "Merge friendly greeting", expected=1)
        unmerged = git("diff", "--name-only", "--diff-filter=U").splitlines()
        if unmerged != ["greeting.txt"]:
            raise RuntimeError(f"Expected greeting.txt conflict, got {unmerged!r}")
        conflict_text = (repo / "greeting.txt").read_text(encoding="utf-8")
        if not all(marker in conflict_text for marker in ("<<<<<<<", "=======", ">>>>>>>")):
            raise RuntimeError("Expected real Git conflict markers")
        final_greeting = "Hello, curious Devlify-Team builders!\n"
        commit_file("greeting.txt", final_greeting, "Resolve greeting conflict by preserving both intentions")
        git("branch", "-d", "feature/friendly-greeting")

        graph = git("log", "--graph", "--oneline", "--all", "--decorate")
        branch = git("branch", "--show-current").strip()
        branches = git("branch", "--format=%(refname:short)").splitlines()
        clean = not git("status", "--porcelain").strip()
        remotes = git("remote").splitlines()
        merge_count = int(git("rev-list", "--count", "--merges", "HEAD").strip())
        greeting = (repo / "greeting.txt").read_text(encoding="utf-8")
        if not (branch == "main" and branches == ["main"] and clean
                and not remotes and merge_count == 3 and greeting == final_greeting):
            raise RuntimeError("Final repository checks failed")
        result = dict(branch=branch, branches=branches, clean=clean, remotes=remotes,
                      merge_count=merge_count, conflict_resolved=True,
                      greeting=greeting, graph=graph, sandbox=str(repo))
    if verbose:
        print("PASS: feature merge, hotfix, conflict resolution, clean main, no remotes.")
        print("Temporary lab removed. Your existing repository was not modified.")
    return result


def main():
    try:
        run_demo()
    except (RuntimeError, OSError, subprocess.TimeoutExpired) as error:
        print(f"Branching lab failed: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
