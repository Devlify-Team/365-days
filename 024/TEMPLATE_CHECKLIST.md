# Adapting the ML starter

Before using this scaffold for real work:

- [ ] Replace generated synthetic examples with a documented, licensed dataset; record its source, version, and collection date.
- [ ] Keep immutable source data separate from processed data, and document every transformation.
- [ ] Define the prediction target, intended users, known limitations, and a simple baseline before selecting a model.
- [ ] Choose a split strategy and metrics appropriate to the task (for example, group or time-aware splits when random splitting would leak information).
- [ ] Put learned preprocessing inside a scikit-learn `Pipeline`, fit only on training folds, and reserve final test data for evaluation.
- [ ] Add tests for data schema, missing values, target leakage, and expected model behavior.
- [ ] Track configuration and package versions; set and record random seeds where supported.
- [ ] Keep sensitive data, credentials, large datasets, and generated model binaries out of Git unless a reviewed policy explicitly permits them.
- [ ] Review fairness, privacy, security, licensing, and deployment requirements before sharing or using predictions.

The toy classification accuracy is only a wiring check; it is not a target or a quality claim for a real model.
