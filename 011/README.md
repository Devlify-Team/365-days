# Day 11 — Setup a Data Science Project Template

**Workbook mapping:** Day 11 · Month 1: Foundations & GitHub Basics · Topic: Data Science · Primary: GitHub `datascience-template` · Alternate: Cookiecutter Data Science · Slug: `setup-data-science-project-template`.

## What this scaffold is

This is a small, hand-built teaching scaffold inspired by selected conventions from [Cookiecutter Data Science](https://cookiecutter-data-science.drivendata.org/). It is **not** the official Cookiecutter Data Science generator, and it does not install Cookiecutter, `ccds`, or any project dependencies. No remote repository is generated.

If you choose the official generator, follow the [official usage guide](https://cookiecutter-data-science.drivendata.org/using-the-template/) and make that decision yourself. The current v2 generator requires Python **3.10 or newer**; its documented install and invocation use `ccds`. The official source is the [Cookiecutter Data Science GitHub repository](https://github.com/drivendataorg/cookiecutter-data-science).

All directories, data conventions, and code examples here are starting points, not guarantees of correctness. Maintain `.gitignore` carefully, and never commit credentials or private data.

## Delivered tree

```text
011/
├── .gitignore
├── data/
│   ├── README.md
│   ├── external/
│   │   └── .gitkeep
│   ├── interim/
│   │   └── .gitkeep
│   ├── processed/
│   │   └── .gitkeep
│   └── raw/
│       └── .gitkeep
├── references/
│   └── README.md
├── models/
│   └── .gitkeep
├── notebooks/
│   └── README.md
├── pyproject.toml
├── reports/
│   └── figures/
│       └── .gitkeep
├── src/
│   └── ds_template/
│       ├── __init__.py
│       └── validate_csv.py
└── tests/
    └── test_validate_csv.py
```

`pyproject.toml` contains metadata only and declares Python `>=3.9` with zero runtime dependencies. This is not a reproducibly locked or installed environment. Day 12 separately covers reproducible environments.

`data/README.md` explains the raw, interim, processed, and external folders, their intended permissions, and that data is not included. `notebooks/README.md` explains the notebook convention. The `.gitignore` preserves `.gitkeep` placeholders while excluding actual files under `data/raw`, `data/interim`, `data/processed`, and `data/external`, plus model/report artifacts and `.env`.

## Run the offline tests

From the repository root:

```bash
PYTHONPATH=011/src python3 -B -m unittest discover -s 011/tests -p 'test_*.py' -v
```

The tests use only temporary parser fixtures. They do not download, generate, or analyze a dataset.

## Check a CSV schema

Use your own authorized local CSV file:

```bash
PYTHONPATH=011/src python3 -B -m ds_template.validate_csv /path/to/local.csv --required-columns id,value
```

Replace `id,value` with the real required headers for your project. This command performs a basic schema check only; passing it does **not** prove data quality, correctness, completeness, safety, or suitability for analysis. No actual analysis or dataset is included, and no simulated analysis data is provided.

## License and publishing

No license declaration is included intentionally. Before publishing or sharing this scaffold or any derived work, establish the applicable rights and choose an appropriate license. Also confirm that every dataset, model, notebook, and dependency you add may legally be used and redistributed.
