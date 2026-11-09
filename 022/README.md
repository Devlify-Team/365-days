# Day 22 — Experiment tracking setup

**Track:** ML Ops · **Month:** Month 1: Foundations & GitHub Basics · **Primary tool:** [MLflow](https://mlflow.org/) · **Alternatives:** Neptune, Comet · **Slug:** `experiment-tracking-setup`

## Goal

Set up a small, reproducible MLflow experiment for a one-variable ridge-regression model. The experiment compares three regularization strengths, records parameters and validation metrics, and stores a temporary model JSON artifact.

This exercise is intentionally lightweight: `src/modeling.py` contains pure-Python modeling utilities, while `run_experiment.py` trains and logs the runs. The CSV files in `data/` are explicitly illustrative toy data, not a production or benchmark dataset.

## Project files

```text
022/
├── .gitignore
├── data/
│   ├── train.csv                 # Illustrative toy data
│   └── validation.csv            # Illustrative toy data
├── src/
│   └── modeling.py               # Pure-Python one-variable ridge regression and RMSE
├── tests/
│   └── test_modeling.py          # unittest coverage for the modeling helpers
├── requirements.txt              # Includes mlflow==3.18.0
├── run_experiment.py             # Trains and logs three MLflow runs
└── README.md
```

## Setup and run

From the repository root:

```bash
cd 022
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python run_experiment.py
```

The runner uses `MLFLOW_TRACKING_URI` when it is set. Otherwise, it defaults to the local SQLite tracking store `sqlite:///mlflow.db`. It runs the ridge model with `alpha` values `0.0`, `0.5`, and `2.0`, and logs the model type, `alpha`, training-row count, validation RMSE, and a temporary model JSON artifact for each run:

- the `alpha` parameter;
- the validation RMSE metric; and
- a temporary model JSON artifact.

MLflow tracking records parameters, metrics, artifacts, and run metadata for later inspection. See the [MLflow Tracking documentation](https://mlflow.org/docs/latest/ml/tracking/) and the [Tracking API reference](https://mlflow.org/docs/latest/ml/tracking/tracking-api/). Validation here produced three logged runs, each with `model/model.json`; all four modeling tests passed. The database and artifacts stay local and are excluded from Git.

## View the MLflow UI

In the same `022` folder, with the virtual environment active, start the MLflow server:

```bash
mlflow server --port 5000 --backend-store-uri sqlite:///mlflow.db
```

Then visit [http://127.0.0.1:5000](http://127.0.0.1:5000) in a browser. The local SQLite setup follows MLflow's [local database tracking tutorial](https://mlflow.org/docs/latest/ml/tracking/tutorials/local-database/).

The following local tracking outputs are intentionally ignored and should not be committed:

```text
mlflow.db
mlartifacts/
mlruns/
```

## Tests

Run the pure-Python modeling tests with:

```bash
python -m unittest discover -s tests -p 'test_*.py'
```

## Use another tracking destination

To send runs to another MLflow tracking server or store, set `MLFLOW_TRACKING_URI` before running the experiment. For example:

```bash
MLFLOW_TRACKING_URI=http://127.0.0.1:5000 python run_experiment.py
```

The exact MLflow dependency used by this exercise is pinned to [`mlflow==3.18.0`](https://github.com/mlflow/mlflow/releases/tag/v3.18.0).
