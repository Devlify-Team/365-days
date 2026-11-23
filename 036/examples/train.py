"""Fit a small gradient-boosted regression model to a synthetic dataset."""

from gradient_boosting import GradientBoostingRegressor


X = [[float(value)] for value in range(8)]
y = [1.0, 2.0, 1.5, 4.0, 5.0, 7.5, 7.0, 9.0]

model = GradientBoostingRegressor(n_estimators=40, learning_rate=0.1, max_depth=2).fit(X, y)
predictions = model.predict(X)

print(f"Training MSE: {model.loss_history[0]:.3f} -> {model.loss_history[-1]:.3f}")
for features, actual, predicted in zip(X, y, predictions):
    print(f"x={features[0]:.1f} target={actual:.1f} prediction={predicted:.2f}")
