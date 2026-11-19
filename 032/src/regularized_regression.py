"""Educational Ridge and Lasso regression using pure-Python batch updates."""

from __future__ import annotations

import math
from collections.abc import Sequence


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


def _vector(values: Sequence[float], name: str) -> list[float]:
    if isinstance(values, (str, bytes)) or not isinstance(values, Sequence) or not values:
        raise ValueError(f"{name} must be a non-empty sequence")
    try:
        result = [float(value) for value in values]
    except (TypeError, ValueError) as error:
        raise ValueError(f"{name} must contain numeric values") from error
    if not all(math.isfinite(value) for value in result):
        raise ValueError(f"{name} must contain only finite values")
    return result


class RegularizedLinearRegression:
    """Fit a single-target Ridge or Lasso model with full-batch updates.

    The objective is mean squared error plus ``alpha`` times the selected
    coefficient penalty. The intercept is not regularized.
    """

    def __init__(
        self,
        method: str = "ridge",
        alpha: float = 1.0,
        learning_rate: float = 0.01,
        epochs: int = 1000,
    ) -> None:
        if method not in {"ridge", "lasso"}:
            raise ValueError("method must be 'ridge' or 'lasso'")
        if isinstance(alpha, bool) or not isinstance(alpha, (int, float)):
            raise ValueError("alpha must be a non-negative finite number")
        if not math.isfinite(alpha) or alpha < 0:
            raise ValueError("alpha must be a non-negative finite number")
        if isinstance(learning_rate, bool) or not isinstance(learning_rate, (int, float)):
            raise ValueError("learning_rate must be a positive finite number")
        if not math.isfinite(learning_rate) or learning_rate <= 0:
            raise ValueError("learning_rate must be a positive finite number")
        if isinstance(epochs, bool) or not isinstance(epochs, int) or epochs < 1:
            raise ValueError("epochs must be a positive integer")
        self.method = method
        self.alpha = float(alpha)
        self.learning_rate = float(learning_rate)
        self.epochs = epochs
        self.weights: list[float] = []
        self.intercept = 0.0
        self.n_features_in_: int | None = None
        self.objective_history: list[float] = []
        self._fitted = False

    def _objective(self, features: list[list[float]], targets: list[float]) -> float:
        errors = [
            sum(weight * value for weight, value in zip(self.weights, row))
            + self.intercept
            - target
            for row, target in zip(features, targets)
        ]
        mse = sum(error * error for error in errors) / len(targets)
        if self.method == "ridge":
            penalty = sum(weight * weight for weight in self.weights)
        else:
            penalty = sum(abs(weight) for weight in self.weights)
        return mse + self.alpha * penalty

    def fit(self, X: Sequence[Sequence[float]], y: Sequence[float]) -> "RegularizedLinearRegression":
        """Fit weights using the selected penalty and full-batch gradients."""
        features, width = _matrix(X)
        targets = _vector(y, "y")
        if len(features) != len(targets):
            raise ValueError("X and y must contain the same number of samples")

        self.weights = [0.0] * width
        self.intercept = 0.0
        self.n_features_in_ = width
        self.objective_history = []
        self._fitted = False
        sample_count = len(targets)
        scale = 2.0 / sample_count

        for _ in range(self.epochs):
            errors = [
                sum(weight * value for weight, value in zip(self.weights, row))
                + self.intercept
                - target
                for row, target in zip(features, targets)
            ]
            gradients = [
                scale * sum(error * row[column] for error, row in zip(errors, features))
                for column in range(width)
            ]
            bias_gradient = scale * sum(errors)
            if self.method == "ridge":
                self.weights = [
                    weight - self.learning_rate * (gradient + 2.0 * self.alpha * weight)
                    for weight, gradient in zip(self.weights, gradients)
                ]
            else:
                stepped = [
                    weight - self.learning_rate * gradient
                    for weight, gradient in zip(self.weights, gradients)
                ]
                threshold = self.learning_rate * self.alpha
                self.weights = [
                    math.copysign(max(abs(value) - threshold, 0.0), value)
                    for value in stepped
                ]
            self.intercept -= self.learning_rate * bias_gradient
            objective = self._objective(features, targets)
            if not math.isfinite(objective):
                raise ValueError("training diverged; reduce learning_rate or scale the features")
            self.objective_history.append(objective)

        self._fitted = True
        return self

    def predict(self, X: Sequence[Sequence[float]]) -> list[float]:
        """Predict one numeric target for each input row."""
        if not self._fitted or self.n_features_in_ is None:
            raise RuntimeError("fit the model before calling predict")
        features, _ = _matrix(X, width=self.n_features_in_)
        return [
            sum(weight * value for weight, value in zip(self.weights, row)) + self.intercept
            for row in features
        ]
