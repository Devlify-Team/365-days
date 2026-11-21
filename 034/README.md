# Decision tree implementation

- **Day:** 034
- **Month:** 2 — Classical ML Projects
- **Category:** Classification
- **Primary GitHub:** `ml-from-scratch`
- **Alternative:** scikit-learn
- **Slug:** `decision-tree-implementation`

This project builds a small classification tree from scratch with no external dependencies. It searches numeric feature thresholds, chooses the split with the largest Gini-impurity reduction, and recursively grows branches until they are pure or a stopping rule applies. The fitted tree predicts class labels and per-class probabilities.

## Run the example and tests

From this folder, run:

```bash
PYTHONPATH=src python3 examples/train.py
PYTHONPATH=src python3 -m unittest discover -s tests -v
```

No third-party packages or datasets are needed.

## Model in brief

For a node containing class proportions `p₁, …, pₖ`, Gini impurity is `1 − Σ pᵢ²`. A candidate threshold divides the node's samples into left and right groups; the implementation measures the sample-weighted impurity after the split and selects the greatest positive decrease. Ties are resolved deterministically by considering features and thresholds in ascending order. A leaf reports its training class frequencies as probabilities.

The implementation accepts finite numeric features and hashable labels. `max_depth`, `min_samples_split`, `min_samples_leaf`, and `min_impurity_decrease` provide basic controls on tree growth. Exhaustive threshold search is intentionally transparent and suitable for small examples, not large datasets; missing values, categorical feature encodings, sample weights, pruning, and optimized data structures are out of scope. For practical use, see [scikit-learn's `DecisionTreeClassifier`](https://scikit-learn.org/stable/modules/generated/sklearn.tree.DecisionTreeClassifier.html), which offers Gini, entropy, and log-loss criteria along with additional controls and optimized implementations.
