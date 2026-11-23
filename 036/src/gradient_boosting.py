"""A small gradient-boosted tree regressor for squared-error loss."""

from __future__ import annotations

import math
from collections.abc import Sequence
from dataclasses import dataclass


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


def _targets(values: Sequence[float]) -> list[float]:
    if isinstance(values, (str, bytes)) or not isinstance(values, Sequence) or not values:
        raise ValueError("y must be a non-empty sequence of finite numeric targets")
    try:
        targets = [float(value) for value in values]
    except (TypeError, ValueError) as error:
        raise ValueError("y must contain only finite numeric targets") from error
    if not all(math.isfinite(value) for value in targets):
        raise ValueError("y must contain only finite numeric targets")
    return targets


def _mean(values: Sequence[float]) -> float:
    try:
        result = math.fsum(values) / len(values)
    except OverflowError as error:
        raise ValueError("targets are too large to compute a finite mean") from error
    if not math.isfinite(result):
        raise ValueError("targets are too large to compute a finite mean")
    return result


def _squared_error(values: Sequence[float], predictions: Sequence[float]) -> float:
    errors = [actual - predicted for actual, predicted in zip(values, predictions)]
    if not all(math.isfinite(error) for error in errors):
        return math.inf
    try:
        return math.fsum(error * error for error in errors) / len(errors)
    except OverflowError:
        return math.inf


def _midpoint(lower: float, upper: float) -> float:
    """Find a finite split threshold between two adjacent feature values."""
    if lower < 0.0 < upper:
        threshold = lower / 2.0 + upper / 2.0
    else:
        threshold = lower + (upper - lower) / 2.0
    return threshold if lower <= threshold < upper else lower


@dataclass(frozen=True)
class _Node:
    value: float
    feature_index: int | None = None
    threshold: float | None = None
    left: _Node | None = None
    right: _Node | None = None

    def predict(self, row: list[float]) -> float:
        node = self
        while node.feature_index is not None:
            if node.threshold is None or node.left is None or node.right is None:
                raise RuntimeError("the fitted regression tree is incomplete")
            node = node.left if row[node.feature_index] <= node.threshold else node.right
        return node.value


class _RegressionTree:
    """A small CART regressor that minimizes within-leaf squared error."""

    def __init__(self, max_depth: int, min_samples_split: int, min_samples_leaf: int) -> None:
        self.max_depth = max_depth
        self.min_samples_split = min_samples_split
        self.min_samples_leaf = min_samples_leaf
        self.root: _Node | None = None

    def fit(self, features: list[list[float]], targets: list[float]) -> None:
        self.root = self._build(features, targets, list(range(len(targets))), depth=0)

    def _best_split(
        self,
        features: list[list[float]],
        targets: list[float],
        indices: list[int],
    ) -> tuple[int, float] | None:
        parent_mean = _mean([targets[index] for index in indices])
        parent_sse = math.fsum((targets[index] - parent_mean) ** 2 for index in indices)
        best_sse = parent_sse
        best_split: tuple[int, float] | None = None

        for feature_index in range(len(features[0])):
            distinct = sorted({features[index][feature_index] for index in indices})
            for lower, upper in zip(distinct, distinct[1:]):
                threshold = _midpoint(lower, upper)
                left = [index for index in indices if features[index][feature_index] <= threshold]
                right = [index for index in indices if features[index][feature_index] > threshold]
                if len(left) < self.min_samples_leaf or len(right) < self.min_samples_leaf:
                    continue
                left_mean = _mean([targets[index] for index in left])
                right_mean = _mean([targets[index] for index in right])
                child_sse = math.fsum(
                    (targets[index] - left_mean) ** 2 for index in left
                ) + math.fsum((targets[index] - right_mean) ** 2 for index in right)
                # Strict comparison makes equal-gain tie-breaking deterministic.
                if child_sse < best_sse:
                    best_sse = child_sse
                    best_split = (feature_index, threshold)
        return best_split

    def _build(
        self,
        features: list[list[float]],
        targets: list[float],
        indices: list[int],
        depth: int,
    ) -> _Node:
        node_mean = _mean([targets[index] for index in indices])
        if depth >= self.max_depth or len(indices) < self.min_samples_split:
            return _Node(value=node_mean)
        split = self._best_split(features, targets, indices)
        if split is None:
            return _Node(value=node_mean)
        feature_index, threshold = split
        left_indices = [index for index in indices if features[index][feature_index] <= threshold]
        right_indices = [index for index in indices if features[index][feature_index] > threshold]
        return _Node(
            value=node_mean,
            feature_index=feature_index,
            threshold=threshold,
            left=self._build(features, targets, left_indices, depth + 1),
            right=self._build(features, targets, right_indices, depth + 1),
        )

    def predict_one(self, row: list[float]) -> float:
        if self.root is None:
            raise RuntimeError("fit the tree before making predictions")
        return self.root.predict(row)


class GradientBoostingRegressor:
    """Add shallow residual-fitting trees to minimize mean squared error.

    The initial prediction is the target mean. Each later tree is fit to the
    residuals (the negative gradient of half squared-error loss) and its output
    is shrunk by ``learning_rate`` before being added to the ensemble.
    """

    def __init__(
        self,
        n_estimators: int = 50,
        learning_rate: float = 0.1,
        max_depth: int = 2,
        min_samples_split: int = 2,
        min_samples_leaf: int = 1,
    ) -> None:
        if isinstance(n_estimators, bool) or not isinstance(n_estimators, int) or n_estimators < 1:
            raise ValueError("n_estimators must be a positive integer")
        if isinstance(learning_rate, bool) or not isinstance(learning_rate, (int, float)):
            raise ValueError("learning_rate must be a positive finite number")
        if not math.isfinite(learning_rate) or learning_rate <= 0:
            raise ValueError("learning_rate must be a positive finite number")
        if isinstance(max_depth, bool) or not isinstance(max_depth, int) or max_depth < 0:
            raise ValueError("max_depth must be a non-negative integer")
        if isinstance(min_samples_split, bool) or not isinstance(min_samples_split, int) or min_samples_split < 2:
            raise ValueError("min_samples_split must be an integer of at least 2")
        if isinstance(min_samples_leaf, bool) or not isinstance(min_samples_leaf, int) or min_samples_leaf < 1:
            raise ValueError("min_samples_leaf must be a positive integer")

        self.n_estimators = n_estimators
        self.learning_rate = float(learning_rate)
        self.max_depth = max_depth
        self.min_samples_split = min_samples_split
        self.min_samples_leaf = min_samples_leaf
        self.initial_prediction_: float | None = None
        self.n_features_in_: int | None = None
        self.estimators_: list[_RegressionTree] = []
        self.loss_history: list[float] = []

    def fit(self, X: Sequence[Sequence[float]], y: Sequence[float]) -> "GradientBoostingRegressor":
        """Fit sequential regression trees to the current model's residuals."""
        features, width = _matrix(X)
        targets = _targets(y)
        if len(features) != len(targets):
            raise ValueError("X and y must contain the same number of samples")

        initial_prediction = _mean(targets)
        predictions = [initial_prediction] * len(targets)
        initial_loss = _squared_error(targets, predictions)
        if not math.isfinite(initial_loss):
            raise ValueError("targets are too large for finite squared-error training")
        loss_history = [initial_loss]
        estimators: list[_RegressionTree] = []

        for _ in range(self.n_estimators):
            residuals = [actual - predicted for actual, predicted in zip(targets, predictions)]
            if not all(math.isfinite(value) for value in residuals):
                raise ValueError("training produced non-finite residuals")
            tree = _RegressionTree(
                max_depth=self.max_depth,
                min_samples_split=self.min_samples_split,
                min_samples_leaf=self.min_samples_leaf,
            )
            tree.fit(features, residuals)
            updated_predictions = [
                prediction + self.learning_rate * tree.predict_one(row)
                for row, prediction in zip(features, predictions)
            ]
            loss = _squared_error(targets, updated_predictions)
            if not math.isfinite(loss):
                raise ValueError("training produced non-finite loss")
            estimators.append(tree)
            predictions = updated_predictions
            loss_history.append(loss)

        self.initial_prediction_ = initial_prediction
        self.n_features_in_ = width
        self.estimators_ = estimators
        self.loss_history = loss_history
        return self

    def predict(self, X: Sequence[Sequence[float]]) -> list[float]:
        """Predict continuous targets by summing the initial value and tree outputs."""
        if self.initial_prediction_ is None or self.n_features_in_ is None:
            raise RuntimeError("fit the model before making predictions")
        features, _ = _matrix(X, width=self.n_features_in_)
        predictions: list[float] = []
        for row in features:
            value = self.initial_prediction_
            for tree in self.estimators_:
                value += self.learning_rate * tree.predict_one(row)
            if not math.isfinite(value):
                raise ValueError("prediction produced a non-finite value")
            predictions.append(value)
        return predictions
