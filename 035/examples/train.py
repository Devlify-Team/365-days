"""Fit and query a small three-class random forest."""

from random_forest import RandomForestClassifier


X = [
    [0.0, 0.1], [0.2, 0.0], [0.1, 0.2],
    [4.0, 4.1], [4.2, 4.0], [3.9, 4.2],
    [8.0, 8.1], [8.2, 8.0], [7.9, 8.2],
]
y = ["low"] * 3 + ["middle"] * 3 + ["high"] * 3

model = RandomForestClassifier(n_estimators=31, max_depth=4, random_state=17).fit(X, y)
new_samples = [[0.15, 0.1], [4.1, 4.1], [8.1, 8.1]]

print("Classes:", model.classes_)
for features, label, probabilities in zip(
    new_samples, model.predict(new_samples), model.predict_proba(new_samples)
):
    print(f"{features} -> {label} (probabilities: {probabilities})")
