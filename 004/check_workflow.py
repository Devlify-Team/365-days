#!/usr/bin/env python3
"""Read-only Git preflight. This is not a test runner or a secret scanner."""

import argparse
import json
import os
from pathlib import Path
import subprocess
import sys


class GitError(RuntimeError):
    """Git could not inspect the requested working repository."""


def inspect_repository(path="."):
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    env.update(GIT_OPTIONAL_LOCKS="0", GIT_TERMINAL_PROMPT="0", LC_ALL="C")
    path = Path(path).resolve()

    def git(*args, allowed=(0,)):
        result = subprocess.run(
            ["git", "-c", "color.ui=false", "-C", str(path), *args],
            env=env, capture_output=True, text=True, encoding="utf-8",
            errors="replace", timeout=30,
        )
        if result.returncode not in allowed:
            raise GitError(result.stderr.strip() or f"git {args[0]} failed ({result.returncode})")
        return result

    if git("rev-parse", "--is-inside-work-tree").stdout.strip() != "true":
        raise GitError("A non-bare working repository is required")
    root = git("rev-parse", "--show-toplevel").stdout.strip()
    branch_result = git("symbolic-ref", "--quiet", "--short", "HEAD", allowed=(0, 1))
    branch = branch_result.stdout.strip() if branch_result.returncode == 0 else None
    staged = git("diff", "--cached", "--name-only", "--no-ext-diff", "--no-textconv", "-z").stdout
    staged_files = [name for name in staged.split("\0") if name]
    conflicts = git("diff", "--name-only", "--diff-filter=U", "--no-ext-diff", "--no-textconv", "-z").stdout
    conflict_files = [name for name in conflicts.split("\0") if name]
    whitespace = git("diff", "--cached", "--check", "--no-ext-diff", "--no-textconv", allowed=(0, 1, 2))
    if whitespace.returncode and not whitespace.stdout.strip():
        raise GitError(whitespace.stderr.strip() or "Unable to check staged whitespace")

    issues = []
    warnings = []
    if not staged_files:
        issues.append("No staged changes. Review your diff and explicitly stage the intended files.")
    if conflict_files:
        issues.append("Unresolved merge conflicts: " + ", ".join(conflict_files))
    if whitespace.returncode:
        issues.append("Staged whitespace errors or conflict markers: " + whitespace.stdout.strip())
    if branch is None:
        warnings.append("Detached HEAD: switch to an appropriate branch before normal collaboration.")
    elif branch in ("main", "master"):
        warnings.append("On a common default branch; prefer a short-lived branch for reviewed changes.")
    return dict(repository=root, branch=branch, staged_files=staged_files,
                conflict_files=conflict_files, issues=issues, warnings=warnings,
                ready=not issues)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", default=".", help="Working repository or a directory within it")
    parser.add_argument("--json", action="store_true", help="Print machine-readable output")
    args = parser.parse_args(argv)
    try:
        report = inspect_repository(args.repo)
    except (GitError, OSError, subprocess.TimeoutExpired) as error:
        if args.json:
            print(json.dumps({"ready": False, "error": str(error)}))
        else:
            print(f"ERROR: {error}", file=sys.stderr)
        return 2
    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print("READY (limited preflight)" if report["ready"] else "NOT READY")
        print(f"Repository: {report['repository']}")
        print(f"Branch: {report['branch'] or '(detached)'}")
        print(f"Staged paths: {len(report['staged_files'])}")
        for issue in report["issues"]:
            print(f"ISSUE: {issue}")
        for warning in report["warnings"]:
            print(f"WARNING: {warning}")
        print("Still review the diff, run tests, and check for secrets and required approvals.")
    return 0 if report["ready"] else 1


if __name__ == "__main__":
    sys.exit(main())
