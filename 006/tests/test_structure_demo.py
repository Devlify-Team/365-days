"""Dependency-free tests for the example package and CLI."""

import contextlib
import io
import unittest

from structure_demo import greet, main


class StructureDemoTests(unittest.TestCase):
    def test_default_greeting(self):
        self.assertEqual(greet(), "Hello, world!")

    def test_name_is_trimmed(self):
        self.assertEqual(greet("  John  "), "Hello, John!")

    def test_blank_name_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "blank"):
            greet(" \t")

    def test_cli_prints_greeting(self):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            self.assertEqual(main(["--name", "John"]), 0)
        self.assertEqual(output.getvalue(), "Hello, John!\n")

    def test_cli_reports_blank_name(self):
        with contextlib.redirect_stderr(io.StringIO()):
            with self.assertRaises(SystemExit) as raised:
                main(["--name", " "])
        self.assertEqual(raised.exception.code, 2)


if __name__ == "__main__":
    unittest.main()
