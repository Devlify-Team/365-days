"""Train and display a small three-class decision tree."""

from decision_tree import DecisionTreeClassifier


X = [[0.0], [1.0], [2.0], [3.0], [4.0], [5.0]]
y = ["low", "low", "medium", "medium", "high", "high"]

model = DecisionTreeClassifier(max_depth=2).fit(X, y)
new_samples = [[0.5], [2.5], [4.5]]

print("Classes:", model.classes_)
for features, label, probabilities in zip(
    new_samples, model.predict(new_samples), model.predict_proba(new_samples)
):
    print(f"{features} -> {label} (probabilities: {probabilities})")
