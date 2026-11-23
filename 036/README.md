# Gradient boosting implementation

- **Day:** 036
- **Month:** 2 — Classical ML Projects
- **Category:** Ensemble
- **Primary GitHub:** `ml-from-scratch`
- **Alternative:** XGBoost
- **Slug:** `gradient-boosting-implementation`

A dependency-free gradient boosting regressor for numeric targets and finite numeric features. It starts from the target mean, then adds shallow regression trees fit sequentially to the current residuals. The learning rate shrinks each tree's contribution; the model records mean-squared error after each boosting stage.

## Run the example and tests

From this folder, run:

```bash
PYTHONPATH=src python3 examples/train.py
PYTHONPATH=src python3 -m unittest discover -s tests -v
```

No third-party packages or datasets are needed.

## Model in brief

For squared-error loss, the negative gradient is proportional to the residual `target − prediction`. At each stage the implementation fits a CART-style regression tree to those residuals. Its leaf values are the mean residual in that leaf, which minimizes squared error there; the model adds `learning_rate × tree_output` to every current prediction. Trees greedily choose numeric thresholds that reduce within-leaf squared error. `max_depth`, `min_samples_split`, and `min_samples_leaf` constrain tree size.

This project covers the regression / squared-error case only. It does not implement classification, other loss functions, row subsampling, categorical or missing-value handling, or optimized split search. For a production implementation with more losses and options, see [scikit-learn's `GradientBoostingRegressor`](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.GradientBoostingRegressor.html); XGBoost is another widely used gradient-boosted tree library.
