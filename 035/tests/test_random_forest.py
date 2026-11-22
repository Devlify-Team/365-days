import unittest

from random_forest import RandomForestClassifier


class RandomForestClassifierTests(unittest.TestCase):
    @staticmethod
    def multiclass_data():
        X = [
            [0.0, 0.1], [0.2, 0.0], [0.1, 0.2],
            [4.0, 4.1], [4.2, 4.0], [3.9, 4.2],
            [8.0, 8.1], [8.2, 8.0], [7.9, 8.2],
        ]
        y = ["low"] * 3 + ["middle"] * 3 + ["high"] * 3
        return X, y

    def test_forest_learns_clear_separated_classes(self):
        X, y = self.multiclass_data()
        model = RandomForestClassifier(n_estimators=31, max_depth=4, random_state=17).fit(X, y)
        self.assertEqual(model.predict(X), y)
        self.assertEqual(len(model.estimators_), 31)

    def test_probabilities_are_averaged_and_normalized(self):
        X, y = self.multiclass_data()
        model = RandomForestClassifier(n_estimators=13, random_state=5).fit(X, y)
        probabilities = model.predict_proba([[0.1, 0.1], [4.1, 4.1], [8.1, 8.1]])
        self.assertEqual(model.classes_, ("high", "low", "middle"))
        self.assertTrue(all(abs(sum(row) - 1.0) < 1e-12 for row in probabilities))
        self.assertTrue(all(0.0 <= value <= 1.0 for row in probabilities for value in row))
        self.assertEqual([len(row) for row in probabilities], [3, 3, 3])

    def test_random_state_makes_bootstrap_and_splits_reproducible(self):
        X, y = self.multiclass_data()
        first = RandomForestClassifier(n_estimators=11, random_state=42).fit(X, y)
        second = RandomForestClassifier(n_estimators=11, random_state=42).fit(X, y)
        self.assertEqual(first.predict_proba(X), second.predict_proba(X))
        self.assertEqual(first.predict(X), second.predict(X))

    def test_accepts_feature_subset_options(self):
        X, y = self.multiclass_data()
        for max_features in (1, "sqrt", "log2", None):
            with self.subTest(max_features=max_features):
                model = RandomForestClassifier(
                    n_estimators=3, max_features=max_features, random_state=3
                ).fit(X, y)
                self.assertEqual(len(model.predict(X)), len(y))

    def test_single_class_forest_returns_unit_probability(self):
        model = RandomForestClassifier(n_estimators=5, random_state=1).fit(
            [[0.0], [1.0], [2.0]], ["same", "same", "same"]
        )
        self.assertEqual(model.classes_, ("same",))
        self.assertEqual(model.predict([[100.0]]), ["same"])
        self.assertEqual(model.predict_proba([[100.0]]), [[1.0]])

    def test_rejects_bad_shapes_and_invalid_features(self):
        with self.assertRaisesRegex(ValueError, "same number of samples"):
            RandomForestClassifier().fit([[0.0], [1.0]], [0])
        with self.assertRaisesRegex(ValueError, "same number of features"):
            RandomForestClassifier().fit([[0.0], [1.0, 2.0]], [0, 1])
        with self.assertRaisesRegex(ValueError, "finite"):
            RandomForestClassifier().fit([[float("inf")]], [0])
        with self.assertRaisesRegex(ValueError, "hashable"):
            RandomForestClassifier().fit([[0.0]], [["no"]])

    def test_rejects_bad_parameters_and_prediction_before_fit(self):
        with self.assertRaisesRegex(ValueError, "n_estimators"):
            RandomForestClassifier(n_estimators=0)
        with self.assertRaisesRegex(ValueError, "max_depth"):
            RandomForestClassifier(max_depth=-1)
        with self.assertRaisesRegex(ValueError, "max_features"):
            RandomForestClassifier(max_features="all")
        with self.assertRaisesRegex(ValueError, "random_state"):
            RandomForestClassifier(random_state=True)
        with self.assertRaisesRegex(ValueError, "max_features"):
            RandomForestClassifier(max_features=3).fit([[0.0, 1.0]], [0])
        with self.assertRaisesRegex(RuntimeError, "fit the model"):
            RandomForestClassifier().predict([[0.0]])


if __name__ == "__main__":
    unittest.main()
