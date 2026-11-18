# Linear regression from scratch

- **Day:** 031
- **Month:** 2 — Classical ML Projects
- **Category:** Regression
- **Primary GitHub:** `ml-from-scratch`
- **Alternative:** scikit-learn
- **Slug:** `linear-regression-from-scratch`

A dependency-free Python implementation of full-batch gradient descent for linear regression. It learns a bias and one or more feature weights, records mean-squared-error history, and checks data shapes and numeric values. A tiny synthetic example makes the training process reproducible.

## Run the example and tests

From this folder, run:

```bash
PYTHONPATH=src python3 examples/train.py
PYTHONPATH=src python3 -m unittest discover -s tests -v
```

No third-party packages or dataset downloads are required.

## How the update works

For input row `x`, the model predicts `ŷ = w · x + b`. It minimizes mean squared error with gradient updates:

```text
MSE = (1/n) Σ(ŷᵢ - yᵢ)²
wⱼ ← wⱼ - η (2/n) Σ((ŷᵢ - yᵢ) xᵢⱼ)
b  ← b  - η (2/n) Σ(ŷᵢ - yᵢ)
```

The code uses batch updates: it calculates each gradient from the current weights, then applies the update. Feature scale and learning rate affect convergence; inspect the loss history and scale real features before training. This is an educational implementation, not a production optimizer. For a maintained estimator, compare with [scikit-learn's `LinearRegression`](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LinearRegression.html), which solves ordinary least squares.
