# Random forest from scratch

- **Day:** 035
- **Month:** 2 — Classical ML Projects
- **Category:** Ensemble
- **Primary GitHub:** `ml-from-scratch`
- **Alternative:** scikit-learn
- **Slug:** `random-forest-from-scratch`

A compact, dependency-free multiclass random forest classifier. Each estimator is trained on a bootstrap sample drawn with replacement; at each tree node, only a random subset of features is considered for the Gini-based split. The forest averages the trees' leaf class probabilities to predict labels.

## Run the example and tests

From this folder, run:

```bash
PYTHONPATH=src python3 examples/train.py
PYTHONPATH=src python3 -m unittest discover -s tests -v
```

No third-party packages or datasets are needed.

## Model in brief

For each of `n_estimators` trees, the implementation draws as many training rows as the original dataset contains, with replacement. At each node, it chooses `max_features` feature columns (`"sqrt"` by default), searches numeric thresholds among those columns, and takes the split with the greatest positive Gini-impurity reduction. `max_depth`, `min_samples_split`, `min_samples_leaf`, and `min_impurity_decrease` control tree growth. Setting `random_state` makes bootstrap draws and feature choices reproducible.

A tree's probability for a class is that class's fraction of the bootstrap samples in the reached leaf. `predict_proba` averages those probabilities over the forest, and `predict` chooses the largest average (ties follow the stable `classes_` order). The project is intentionally small and educational: numeric finite features only; no missing values, categorical encoders, sample weights, out-of-bag estimates, pruning, or optimized data structures. For production use, see [scikit-learn's `RandomForestClassifier`](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestClassifier.html), which provides bootstrap-based tree ensembles and additional options.
