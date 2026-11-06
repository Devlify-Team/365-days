# Day 19 — Setup GitHub Actions

- **Topic:** CI/CD
- **Month:** Month 1: Foundations & GitHub Basics
- **Primary:** GitHub Actions
- **Alternative:** GitLab CI / Travis CI
- **Slug:** `setup-github-actions`

## What this example does

This example adds a small `ci_greeting.py` module and a unittest suite. The project workflow is [`.github/workflows/019-ci.yml`](../.github/workflows/019-ci.yml), deliberately located at the repository root rather than inside the Day 19 directory: GitHub discovers workflow files from the repository-root `.github/workflows/` directory, not from nested day directories.

The workflow:

- runs on `pull_request` when `019/**` or `.github/workflows/019-ci.yml` changes;
- runs on pushes to `main` when those same paths change; or
- runs when started manually with `workflow_dispatch`.

No schedule timer was added. Because the example uses a narrow path scope, it intentionally does not run for unrelated changes. If you reuse it, adjust the path filters carefully so the workflow covers the files that matter.

On `ubuntu-latest`, it checks out the repository, sets up Python 3.12, and runs the Day 019 unittest suite. The workflow uses `contents: read` only. It has no secrets, performs no write operations or deployments, and does not use `pull_request_target`. Checkout sets `persist-credentials: false`.

The action references are pinned to verified full commit SHAs rather than movable tags:

- [`actions/checkout` v7.0.1](https://github.com/actions/checkout/releases/tag/v7.0.1): `3d3c42e5aac5ba805825da76410c181273ba90b1`
- [`actions/setup-python` v7.1.0](https://github.com/actions/setup-python/releases/tag/v7.1.0): `6d4fd22b20465ccc0f7354476588e8df7c9ca0e0`

The initial push of this workflow to `main` will trigger an automatic workflow run when the configured paths match. Do not assume that run passed until GitHub reports its result.

## Repository tree

```text
.
├── .github/
│   └── workflows/
│       └── 019-ci.yml
└── 019/
    ├── .gitignore
    ├── README.md
    ├── ci_greeting.py
    └── tests/
        └── test_ci_greeting.py
```

## Run the tests locally

From the repository root:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -B -m unittest discover -s 019/tests -p 'test_*.py' -v
```

The workflow syntax, including jobs and triggers, is documented in [GitHub's workflow syntax reference](https://docs.github.com/en/actions/writing-workflows/workflow-syntax-for-github-actions). For Python setup and build/test patterns, see [Building and testing Python](https://docs.github.com/en/actions/guides/building-and-testing-python). See [events that trigger workflows](https://docs.github.com/en/actions/writing-workflows/choosing-when-your-workflow-runs/events-that-trigger-workflows) for event and path-filter behavior, and [security hardening for GitHub Actions](https://docs.github.com/en/actions/security-for-github-actions/security-guides/security-hardening-for-github-actions) for the security practices used here.
