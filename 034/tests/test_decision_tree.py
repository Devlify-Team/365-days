import unittest

from decision_tree import DecisionTreeClassifier


class DecisionTreeClassifierTests(unittest.TestCase):
    def test_learns_a_separable_binary_problem(self):
        X = [[0.0], [1.0], [2.0], [3.0]]
        y = ["no", "no", "yes", "yes"]
        model = DecisionTreeClassifier(max_depth=1).fit(X, y)
        self.assertEqual(model.predict(X), y)
        self.assertEqual(model.predict([[1.5], [2.5]]), ["no", "yes"])

    def test_multiclass_probabilities_follow_class_order(self):
        X = [[0.0], [1.0], [2.0], [3.0], [4.0], [5.0]]
        y = ["low", "low", "medium", "medium", "high", "high"]
        model = DecisionTreeClassifier(max_depth=2).fit(X, y)
        self.assertEqual(model.classes_, ("high", "low", "medium"))
        probabilities = model.predict_proba(X)
        self.assertEqual(model.predict(X), y)
        self.assertTrue(all(abs(sum(row) - 1.0) < 1e-12 for row in probabilities))
        self.assertTrue(all(0.0 <= value <= 1.0 for row in probabilities for value in row))

    def test_max_depth_zero_keeps_a_majority_leaf(self):
        model = DecisionTreeClassifier(max_depth=0).fit([[0.0], [1.0], [2.0]], ["b", "a", "a"])
        self.assertEqual(model.predict([[0.0], [2.0]]), ["a", "a"])
        self.assertEqual(model.predict_proba([[0.0]]), [[2 / 3, 1 / 3]])

    def test_minimum_leaf_size_prevents_tiny_branch(self):
        X = [[0.0], [1.0], [2.0], [3.0]]
        y = [0, 1, 1, 1]
        model = DecisionTreeClassifier(min_samples_leaf=3).fit(X, y)
        self.assertEqual(model.predict(X), [1, 1, 1, 1])

    def test_handles_constant_features_and_a_single_class(self):
        X = [[2.0, 2.0], [2.0, 2.0], [2.0, 2.0]]
        model = DecisionTreeClassifier().fit(X, ["same", "same", "same"])
        self.assertEqual(model.predict(X), ["same", "same", "same"])
        self.assertEqual(model.predict_proba([[2.0, 2.0]]), [[1.0]])

    def test_rejects_bad_shapes_labels_and_non_finite_features(self):
        with self.assertRaisesRegex(ValueError, "same number of samples"):
            DecisionTreeClassifier().fit([[0.0], [1.0]], [0])
        with self.assertRaisesRegex(ValueError, "same number of features"):
            DecisionTreeClassifier().fit([[0.0], [1.0, 2.0]], [0, 1])
        with self.assertRaisesRegex(ValueError, "finite"):
            DecisionTreeClassifier().fit([[float("nan")]], [0])
        with self.assertRaisesRegex(ValueError, "hashable"):
            DecisionTreeClassifier().fit([[0.0]], [["unhashable"]])

    def test_rejects_invalid_parameters_and_prediction_before_fit(self):
        with self.assertRaisesRegex(ValueError, "max_depth"):
            DecisionTreeClassifier(max_depth=-1)
        with self.assertRaisesRegex(ValueError, "min_samples_split"):
            DecisionTreeClassifier(min_samples_split=1)
        with self.assertRaisesRegex(ValueError, "min_samples_leaf"):
            DecisionTreeClassifier(min_samples_leaf=0)
        with self.assertRaisesRegex(ValueError, "min_impurity_decrease"):
            DecisionTreeClassifier(min_impurity_decrease=-0.1)
        model = DecisionTreeClassifier()
        with self.assertRaisesRegex(RuntimeError, "fit the model"):
            model.predict([[0.0]])


if __name__ == "__main__":
    unittest.main()
