# Set up pre-commit hooks

- **Day:** 029
- **Month:** 1 — Foundations & GitHub Basics
- **Category:** Advanced
- **Primary GitHub:** `pre-commit`
- **Alternative:** Git hooks
- **Slug:** `setup-pre-commit-hooks`

This starter config runs lightweight checks before a commit: trim accidental trailing whitespace, ensure a final newline, and validate YAML and TOML files. Hook revisions are pinned so the same hook code is used until you intentionally update it. A test checks the configuration itself.

## Try the sample configuration

This project lives in a numbered subfolder of a larger repository, so it does not install hooks into the parent repository automatically. From the repository root, install the pinned pre-commit framework and run the sample config on the Day 029 files:

```bash
python3 -m venv 029/.venv
029/.venv/bin/python -m pip install -r 029/requirements-dev.txt
029/.venv/bin/pre-commit run --config 029/.pre-commit-config.yaml \
  --files 029/.pre-commit-config.yaml 029/pyproject.toml \
  029/README.md 029/requirements-dev.txt 029/tests/test_config.py
029/.venv/bin/python -m unittest discover -s 029/tests -v
```

The first run downloads the pinned hook repository. Some hooks may edit files; review and stage any changes they make. To enable the same workflow for your own repository, merge the config into a `.pre-commit-config.yaml` at that repository's root, adapt its hook set, install `pre-commit`, then run `pre-commit install` from the root. Do not overwrite an existing hook config without reviewing it.

## What to expect

After installation, `pre-commit` runs on staged files during `git commit`. If a hook fixes a file, inspect the diff, stage the fix, and commit again. For broader validation, run `pre-commit run --all-files`. Hooks improve consistency; they are not a security boundary and can be skipped by users with permission to bypass local Git hooks. CI can run the same checks independently.

The framework's [official guide](https://pre-commit.com/) documents installation, revisions, and running hooks. The [`pre-commit-hooks` repository](https://github.com/pre-commit/pre-commit-hooks) lists the checks used here.
