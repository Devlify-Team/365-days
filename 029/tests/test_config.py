import unittest
from pathlib import Path

import yaml


CONFIG_PATH = Path(__file__).resolve().parents[1] / ".pre-commit-config.yaml"
EXPECTED_HOOKS = {
    "trailing-whitespace",
    "end-of-file-fixer",
    "check-yaml",
    "check-toml",
    "check-added-large-files",
}


class PreCommitConfigTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.config = yaml.safe_load(CONFIG_PATH.read_text(encoding="utf-8"))

    def test_framework_minimum_is_declared(self):
        self.assertEqual(self.config["minimum_pre_commit_version"], "4.7.0")

    def test_external_repositories_are_pinned(self):
        self.assertTrue(self.config["repos"])
        for repository in self.config["repos"]:
            with self.subTest(repository=repository["repo"]):
                self.assertTrue(repository.get("rev"))
                self.assertNotIn("@main", repository["rev"])

    def test_expected_quality_hooks_are_configured(self):
        hooks = {
            hook["id"]
            for repository in self.config["repos"]
            for hook in repository["hooks"]
        }
        self.assertEqual(hooks, EXPECTED_HOOKS)

    def test_hook_ids_are_unique(self):
        hook_ids = [
            hook["id"]
            for repository in self.config["repos"]
            for hook in repository["hooks"]
        ]
        self.assertEqual(len(hook_ids), len(set(hook_ids)))


if __name__ == "__main__":
    unittest.main()
