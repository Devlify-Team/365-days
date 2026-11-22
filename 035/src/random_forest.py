"""A small, dependency-free random forest classifier built from scratch."""

from __future__ import annotations

import math
import random
from collections import Counter
from collections.abc import Hashable, Sequence
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


def _labels(values: Sequence[Hashable]) -> list[Hashable]:
    if isinstance(values, (str, bytes)) or not isinstance(values, Sequence) or not values:
        raise ValueError("y must be a non-empty sequence of hashable class labels")
    result = list(values)
    try:
        for label in result:
            hash(label)
    except TypeError as error:
        raise ValueError("class labels must be hashable") from error
    return result


def _label_key(label: Hashable) -> tuple[str, str]:
    """Sort labels consistently without requiring unlike labels to compare."""
    return type(label).__qualname__, repr(label)


def _gini(labels: Sequence[Hashable]) -> float:
    counts = Counter(labels)
    size = len(labels)
    return 1.0 - sum((count / size) ** 2 for count in counts.values())


def _midpoint(lower: float, upper: float) -> float:
    if lower < 0.0 < upper:
        threshold = lower / 2.0 + upper / 2.0
    else:
        threshold = lower + (upper - lower) / 2.0
    return threshold if lower <= threshold < upper else lower


@dataclass(frozen=True)
class _Node:
    counts: tuple[int, ...]
    feature_index: int | None = None
    threshold: float | None = None
    left: _Node | None = None
    right: _Node | None = None


class _DecisionTree:
    """Internal Gini tree that randomly considers a subset of features per node."""

    def __init__(
        self,
        classes: tuple[Hashable, ...],
        max_features: int,
        max_depth: int | None,
        min_samples_split: int,
        min_samples_leaf: int,
        min_impurity_decrease: float,
        rng: random.Random,
    ) -> None:
        self.classes = classes
        self.max_features = max_features
        self.max_depth = max_depth
        self.min_samples_split = min_samples_split
        self.min_samples_leaf = min_samples_leaf
        self.min_impurity_decrease = min_impurity_decrease
        self.rng = rng
        self.root: _Node | None = None

    def fit(self, features: list[list[float]], labels: list[Hashable], indices: list[int]) -> None:
        self.root = self._build(features, labels, indices, depth=0)

    def _counts(self, labels: Sequence[Hashable]) -> tuple[int, ...]:
        observed = Counter(labels)
        return tuple(observed.get(label, 0) for label in self.classes)

    def _best_split(
        self,
        features: list[list[float]],
        labels: list[Hashable],
        indices: list[int],
    ) -> tuple[int, float] | None:
        parent_impurity = _gini([labels[index] for index in indices])
        best_gain = 0.0
        best_split: tuple[int, float] | None = None
        sample_count = len(indices)
        sampled_features = self.rng.sample(range(len(features[0])), self.max_features)

        for feature_index in sampled_features:
            distinct = sorted({features[index][feature_index] for index in indices})
            for lower, upper in zip(distinct, distinct[1:]):
                threshold = _midpoint(lower, upper)
                left = [index for index in indices if features[index][feature_index] <= threshold]
                right = [index for index in indices if features[index][feature_index] > threshold]
                if len(left) < self.min_samples_leaf or len(right) < self.min_samples_leaf:
                    continue
                weighted_impurity = (
                    len(left) * _gini([labels[index] for index in left])
                    + len(right) * _gini([labels[index] for index in right])
                ) / sample_count
                gain = parent_impurity - weighted_impurity
                if gain > best_gain and gain >= self.min_impurity_decrease:
                    best_gain = gain
                    best_split = (feature_index, threshold)
        return best_split

    def _build(
        self,
        features: list[list[float]],
        labels: list[Hashable],
        indices: list[int],
        depth: int,
    ) -> _Node:
        node_labels = [labels[index] for index in indices]
        counts = self._counts(node_labels)
        pure = sum(count > 0 for count in counts) == 1
        if (
            pure
            or (self.max_depth is not None and depth >= self.max_depth)
            or len(indices) < self.min_samples_split
        ):
            return _Node(counts=counts)

        split = self._best_split(features, labels, indices)
        if split is None:
            return _Node(counts=counts)
        feature_index, threshold = split
        left_indices = [index for index in indices if features[index][feature_index] <= threshold]
        right_indices = [index for index in indices if features[index][feature_index] > threshold]
        return _Node(
            counts=counts,
            feature_index=feature_index,
            threshold=threshold,
            left=self._build(features, labels, left_indices, depth + 1),
            right=self._build(features, labels, right_indices, depth + 1),
        )

    def predict_proba_one(self, row: list[float]) -> list[float]:
        if self.root is None:
            raise RuntimeError("the fitted tree has no root")
        node = self.root
        while node.feature_index is not None:
            if node.threshold is None or node.left is None or node.right is None:
                raise RuntimeError("the fitted tree is incomplete")
            node = node.left if row[node.feature_index] <= node.threshold else node.right
        total = sum(node.counts)
        return [count / total for count in node.counts]


class RandomForestClassifier:
    """Train bootstrap-sampled Gini trees and average their class probabilities.

    This transparent implementation accepts finite numeric features and
    hashable labels. It is intended for learning and small datasets; use an
    optimized library for large or production workloads.
    """

    def __init__(
        self,
        n_estimators: int = 25,
        max_depth: int | None = None,
        min_samples_split: int = 2,
        min_samples_leaf: int = 1,
        max_features: int | str | None = "sqrt",
        min_impurity_decrease: float = 0.0,
        random_state: int | None = None,
    ) -> None:
        if isinstance(n_estimators, bool) or not isinstance(n_estimators, int) or n_estimators < 1:
            raise ValueError("n_estimators must be a positive integer")
        if max_depth is not None and (
            isinstance(max_depth, bool) or not isinstance(max_depth, int) or max_depth < 0
        ):
            raise ValueError("max_depth must be a non-negative integer or None")
        if isinstance(min_samples_split, bool) or not isinstance(min_samples_split, int) or min_samples_split < 2:
            raise ValueError("min_samples_split must be an integer of at least 2")
        if isinstance(min_samples_leaf, bool) or not isinstance(min_samples_leaf, int) or min_samples_leaf < 1:
            raise ValueError("min_samples_leaf must be a positive integer")
        if isinstance(min_impurity_decrease, bool) or not isinstance(min_impurity_decrease, (int, float)):
            raise ValueError("min_impurity_decrease must be a finite non-negative number")
        if not math.isfinite(min_impurity_decrease) or min_impurity_decrease < 0:
            raise ValueError("min_impurity_decrease must be a finite non-negative number")
        if isinstance(max_features, bool) or not (
            max_features is None
            or (isinstance(max_features, int) and max_features >= 1)
            or max_features in ("sqrt", "log2")
        ):
            raise ValueError("max_features must be a positive integer, 'sqrt', 'log2', or None")
        if random_state is not None and (
            isinstance(random_state, bool) or not isinstance(random_state, int)
        ):
            raise ValueError("random_state must be an integer or None")

        self.n_estimators = n_estimators
        self.max_depth = max_depth
        self.min_samples_split = min_samples_split
        self.min_samples_leaf = min_samples_leaf
        self.max_features = max_features
        self.min_impurity_decrease = float(min_impurity_decrease)
        self.random_state = random_state
        self.classes_: tuple[Hashable, ...] = ()
        self.n_features_in_: int | None = None
        self.estimators_: list[_DecisionTree] = []

    def _feature_count(self, n_features: int) -> int:
        if self.max_features is None:
            return n_features
        if isinstance(self.max_features, int):
            if self.max_features > n_features:
                raise ValueError("max_features cannot exceed the number of input features")
            return self.max_features
        if self.max_features == "sqrt":
            return max(1, math.isqrt(n_features))
        return max(1, int(math.log2(n_features)))

    def fit(self, X: Sequence[Sequence[float]], y: Sequence[Hashable]) -> "RandomForestClassifier":
        """Draw one bootstrap sample per tree and fit its randomized split tree."""
        features, width = _matrix(X)
        labels = _labels(y)
        if len(features) != len(labels):
            raise ValueError("X and y must contain the same number of samples")
        feature_count = self._feature_count(width)
        classes = tuple(sorted(set(labels), key=_label_key))
        master_rng = random.Random(self.random_state)
        estimators: list[_DecisionTree] = []

        for _ in range(self.n_estimators):
            tree_seed = master_rng.getrandbits(64)
            sampling_rng = random.Random(tree_seed)
            bootstrap_indices = [sampling_rng.randrange(len(features)) for _ in features]
            split_rng = random.Random(sampling_rng.getrandbits(64))
            tree = _DecisionTree(
                classes=classes,
                max_features=feature_count,
                max_depth=self.max_depth,
                min_samples_split=self.min_samples_split,
                min_samples_leaf=self.min_samples_leaf,
                min_impurity_decrease=self.min_impurity_decrease,
                rng=split_rng,
            )
            tree.fit(features, labels, bootstrap_indices)
            estimators.append(tree)

        self.classes_ = classes
        self.n_features_in_ = width
        self.estimators_ = estimators
        return self

    def predict_proba(self, X: Sequence[Sequence[float]]) -> list[list[float]]:
        """Average each tree's leaf class frequencies in ``classes_`` order."""
        if self.n_features_in_ is None or not self.estimators_:
            raise RuntimeError("fit the model before calling predict_proba")
        features, _ = _matrix(X, width=self.n_features_in_)
        predictions: list[list[float]] = []
        for row in features:
            averaged = [0.0] * len(self.classes_)
            for tree in self.estimators_:
                for class_index, probability in enumerate(tree.predict_proba_one(row)):
                    averaged[class_index] += probability / len(self.estimators_)
            predictions.append(averaged)
        return predictions

    def predict(self, X: Sequence[Sequence[float]]) -> list[Hashable]:
        """Return the class with the largest mean probability; ties use class order."""
        return [
            self.classes_[max(range(len(row)), key=row.__getitem__)]
            for row in self.predict_proba(X)
        ]
