import unittest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from ci_greeting import greet


class GreetingTests(unittest.TestCase):
    def test_default_greeting(self):
        self.assertEqual(greet(), "Hello, world!")

    def test_strips_surrounding_whitespace(self):
        self.assertEqual(greet("  Ada  "), "Hello, Ada!")

    def test_rejects_blank_name(self):
        with self.assertRaisesRegex(ValueError, "must not be blank"):
            greet(" \t ")

    def test_rejects_non_text_name(self):
        with self.assertRaisesRegex(TypeError, "must be text"):
            greet(None)


if __name__ == "__main__":
    unittest.main()
