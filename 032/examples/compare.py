"""Compare Ridge and Lasso on a deterministic, two-feature toy dataset."""

from regularized_regression import RegularizedLinearRegression


X = [[float(x), float(4 * x)] for x in range(-5, 6)]
y = [1.0 + 2.0 * row[0] for row in X]

for method in ("ridge", "lasso"):
    model = RegularizedLinearRegression(
        method=method, alpha=0.15, learning_rate=0.001, epochs=3000
    ).fit(X, y)
    print(
        f"{method:5} weights={model.weights!r} intercept={model.intercept:.4f} "
        f"objective={model.objective_history[-1]:.6f}"
    )
