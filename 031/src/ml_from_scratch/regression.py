"""A small, dependency-free full-batch linear regression estimator."""

from __future__ import annotations

import math
from collections.abc import Sequence


def _numeric_vector(values: Sequence[float], name: str) -> list[float]:
    if isinstance(values, (str, bytes)) or not isinstance(values, Sequence) or not values:
        raise ValueError(f"{name} must be a non-empty sequence")
    try:
        result = [float(value) for value in values]
    except (TypeError, ValueError) as error:
        raise ValueError(f"{name} must contain numeric values") from error
    if not all(math.isfinite(value) for value in result):
        raise ValueError(f"{name} must contain only finite values")
    return result


def _numeric_matrix(
    values: Sequence[Sequence[float]], expected_width: int | None = None
) -> tuple[list[list[float]], int]:
    if isinstance(values, (str, bytes)) or not isinstance(values, Sequence) or not values:
        raise ValueError("X must be a non-empty sequence of feature rows")

    rows: list[list[float]] = []
    width = expected_width
    for row_number, row in enumerate(values, start=1):
        if isinstance(row, (str, bytes)) or not isinstance(row, Sequence) or not row:
            raise ValueError(f"X row {row_number} must be a non-empty feature sequence")
        if width is None:
            width = len(row)
        if len(row) != width:
            raise ValueError("all feature rows must have the same number of columns")
        try:
            numeric_row = [float(value) for value in row]
        except (TypeError, ValueError) as error:
            raise ValueError(f"X row {row_number} must contain numeric values") from error
        if not all(math.isfinite(value) for value in numeric_row):
            raise ValueError("X must contain only finite values")
        rows.append(numeric_row)
    return rows, int(width)


class LinearRegressionGD:
    """Fit a linear model using full-batch gradient descent on mean squared error."""

    def __init__(self, learning_rate: float = 0.01, epochs: int = 1000) -> None:
        if isinstance(learning_rate, bool) or not isinstance(learning_rate, (int, float)):
            raise ValueError("learning_rate must be a positive finite number")
        if not math.isfinite(learning_rate) or learning_rate <= 0:
            raise ValueError("learning_rate must be a positive finite number")
        if isinstance(epochs, bool) or not isinstance(epochs, int) or epochs < 1:
            raise ValueError("epochs must be a positive integer")
        self.learning_rate = float(learning_rate)
        self.epochs = epochs
        self.weights: list[float] = []
        self.bias = 0.0
        self.n_features_in_: int | None = None
        self.loss_history: list[float] = []
        self._fitted = False

    def fit(self, X: Sequence[Sequence[float]], y: Sequence[float]) -> "LinearRegressionGD":
        """Estimate coefficients from rows of features and one target per row."""
        features, width = _numeric_matrix(X)
        targets = _numeric_vector(y, "y")
        if len(features) != len(targets):
            raise ValueError("X and y must contain the same number of samples")

        self.weights = [0.0] * width
        self.bias = 0.0
        self.n_features_in_ = width
        self.loss_history = []
        self._fitted = False
        sample_count = len(targets)

        for _ in range(self.epochs):
            errors = [
                sum(weight * value for weight, value in zip(self.weights, row))
                + self.bias
                - target
                for row, target in zip(features, targets)
            ]
            scale = 2.0 / sample_count
            weight_gradients = [
                scale * sum(error * row[column] for error, row in zip(errors, features))
                for column in range(width)
            ]
            bias_gradient = scale * sum(errors)
            self.weights = [
                weight - self.learning_rate * gradient
                for weight, gradient in zip(self.weights, weight_gradients)
            ]
            self.bias -= self.learning_rate * bias_gradient

            updated_errors = [
                sum(weight * value for weight, value in zip(self.weights, row))
                + self.bias
                - target
                for row, target in zip(features, targets)
            ]
            loss = sum(error * error for error in updated_errors) / sample_count
            if not math.isfinite(loss):
                raise ValueError("training diverged; reduce the learning rate or scale the features")
            self.loss_history.append(loss)

        self._fitted = True
        return self

    def predict(self, X: Sequence[Sequence[float]]) -> list[float]:
        """Predict targets for rows with the same features used during fitting."""
        if not self._fitted or self.n_features_in_ is None:
            raise RuntimeError("fit the model before calling predict")
        features, _ = _numeric_matrix(X, expected_width=self.n_features_in_)
        return [
            sum(weight * value for weight, value in zip(self.weights, row)) + self.bias
            for row in features
        ]
