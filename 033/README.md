# Logistic regression from scratch

- **Day:** 033
- **Month:** 2 — Classical ML Projects
- **Category:** Classification
- **Primary GitHub:** `ml-from-scratch`
- **Alternative:** scikit-learn
- **Slug:** `logistic-regression-from-scratch`

A dependency-free binary classifier trained with full-batch gradient descent. The implementation provides stable sigmoid and log-loss calculations, class probabilities, thresholded predictions, input validation, and a reproducible synthetic example. It is intentionally educational: multiclass classification and regularization are out of scope.

## Run the example and tests

From this folder, run:

```bash
PYTHONPATH=src python3 examples/train.py
PYTHONPATH=src python3 -m unittest discover -s tests -v
```

No third-party packages or datasets are needed.

## Model in brief

For feature vector `x`, the model computes a score `z = w · x + b`, then maps it to a probability with `σ(z) = 1 / (1 + exp(-z))`. Training minimizes binary cross-entropy. The gradient for each weight is the average of `(probability - label) × feature`; the intercept gradient is the average error.

The sigmoid and log-loss calculations are written to remain numerically stable for large positive or negative scores. This simple implementation does not regularize or standardize features; learning rate and feature scale still matter. For practical work, use [scikit-learn's `LogisticRegression`](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LogisticRegression.html), which offers optimized solvers, regularization, and broader classification support.
