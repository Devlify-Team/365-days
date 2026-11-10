# Create a Python package template

- **Month:** 1 — Foundations & GitHub Basics
- **Category:** Templates
- **Primary GitHub:** `python-template`
- **Alternative:** Cookiecutter
- **Slug:** `create-a-python-package-template`

This folder is a minimal setuptools-based Python package starter. It uses a `src/` layout, exposes `greet` from `python_template`, includes a small greeting CLI, and provides a pytest suite as a starting point for replacement package behavior.

## Current structure

- `pyproject.toml` — setuptools build metadata, package metadata, Python `>=3.10`, the editable test extra (`pytest>=8,<10`), the `python-template=python_template.cli:main` console script, `src`-directory package discovery, and pytest configuration.
- `src/python_template/__init__.py` — exports `greet` and currently reports version `0.1.0`.
- `src/python_template/core.py` — defines `greet(name="world")`, including blank-name and non-text validation.
- `src/python_template/cli.py` — implements `python-template --name NAME`.
- `src/python_template/__main__.py` — supports `python -m python_template`.
- `tests/test_core.py` — tests default, named, blank-name, and non-text greeting behavior.
- `.gitignore` — ignores the virtual environment, caches, build artifacts, and package metadata generated during development.
- `TEMPLATE_CHECKLIST.md` — publishing checklist, including package naming, replacement functionality, metadata, licensing, clean-environment checks, and removal of placeholder metadata.

## Setup and verification

Run these exact commands from the repository root:

```bash
cd 023
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e '.[test]'
python -m pytest
python-template --name Ada
python -m python_template
```

Expected CLI output for the named invocation is:

```text
Hello, Ada!
```

The module invocation uses the CLI's default name and should print:

```text
Hello, world!
```

**Validated locally:** All five tests passed in an isolated environment; both CLI entry points printed their expected greetings, and pip built a wheel successfully. Build products and test caches are excluded by `.gitignore`.

## What to rename or replace

Before publishing or turning this into a real package:

1. Choose a unique distribution name in `pyproject.toml` and update the import-package directory under `src/` (currently `src/python_template`). Keep the distribution name and import name intentionally aligned or document the distinction.
2. Replace the example `greet` API, greeting CLI, and demo tests with the package's actual functionality and tests.
3. Set the supported Python range, version, description, console-script entry points, runtime dependencies, and optional development dependencies deliberately.
4. Remove placeholder metadata and update the README and package docstrings so they describe the real project.
5. Choose and include a license before public distribution. No license is chosen in this starter; see `TEMPLATE_CHECKLIST.md`.
6. Install in a clean environment, run the tests, and build/check the distribution before publishing, as noted in the checklist.

Because this project uses a `src` layout, the package is not expected to be imported directly from the repository root without installation. Use the editable install shown above during development. See the PyPA [Packaging Python Projects tutorial](https://packaging.python.org/en/latest/tutorials/packaging-projects/) and [src layout vs flat layout discussion](https://packaging.python.org/en/latest/discussions/src-layout-vs-flat-layout/) for the rationale and packaging workflow.

## GitHub template repository note

This numbered folder is **not itself registered as a GitHub Template Repository**. To make a reusable GitHub template, move or copy the package project into its own repository, then enable **Settings → Template repository** in that repository. Users can then create new repositories from it. See GitHub's documentation on [creating a template repository](https://docs.github.com/en/repositories/creating-and-managing-repositories/creating-a-template-repository) and [creating a repository from a template](https://docs.github.com/en/repositories/creating-and-managing-repositories/creating-a-repository-from-a-template).
