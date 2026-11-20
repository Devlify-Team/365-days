"""Train on a tiny synthetic dataset and print probabilities and predictions."""

from logistic_regression import LogisticRegressionGD


X = [[-2.0, -1.0], [-1.0, -2.0], [-1.0, -1.0], [1.0, 1.0], [1.0, 2.0], [2.0, 1.0]]
y = [0, 0, 0, 1, 1, 1]

model = LogisticRegressionGD(learning_rate=0.1, epochs=1500).fit(X, y)
probabilities = model.predict_proba(X)
predictions = model.predict(X)
accuracy = sum(prediction == label for prediction, label in zip(predictions, y)) / len(y)
print(f"final log loss: {model.loss_history[-1]:.6f}")
print(f"probabilities: {[round(value, 3) for value in probabilities]}")
print(f"predictions: {predictions}")
print(f"training accuracy: {accuracy:.1%} (synthetic data only)")
