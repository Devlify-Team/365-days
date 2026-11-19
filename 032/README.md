# Ridge and Lasso implementation

- **Day:** 032
- **Month:** 2 — Classical ML Projects
- **Category:** Regression
- **Primary GitHub:** `regularization`
- **Alternative:** scikit-learn
- **Slug:** `ridge-and-lasso-implementation`

A dependency-free extension of the from-scratch regression exercise: one estimator supports both L2 (Ridge) and L1 (Lasso) penalties. It leaves the intercept unpenalized, records the objective at each epoch, and uses soft-thresholding for the Lasso update so coefficients can become exactly zero.

## Run the comparison and tests

From this folder, run:

```bash
PYTHONPATH=src python3 examples/compare.py
PYTHONPATH=src python3 -m unittest discover -s tests -v
```

The example uses a small deterministic dataset; no packages or data downloads are needed.

## Objective and updates

This project defines its objective as `MSE + alpha × penalty`, where `MSE = mean((prediction - target)²)`. Ridge uses `sum(weight²)` and updates each weight with the L2 gradient. Lasso uses `sum(abs(weight))` and applies a soft-threshold after the MSE gradient step. The intercept is excluded from both penalties. Larger `alpha` applies stronger shrinkage; Lasso can set small weights exactly to zero. Feature scaling and learning rate affect convergence, so inspect the recorded objective rather than assuming every setting will train well.

The formulas follow the standard L2/L1 regularization ideas, but this starter's mean-squared-error scaling differs from scikit-learn's documented objective. Do not compare `alpha` values directly. For production, use [scikit-learn Ridge](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.Ridge.html) or [Lasso](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.Lasso.html); those estimators provide mature solvers and broader input support.
