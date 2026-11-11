# Create a machine-learning project template

- **Day:** 024
- **Month:** 1 — Foundations & GitHub Basics
- **Category:** Templates
- **Primary GitHub:** `ml-template`
- **Alternative:** Cookiecutter ML
- **Slug:** `create-a-ml-project-template`

A compact, reusable starter for small tabular classification projects. The example trains a scikit-learn pipeline on a deterministic synthetic dataset, evaluates it on a held-out test split, and writes a local model and metrics report. No external dataset or credentials are needed.

## Project structure

- `configs/default.json` — sample run settings.
- `data/raw/` — place original inputs here; never silently replace source data.
- `data/processed/` — place derived datasets here; document the transformation that produced them.
- `src/ml_template/pipeline.py` — validates configuration, generates reproducible sample data, splits it, trains a scaled logistic-regression pipeline, evaluates accuracy, and saves outputs.
- `src/ml_template/cli.py` — loads JSON settings and exposes the `ml-template` command.
- `models/` — generated model artifacts (ignored by Git).
- `reports/` — generated metrics (ignored by Git).
- `tests/` — fast checks for configuration validation and the complete training run.
- `TEMPLATE_CHECKLIST.md` — practical steps to adapt the scaffold to a real dataset.

## Run it

From the repository root:

```bash
cd 024
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e '.[test]'
python -m pytest
ml-template
# Or: python -m ml_template
```

A successful run prints JSON metrics and creates `models/classifier.joblib` and `reports/metrics.json`. Those generated files are deliberately ignored by Git. Change settings in `configs/default.json`; rerunning intentionally refreshes these local outputs.

The example splits data before fitting a preprocessing-and-estimator pipeline, so the scaler is fit only on training data. Its generated data is only a smoke-test example—not a useful benchmark or evidence of real-world model quality. Before adapting this starter, use the checklist to choose suitable data, metrics, validation, and model governance.

## References

The folder organization follows the practical separation of raw and processed data, source code, models, and reports in [Cookiecutter Data Science's template guide](https://cookiecutter-data-science.drivendata.org/using-the-template/). The model workflow uses scikit-learn's documented [pipelines and held-out model evaluation](https://scikit-learn.org/stable/getting_started.html).
