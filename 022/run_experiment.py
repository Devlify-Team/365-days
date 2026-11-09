"""Fit a few toy ridge models and log runs to a local MLflow database."""

import csv
import json
import os
from pathlib import Path
import tempfile

import mlflow

from src.modeling import fit_ridge_line, rmse

ROOT = Path(__file__).resolve().parent


def read_rows(path):
    with path.open(newline="", encoding="utf-8") as source:
        return [{key: float(value) for key, value in row.items()} for row in csv.DictReader(source)]


def main():
    tracking_uri = os.environ.get("MLFLOW_TRACKING_URI", "sqlite:///mlflow.db")
    mlflow.set_tracking_uri(tracking_uri)
    mlflow.set_experiment("day-022-ridge-demo")
    train = read_rows(ROOT / "data" / "train.csv")
    validation = read_rows(ROOT / "data" / "validation.csv")

    for alpha in (0.0, 0.5, 2.0):
        model = fit_ridge_line(train, alpha=alpha)
        score = rmse(validation, model)
        with mlflow.start_run(run_name=f"ridge-alpha-{alpha}") as run:
            mlflow.log_params({"model": "ridge_line", "alpha": alpha, "training_rows": len(train)})
            mlflow.log_metric("validation_rmse", score)
            with tempfile.TemporaryDirectory() as directory:
                artifact = Path(directory) / "model.json"
                artifact.write_text(json.dumps(model, indent=2) + "\n", encoding="utf-8")
                mlflow.log_artifact(str(artifact), artifact_path="model")
            print(f"run_id={run.info.run_id} alpha={alpha} validation_rmse={score:.4f}")


if __name__ == "__main__":
    main()
