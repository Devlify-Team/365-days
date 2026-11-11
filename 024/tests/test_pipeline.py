import json

import pytest

from ml_template.pipeline import train_and_evaluate, validate_config


def test_validate_config_rejects_too_small_dataset():
    with pytest.raises(ValueError, match="at least 40"):
        validate_config({"n_samples": 20})


def test_validate_config_rejects_invalid_test_fraction():
    with pytest.raises(ValueError, match="strictly between"):
        validate_config({"test_size": 1.0})


def test_training_saves_model_and_metrics(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    metrics = train_and_evaluate(
        {"n_samples": 120, "test_size": 0.25, "random_state": 7, "max_iter": 300},
        output_dir=tmp_path / "models",
    )

    assert 0.0 <= metrics["accuracy"] <= 1.0
    assert metrics["n_train"] + metrics["n_test"] == 120
    assert metrics["random_state"] == 7
    assert (tmp_path / "models" / "classifier.joblib").is_file()
    saved = json.loads((tmp_path / "reports" / "metrics.json").read_text())
    assert saved == metrics
