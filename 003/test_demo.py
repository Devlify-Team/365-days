"""Integration tests execute real Git operations only in disposable folders."""

import contextlib
import io
import os
from pathlib import Path
import shutil
import tempfile
import unittest
from unittest.mock import patch

from demo import run_demo, main


@unittest.skipUnless(shutil.which("git"), "Git must be installed")
class BranchingDemoTests(unittest.TestCase):
    def test_real_merges_conflict_resolution_and_cleanup(self):
        result = run_demo(verbose=False)
        self.assertEqual(result["branch"], "main")
        self.assertEqual(result["branches"], ["main"])
        self.assertEqual(result["merge_count"], 3)
        self.assertTrue(result["clean"])
        self.assertTrue(result["conflict_resolved"])
        self.assertEqual(result["remotes"], [])
        self.assertEqual(result["greeting"], "Hello, curious Devlify-Team builders!\n")
        self.assertIn("Resolve greeting conflict", result["graph"])
        self.assertFalse(Path(result["sandbox"]).exists())

    def test_repeatable_without_modifying_caller(self):
        caller = Path.cwd()
        with tempfile.TemporaryDirectory() as directory:
            sentinel = Path(directory) / "keep.txt"
            sentinel.write_text("Do not change this", encoding="utf-8")
            try:
                os.chdir(directory)
                first = run_demo(verbose=False)
                second = run_demo(verbose=False)
                self.assertEqual(sentinel.read_text(encoding="utf-8"), "Do not change this")
                self.assertEqual(list(Path(directory).iterdir()), [sentinel])
                self.assertNotEqual(first["sandbox"], second["sandbox"])
            finally:
                os.chdir(caller)

    def test_hostile_inherited_git_environment_is_ignored(self):
        with tempfile.TemporaryDirectory() as directory:
            fake_git = str(Path(directory) / "do-not-create")
            with patch.dict(os.environ, {"GIT_DIR": fake_git,
                                         "GIT_WORK_TREE": directory,
                                         "GIT_INDEX_FILE": fake_git + "-index"}):
                self.assertTrue(run_demo(verbose=False)["clean"])
            self.assertEqual(list(Path(directory).iterdir()), [])

    def test_missing_git_has_clear_error(self):
        with patch("demo.shutil.which", return_value=None):
            with self.assertRaisesRegex(RuntimeError, "Git is required"):
                run_demo(verbose=False)

    def test_cli_reports_error_without_traceback(self):
        output = io.StringIO()
        with patch("demo.run_demo", side_effect=RuntimeError("example failure")):
            with contextlib.redirect_stderr(output):
                self.assertEqual(main(), 1)
        self.assertIn("Branching lab failed: example failure", output.getvalue())


if __name__ == "__main__":
    unittest.main()
