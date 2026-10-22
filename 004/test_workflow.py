"""Exercise the checker against real, isolated Git repositories."""

import contextlib
import io
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest
from unittest.mock import patch

from check_workflow import inspect_repository, main


@unittest.skipUnless(shutil.which("git"), "Git required")
class WorkflowTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="day004-test-")
        self.addCleanup(self.temp.cleanup)
        self.repo = Path(self.temp.name)
        self.env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
        self.env.update(GIT_CONFIG_NOSYSTEM="1", GIT_CONFIG_GLOBAL=os.devnull,
                        GIT_TERMINAL_PROMPT="0", GIT_EDITOR="true", LC_ALL="C")
        self.git("init", "--initial-branch=main", "--template=")
        self.git("config", "user.name", "Workflow Test")
        self.git("config", "user.email", "workflow@example.invalid")
        self.git("config", "commit.gpgSign", "false")
        self.stage("file.txt", "Baseline\n")
        self.git("commit", "-m", "Baseline")
        self.git("switch", "-c", "feature/day004")

    def git(self, *args, expected=0):
        result = subprocess.run(["git", "-c", "core.hooksPath=" + os.devnull, *args],
                                cwd=self.repo, env=self.env, text=True,
                                capture_output=True, timeout=30)
        self.assertEqual(result.returncode, expected, result.stderr)
        return result.stdout

    def stage(self, name, content):
        (self.repo / name).write_text(content, encoding="utf-8")
        self.git("add", "--", name)

    def inspect(self):
        with patch.dict(os.environ, {"GIT_CONFIG_NOSYSTEM": "1", "GIT_CONFIG_GLOBAL": os.devnull}):
            return inspect_repository(self.repo)

    def test_clean_staged_change_is_ready_and_read_only(self):
        self.stage("file.txt", "Reviewed change\n")
        before = (self.repo / ".git/index").read_bytes()
        head = self.git("rev-parse", "HEAD")
        report = self.inspect()
        self.assertTrue(report["ready"])
        self.assertEqual(report["staged_files"], ["file.txt"])
        self.assertEqual(report["warnings"], [])
        self.assertEqual((self.repo / ".git/index").read_bytes(), before)
        self.assertEqual(self.git("rev-parse", "HEAD"), head)

    def test_unstaged_only_is_not_ready(self):
        (self.repo / "file.txt").write_text("Not staged\n", encoding="utf-8")
        self.assertFalse(self.inspect()["ready"])

    def test_trailing_whitespace_is_blocked(self):
        self.stage("file.txt", "Trailing space \n")
        report = self.inspect()
        self.assertFalse(report["ready"])
        self.assertIn("whitespace", " ".join(report["issues"]))

    def test_unresolved_conflict_is_blocked(self):
        self.stage("file.txt", "Feature\n")
        self.git("commit", "-m", "Feature")
        self.git("switch", "main")
        self.stage("file.txt", "Main\n")
        self.git("commit", "-m", "Main")
        self.git("merge", "feature/day004", expected=1)
        report = self.inspect()
        self.assertFalse(report["ready"])
        self.assertEqual(report["conflict_files"], ["file.txt"])

    def test_default_branch_and_detached_head_are_advisory(self):
        self.git("switch", "main")
        self.stage("file.txt", "Ready on main\n")
        report = self.inspect()
        self.assertTrue(report["ready"])
        self.assertTrue(report["warnings"])
        self.git("switch", "--detach", "HEAD")
        report = self.inspect()
        self.assertTrue(report["ready"])
        self.assertIsNone(report["branch"])
        self.assertIn("Detached", report["warnings"][0])

    def test_json_cli_and_error_exit_codes(self):
        self.stage("space in name.txt", "Safe filename\n")
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            self.assertEqual(main(["--repo", str(self.repo), "--json"]), 0)
        self.assertIn("space in name.txt", json.loads(output.getvalue())["staged_files"])
        self.git("reset", "HEAD", "--", "space in name.txt")
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(main(["--repo", str(self.repo), "--json"]), 1)
            self.assertEqual(main(["--repo", str(self.repo / "missing"), "--json"]), 2)

    def test_inherited_git_directory_cannot_redirect_checker(self):
        self.stage("file.txt", "Scoped change\n")
        with patch.dict(os.environ, {"GIT_DIR": "/nonexistent/git", "GIT_INDEX_FILE": "/nonexistent/index"}):
            self.assertTrue(self.inspect()["ready"])


if __name__ == "__main__":
    unittest.main()
