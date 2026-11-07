# Day 20: Automated testing with pytest

**Month 1 — Foundations & GitHub Basics** · **Topic:** CI/CD · **Primary:** GitHub pytest-actions · **Alternative:** `unittest` / `nose` · **Slug:** `automated-testing-with-pytest`

## What this exercise demonstrates

This small package exposes `src/reading_stats.py`, with a focused pytest suite that demonstrates a fixture, parametrization, `pytest.approx` for floating-point comparisons, and `pytest.raises` for expected errors. pytest discovers `test_*.py` and `*_test.py` files by convention and supports the `src` layout with a `pythonpath` setting in its configuration ([pytest: Getting Started](https://docs.pytest.org/en/stable/getting-started.html); [Good Integration Practices](https://docs.pytest.org/en/stable/explanation/goodpractices.html)).

The test dependency is deliberately pinned in `requirements-test.txt`:

```text
pytest==9.2.0
```

pytest 9.2.0 is an official release ([release page](https://github.com/pytest-dev/pytest/releases/tag/9.2.0)). The official support table lists pytest 9.0+ as supporting Python 3.10+, so this exercise is supported on Python 3.12 ([pytest Python version support](https://docs.pytest.org/en/stable/backwards-compatibility.html#python-version-support)).

## Project tree

```text
020/
├── .gitignore
├── README.md
├── pytest.ini
├── requirements-test.txt
├── src/
│   └── reading_stats.py
└── tests/
    └── test_reading_stats.py

.github/
└── workflows/
    └── 020-pytest.yml
```

`pytest.ini` makes discovery explicit and adds `src` to the import path:

```ini
[pytest]
testpaths = tests
pythonpath = src
addopts = -ra
```

## Run the tests locally

From the repository root:

```bash
cd 020
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-test.txt
python -m pytest -q
```

Using `python -m pytest` runs pytest through the active interpreter; `-q` keeps the output brief. The virtual-environment and installation pattern follows pytest’s getting-started guidance ([pytest: Getting Started](https://docs.pytest.org/en/stable/getting-started.html)).

## CI workflow

The workflow is [`.github/workflows/020-pytest.yml`](../.github/workflows/020-pytest.yml). It runs on pull requests and pushes to `main` only when `020/**` or the workflow itself changes, and it can also be started manually with `workflow_dispatch`. There is intentionally no schedule. The workflow checks out the repository, sets up Python 3.12, installs the pinned requirements, and runs `python -m pytest -q` with `020` as its working directory. GitHub documents this install-and-test pattern in [Building and testing Python](https://docs.github.com/en/actions/guides/building-and-testing-python), and documents event/path filters in [Events that trigger workflows](https://docs.github.com/en/actions/writing-workflows/choosing-when-your-workflow-runs/events-that-trigger-workflows).

```yaml
name: Day 020 — pytest example

on:
  pull_request:
    paths:
      - '020/**'
      - '.github/workflows/020-pytest.yml'
  push:
    branches:
      - main
    paths:
      - '020/**'
      - '.github/workflows/020-pytest.yml'
  workflow_dispatch:

permissions:
  contents: read

jobs:
  pytest:
    name: pytest (Python 3.12)
    runs-on: ubuntu-latest
    steps:
      - name: Check out repository
        uses: actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1 # v7.0.1
        with:
          persist-credentials: false
      - name: Set up Python 3.12
        uses: actions/setup-python@6d4fd22b20465ccc0f7354476588e8df7c9ca0e0 # v7.1.0
        with:
          python-version: '3.12'
      - name: Install pinned pytest
        run: python -m pip install --disable-pip-version-check -r requirements-test.txt
        working-directory: '020'
      - name: Run the test suite
        run: python -m pytest -q
        working-directory: '020'
```

The actions are pinned to full commit SHAs, and the job grants only read access to repository contents. This follows GitHub’s security-hardening guidance on least-privilege `GITHUB_TOKEN` permissions and full-SHA action pinning ([Security hardening for GitHub Actions](https://docs.github.com/en/actions/security-for-github-actions/security-guides/security-hardening-for-github-actions)). The `permissions` and workflow structure follow [Workflow syntax for GitHub Actions](https://docs.github.com/en/actions/writing-workflows/workflow-syntax-for-github-actions). The workflow has no secrets, deployment step, artifact publishing, or write permission.

The isolated local test suite currently passes **10 cases** with pytest 9.2.0.

## Scope and caveat

A passing test run shows that the checked examples satisfy the current assertions; it does not prove that the implementation is correct for every possible input. This exercise demonstrates CI only for Day 20: its path filters keep the workflow focused on `020` and do not run or alter the other day projects.
