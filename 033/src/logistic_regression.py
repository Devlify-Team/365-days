"""Educational binary logistic regression using full-batch gradient descent."""

from __future__ import annotations

import math
from collections.abc import Sequence


def sigmoid(value: float) -> float:
    """Compute the logistic sigmoid without overflowing the exponential."""
    if value >= 0:
        exponent = math.exp(-value)
        return 1.0 / (1.0 + exponent)
    exponent = math.exp(value)
    return exponent / (1.0 + exponent)


def _matrix(values: Sequence[Sequence[float]], width: int | None = None) -> tuple[list[list[float]], int]:
    if isinstance(values, (str, bytes)) or not isinstance(values, Sequence) or not values:
        raise ValueError("X must be a non-empty sequence of feature rows")
    rows: list[list[float]] = []
    for index, row in enumerate(values, start=1):
        if isinstance(row, (str, bytes)) or not isinstance(row, Sequence) or not row:
            raise ValueError(f"X row {index} must be a non-empty sequence")
        if width is None:
            width = len(row)
        if len(row) != width:
            raise ValueError("all rows must have the same number of features")
        try:
            converted = [float(value) for value in row]
        except (TypeError, ValueError) as error:
            raise ValueError(f"X row {index} must contain numeric values") from error
        if not all(math.isfinite(value) for value in converted):
            raise ValueError("X must contain only finite values")
        rows.append(converted)
    return rows, int(width)


def _labels(values: Sequence[float]) -> list[int]:
    if isinstance(values, (str, bytes)) or not isinstance(values, Sequence) or not values:
        raise ValueError("y must be a non-empty sequence of binary labels")
    try:
        converted = [float(value) for value in values]
    except (TypeError, ValueError) as error:
        raise ValueError("y must contain only 0 or 1") from error
    if not all(math.isfinite(value) and value in (0.0, 1.0) for value in converted):
        raise ValueError("y must contain only 0 or 1")
    return [int(value) for value in converted]


def _binary_log_loss(logits: Sequence[float], labels: Sequence[int]) -> float:
    """Compute mean binary cross-entropy directly from logits."""
    terms = [
        max(score, 0.0) - score * label + math.log1p(math.exp(-abs(score)))
        for score, label in zip(logits, labels)
    ]
    return sum(terms) / len(terms)


class LogisticRegressionGD:
    """Fit an unregularized binary logistic model by full-batch gradient descent."""

    def __init__(
        self,
        learning_rate: float = 0.1,
        epochs: int = 1000,
        threshold: float = 0.5,
    ) -> None:
        if isinstance(learning_rate, bool) or not isinstance(learning_rate, (int, float)):
            raise ValueError("learning_rate must be a positive finite number")
        if not math.isfinite(learning_rate) or learning_rate <= 0:
            raise ValueError("learning_rate must be a positive finite number")
        if isinstance(epochs, bool) or not isinstance(epochs, int) or epochs < 1:
            raise ValueError("epochs must be a positive integer")
        if isinstance(threshold, bool) or not isinstance(threshold, (int, float)):
            raise ValueError("threshold must be strictly between 0 and 1")
        if not math.isfinite(threshold) or not 0 < threshold < 1:
            raise ValueError("threshold must be strictly between 0 and 1")
        self.learning_rate = float(learning_rate)
        self.epochs = epochs
        self.threshold = float(threshold)
        self.weights: list[float] = []
        self.intercept = 0.0
        self.n_features_in_: int | None = None
        self.loss_history: list[float] = []
        self._fitted = False

    def fit(self, X: Sequence[Sequence[float]], y: Sequence[float]) -> "LogisticRegressionGD":
        """Learn weights from a rectangular feature matrix and binary labels."""
        features, width = _matrix(X)
        labels = _labels(y)
        if len(features) != len(labels):
            raise ValueError("X and y must contain the same number of samples")
        if len(set(labels)) != 2:
            raise ValueError("training labels must include both classes 0 and 1")

        self.weights = [0.0] * width
        self.intercept = 0.0
        self.n_features_in_ = width
        self.loss_history = []
        self._fitted = False
        sample_count = len(labels)

        for _ in range(self.epochs):
            logits = [
                sum(weight * value for weight, value in zip(self.weights, row)) + self.intercept
                for row in features
            ]
            errors = [sigmoid(score) - label for score, label in zip(logits, labels)]
            gradients = [
                sum(error * row[column] for error, row in zip(errors, features)) / sample_count
                for column in range(width)
            ]
            bias_gradient = sum(errors) / sample_count
            self.weights = [
                weight - self.learning_rate * gradient
                for weight, gradient in zip(self.weights, gradients)
            ]
            self.intercept -= self.learning_rate * bias_gradient

            updated_logits = [
                sum(weight * value for weight, value in zip(self.weights, row)) + self.intercept
                for row in features
            ]
            loss = _binary_log_loss(updated_logits, labels)
            if not math.isfinite(loss):
                raise ValueError("training diverged; reduce learning_rate or scale the features")
            self.loss_history.append(loss)

        self._fitted = True
        return self

    def predict_proba(self, X: Sequence[Sequence[float]]) -> list[float]:
        """Return estimated probabilities for the positive class (label 1)."""
        if not self._fitted or self.n_features_in_ is None:
            raise RuntimeError("fit the model before calling predict_proba")
        features, _ = _matrix(X, width=self.n_features_in_)
        return [
            sigmoid(sum(weight * value for weight, value in zip(self.weights, row)) + self.intercept)
            for row in features
        ]

    def predict(self, X: Sequence[Sequence[float]], threshold: float | None = None) -> list[int]:
        """Convert positive-class probabilities to labels using a threshold."""
        cutoff = self.threshold if threshold is None else threshold
        if isinstance(cutoff, bool) or not isinstance(cutoff, (int, float)):
            raise ValueError("threshold must be strictly between 0 and 1")
        if not math.isfinite(cutoff) or not 0 < cutoff < 1:
            raise ValueError("threshold must be strictly between 0 and 1")
        return [int(probability >= cutoff) for probability in self.predict_proba(X)]
