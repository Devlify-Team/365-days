"""Dependency-free linear model helpers used by the MLflow tracking demo."""

import math


def fit_ridge_line(rows, alpha=0.0):
    """Fit a one-feature ridge line with an unpenalized intercept."""
    if alpha < 0:
        raise ValueError("alpha must be non-negative")
    if len(rows) < 2:
        raise ValueError("at least two training rows are required")
    xs = [float(row["x"]) for row in rows]
    ys = [float(row["y"]) for row in rows]
    mean_x = sum(xs) / len(xs)
    mean_y = sum(ys) / len(ys)
    denominator = sum((x - mean_x) ** 2 for x in xs) + alpha
    if denominator == 0:
        raise ValueError("training x values must not all be equal")
    slope = sum((x - mean_x) * (y - mean_y) for x, y in zip(xs, ys)) / denominator
    return {"slope": slope, "intercept": mean_y - slope * mean_x}


def rmse(rows, model):
    """Calculate root mean squared error over labeled rows."""
    if not rows:
        raise ValueError("at least one validation row is required")
    return math.sqrt(sum((row["y"] - (model["slope"] * row["x"] + model["intercept"])) ** 2 for row in rows) / len(rows))
