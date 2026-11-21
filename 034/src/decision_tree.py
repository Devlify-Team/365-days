"""A small, dependency-free CART classifier using Gini impurity."""

from __future__ import annotations

import math
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


def _validated_labels(values: Sequence[Hashable]) -> list[Hashable]:
    if isinstance(values, (str, bytes)) or not isinstance(values, Sequence) or not values:
        raise ValueError("y must be a non-empty sequence of hashable class labels")
    labels = list(values)
    try:
        for label in labels:
            hash(label)
    except TypeError as error:
        raise ValueError("class labels must be hashable") from error
    return labels


def _label_key(label: Hashable) -> tuple[str, str]:
    """Provide a stable class order without requiring labels to compare to each other."""
    label_type = type(label)
    return label_type.__qualname__, repr(label)


def _gini(labels: Sequence[Hashable]) -> float:
    counts = Counter(labels)
    size = len(labels)
    return 1.0 - sum((count / size) ** 2 for count in counts.values())


def _midpoint(lower: float, upper: float) -> float:
    """Find a threshold between distinct values without overflowing."""
    if lower < 0.0 < upper:
        threshold = lower / 2.0 + upper / 2.0
    else:
        threshold = lower + (upper - lower) / 2.0
    # Adjacent floating-point values may have no representable midpoint.
    return threshold if lower <= threshold < upper else lower


@dataclass(frozen=True)
class _Node:
    counts: tuple[int, ...]
    feature_index: int | None = None
    threshold: float | None = None
    left: _Node | None = None
    right: _Node | None = None


class DecisionTreeClassifier:
    """Fit a deterministic binary-split classification tree using Gini gain.

    Features must be finite numeric values. Labels may be any hashable objects.
    The implementation uses exhaustive threshold search and is intended for
    learning and small datasets, not large-scale production workloads.
    """

    def __init__(
        self,
        max_depth: int | None = None,
        min_samples_split: int = 2,
        min_samples_leaf: int = 1,
        min_impurity_decrease: float = 0.0,
    ) -> None:
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

        self.max_depth = max_depth
        self.min_samples_split = min_samples_split
        self.min_samples_leaf = min_samples_leaf
        self.min_impurity_decrease = float(min_impurity_decrease)
        self.classes_: tuple[Hashable, ...] = ()
        self.n_features_in_: int | None = None
        self._root: _Node | None = None

    def fit(self, X: Sequence[Sequence[float]], y: Sequence[Hashable]) -> "DecisionTreeClassifier":
        """Build a tree from a rectangular feature matrix and class labels."""
        features, width = _matrix(X)
        labels = _validated_labels(y)
        if len(features) != len(labels):
            raise ValueError("X and y must contain the same number of samples")

        self.classes_ = tuple(sorted(set(labels), key=_label_key))
        self.n_features_in_ = width
        self._root = None
        self._root = self._build(features, labels, list(range(len(labels))), depth=0)
        return self

    def _counts(self, labels: Sequence[Hashable]) -> tuple[int, ...]:
        observed = Counter(labels)
        return tuple(observed.get(label, 0) for label in self.classes_)

    def _best_split(
        self,
        features: list[list[float]],
        labels: list[Hashable],
        indices: list[int],
    ) -> tuple[float, int, float] | None:
        parent_impurity = _gini([labels[index] for index in indices])
        best: tuple[float, int, float] | None = None
        best_gain = 0.0
        sample_count = len(indices)

        for feature_index in range(len(features[0])):
            distinct = sorted({features[index][feature_index] for index in indices})
            for lower, upper in zip(distinct, distinct[1:]):
                threshold = _midpoint(lower, upper)
                left_indices = [index for index in indices if features[index][feature_index] <= threshold]
                right_indices = [index for index in indices if features[index][feature_index] > threshold]
                if len(left_indices) < self.min_samples_leaf or len(right_indices) < self.min_samples_leaf:
                    continue
                left_labels = [labels[index] for index in left_indices]
                right_labels = [labels[index] for index in right_indices]
                weighted_impurity = (
                    len(left_indices) * _gini(left_labels) + len(right_indices) * _gini(right_labels)
                ) / sample_count
                gain = parent_impurity - weighted_impurity
                if gain > best_gain and gain >= self.min_impurity_decrease:
                    best_gain = gain
                    best = (gain, feature_index, threshold)
        return best

    def _build(
        self,
        features: list[list[float]],
        labels: list[Hashable],
        indices: list[int],
        depth: int,
    ) -> _Node:
        node_labels = [labels[index] for index in indices]
        counts = self._counts(node_labels)
        is_pure = sum(count > 0 for count in counts) == 1
        if (
            is_pure
            or (self.max_depth is not None and depth >= self.max_depth)
            or len(indices) < self.min_samples_split
        ):
            return _Node(counts=counts)

        split = self._best_split(features, labels, indices)
        if split is None:
            return _Node(counts=counts)
        _, feature_index, threshold = split
        left_indices = [index for index in indices if features[index][feature_index] <= threshold]
        right_indices = [index for index in indices if features[index][feature_index] > threshold]
        return _Node(
            counts=counts,
            feature_index=feature_index,
            threshold=threshold,
            left=self._build(features, labels, left_indices, depth + 1),
            right=self._build(features, labels, right_indices, depth + 1),
        )

    def _leaf(self, row: list[float]) -> _Node:
        if self._root is None:
            raise RuntimeError("fit the model before making predictions")
        node = self._root
        while node.feature_index is not None:
            if node.threshold is None or node.left is None or node.right is None:
                raise RuntimeError("the fitted tree is incomplete")
            node = node.left if row[node.feature_index] <= node.threshold else node.right
        return node

    def predict_proba(self, X: Sequence[Sequence[float]]) -> list[list[float]]:
        """Return per-class probabilities in the order of ``classes_``."""
        if self.n_features_in_ is None or self._root is None:
            raise RuntimeError("fit the model before calling predict_proba")
        features, _ = _matrix(X, width=self.n_features_in_)
        probabilities: list[list[float]] = []
        for row in features:
            counts = self._leaf(row).counts
            total = sum(counts)
            probabilities.append([count / total for count in counts])
        return probabilities

    def predict(self, X: Sequence[Sequence[float]]) -> list[Hashable]:
        """Predict the most frequent training class in each reached leaf."""
        return [self.classes_[max(range(len(row)), key=row.__getitem__)] for row in self.predict_proba(X)]
