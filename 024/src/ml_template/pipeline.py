"""Reproducible, small tabular classification example for the ML template."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import joblib
from sklearn.datasets import make_classification
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


def validate_config(config: dict[str, Any]) -> None:
    """Reject settings that would make the demonstration invalid."""
    n_samples = config.get("n_samples", 300)
    test_size = config.get("test_size", 0.25)
    max_iter = config.get("max_iter", 1000)
    random_state = config.get("random_state", 42)

    if not isinstance(n_samples, int) or isinstance(n_samples, bool) or n_samples < 40:
        raise ValueError("n_samples must be an integer of at least 40")
    if not isinstance(test_size, (int, float)) or not 0 < test_size < 1:
        raise ValueError("test_size must be a number strictly between 0 and 1")
    if not isinstance(max_iter, int) or isinstance(max_iter, bool) or max_iter < 1:
        raise ValueError("max_iter must be a positive integer")
    if not isinstance(random_state, int) or isinstance(random_state, bool):
        raise ValueError("random_state must be an integer")


def train_and_evaluate(
    config: dict[str, Any], output_dir: Path | str = Path("models")
) -> dict[str, int | float]:
    """Train on generated data, score held-out rows, and save local artifacts."""
    validate_config(config)
    n_samples = config.get("n_samples", 300)
    test_size = config.get("test_size", 0.25)
    random_state = config.get("random_state", 42)
    max_iter = config.get("max_iter", 1000)

    features, target = make_classification(
        n_samples=n_samples,
        n_features=8,
        n_informative=5,
        n_redundant=1,
        random_state=random_state,
    )
    x_train, x_test, y_train, y_test = train_test_split(
        features,
        target,
        test_size=test_size,
        random_state=random_state,
        stratify=target,
    )

    model = Pipeline(
        [
            ("scale", StandardScaler()),
            ("classifier", LogisticRegression(max_iter=max_iter)),
        ]
    )
    model.fit(x_train, y_train)
    predictions = model.predict(x_test)
    metrics: dict[str, int | float] = {
        "accuracy": float(accuracy_score(y_test, predictions)),
        "n_train": int(len(y_train)),
        "n_test": int(len(y_test)),
        "random_state": random_state,
    }

    output_path = Path(output_dir)
    report_path = Path("reports")
    output_path.mkdir(parents=True, exist_ok=True)
    report_path.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, output_path / "classifier.joblib")
    (report_path / "metrics.json").write_text(
        json.dumps(metrics, indent=2) + "\n", encoding="utf-8"
    )
    return metrics
