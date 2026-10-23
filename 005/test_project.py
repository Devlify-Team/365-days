"""Unit tests plus isolated real-Git integration tests; no network required."""

import contextlib
import io
import os
from pathlib import Path
import shutil
import tempfile
import unittest
from unittest.mock import patch

from hello import greet, main
from init_demo import run_demo


class GreetingTests(unittest.TestCase):
    def test_default_greeting(self):
        self.assertEqual(greet(), "Hello, world!")

    def test_named_and_trimmed_greeting(self):
        self.assertEqual(greet("  John  "), "Hello, John!")

    def test_blank_name_rejected(self):
        with self.assertRaisesRegex(ValueError, "blank"):
            greet(" \t")

    def test_cli_prints_greeting(self):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            self.assertEqual(main(["--name", "John"]), 0)
        self.assertEqual(output.getvalue(), "Hello, John!\n")

    def test_blank_cli_name_exits_two(self):
        with contextlib.redirect_stderr(io.StringIO()):
            with self.assertRaises(SystemExit) as raised:
                main(["--name", " "])
        self.assertEqual(raised.exception.code, 2)


@unittest.skipUnless(shutil.which("git"), "Git required")
class InitializationTests(unittest.TestCase):
    def test_initial_commit_ignore_rules_and_cleanup(self):
        result = run_demo(verbose=False)
        self.assertEqual(result["tracked"], [".gitignore", "README.md", "hello.py"])
        self.assertEqual(result["commit_count"], 1)
        self.assertEqual(result["branch"], "main")
        self.assertEqual(result["remotes"], [])
        self.assertTrue(result["env_ignored"])
        self.assertTrue(result["clean"])
        self.assertFalse(Path(result["sandbox"]).exists())

    def test_repeatable_and_isolated_from_caller_and_git_environment(self):
        original = Path.cwd()
        with tempfile.TemporaryDirectory() as directory:
            sentinel = Path(directory) / "keep.txt"
            sentinel.write_text("Preserve me", encoding="utf-8")
            try:
                os.chdir(directory)
                with patch.dict(os.environ, {"GIT_DIR": "/missing/git", "GIT_WORK_TREE": directory}):
                    first = run_demo(verbose=False)
                    second = run_demo(verbose=False)
                self.assertNotEqual(first["sandbox"], second["sandbox"])
                self.assertEqual(sentinel.read_text(encoding="utf-8"), "Preserve me")
                self.assertEqual(list(Path(directory).iterdir()), [sentinel])
            finally:
                os.chdir(original)

    def test_missing_git_explained(self):
        with patch("init_demo.shutil.which", return_value=None):
            with self.assertRaisesRegex(RuntimeError, "Install Git"):
                run_demo(verbose=False)


if __name__ == "__main__":
    unittest.main()
