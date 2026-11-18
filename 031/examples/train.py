"""Fit a known linear relationship with the educational gradient-descent model."""

from ml_from_scratch import LinearRegressionGD


X = [[0.0], [1.0], [2.0], [3.0], [4.0]]
y = [1.0, 3.0, 5.0, 7.0, 9.0]  # y = 2x + 1

model = LinearRegressionGD(learning_rate=0.03, epochs=1500).fit(X, y)
print(f"weight: {model.weights[0]:.4f}")
print(f"bias: {model.bias:.4f}")
print(f"final MSE: {model.loss_history[-1]:.8f}")
print(f"prediction at x=5: {model.predict([[5.0]])[0]:.4f}")
