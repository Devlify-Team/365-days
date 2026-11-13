import unittest
from pathlib import Path

from scripts.check_question import check_draft


SAMPLE = Path(__file__).resolve().parents[1] / "samples" / "question-draft.md"


class CheckQuestionTests(unittest.TestCase):
    def test_sample_question_is_complete(self):
        self.assertEqual(check_draft(SAMPLE.read_text(encoding="utf-8")), [])

    def test_missing_section_is_reported(self):
        draft = """# Question

## Goal

I want to understand the setup.

## Context

I use the current release.

## What I tried

I read the guide.
"""
        self.assertIn("Add a '## Question' section.", check_draft(draft))

    def test_unfilled_prompt_is_reported(self):
        draft = """# Question

## Goal

[Describe the goal.]

## Context

I use the current release.

## What I tried

I read the guide.

## Question

How should I proceed?
"""
        self.assertTrue(any("placeholder" in item for item in check_draft(draft)))

    def test_empty_section_is_reported(self):
        draft = """# Question

## Goal

I want to understand the setup.

## Context


## What I tried

I read the guide.

## Question

How should I proceed?
"""
        self.assertIn("Add content under '## Context'.", check_draft(draft))


if __name__ == "__main__":
    unittest.main()
