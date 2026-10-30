# Day 12 — Create a reproducible environment

**Workbook mapping:** Day 12 · Month 1 — Foundations & GitHub Basics · Topic: Data Science · Primary GitHub concept: `conda-env` · Alternatives: Docker and pipenv · Slug: `create-reproducible-environment`.

## What this demonstrates

This is a small, reproducible-environment concept/demo. The workbook metadata names `conda-env`, but the tested artifact uses [uv](https://docs.astral.sh/uv/) instead. This choice keeps the example lightweight while demonstrating the same important ideas: declare supported versions and direct dependencies, resolve them, commit the generated lockfile, and verify the environment. This is **not** an actual conda environment or conda lockfile, so no conda commands or conda support are implied.

There are no datasets in this project and no data is analysed. `environment_report.py` only reports runtime and package versions.

## Project files

- `.python-version` pins Python **3.12.3**.
- `pyproject.toml` supports `>=3.12,<3.13`, with direct dependency `pandas>=2.2,<4` and development dependency `pytest>=8,<10`.
- `uv.lock` is the generated, committed lockfile. It freezes dependency resolutions for supported platforms and includes marker and hash information.
- `environment_report.py` prints the runtime and installed package versions; it performs no analysis.
- `tests/test_environment_report.py` checks the report behavior.
- `.gitignore` excludes `.venv`, caches, and secrets.

Commit both `pyproject.toml` and `uv.lock`. Keep the virtual environment outside Git; `.venv` is ignored.

## Verify the artifact

From this directory (`cd 012`):

```bash
uv sync --locked
uv run --locked python environment_report.py
uv run --locked pytest
uv lock --check
```

The tested commands completed successfully: pytest reports **2 passing**. The current lock resolves pandas **3.1.0**, NumPy **2.5.4**, and pytest **9.2.0** under Python 3.12.3.

`uv sync --locked` installs exactly from the committed lockfile and fails if the project metadata and lockfile disagree. `uv run --locked` runs commands in that locked environment. `uv lock --check` verifies that the lockfile is current without rewriting it.

## Constraints versus resolutions

The version ranges in `pyproject.toml` are constraints: they describe what versions are allowed. The exact resolved versions and transitive dependencies are recorded in `uv.lock`. That is why both files belong in version control.

Update dependencies deliberately, rather than editing the lockfile by hand:

```bash
uv add <dep>
uv lock
# inspect the uv.lock diff, then retest
uv run --locked pytest
```

For an explicit pandas upgrade, use `uv lock --upgrade-package pandas`, inspect the resulting diff, and run the verification commands again. Never manually edit `uv.lock`.

A `pip freeze` output records packages installed in one environment; it does not resolve a universal lock for a project. See pip's guidance on [repeatable installs](https://pip.pypa.io/en/stable/topics/repeatable-installs/) and [`pip freeze`](https://pip.pypa.io/en/stable/cli/pip_freeze/). For the workflow used here, see the official [uv project guide](https://docs.astral.sh/uv/guides/projects/) and [uv locking and syncing documentation](https://docs.astral.sh/uv/concepts/projects/sync/).

## Reproducibility limits

A lockfile improves reproducibility, but it does not guarantee byte-for-byte identical results everywhere. Operating-system-specific artifacts, native libraries, hardware, package-index trust, and the Python version can still affect an installation. Match the pinned Python version as well as the lockfile, and use trusted package sources. The lockfile is not a security scan; review dependencies and update them regularly.
