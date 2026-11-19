import unittest

from regularized_regression import RegularizedLinearRegression


class RegularizedRegressionTests(unittest.TestCase):
    @staticmethod
    def data():
        X = [[float(x)] for x in range(-5, 6)]
        y = [1.0 + 2.0 * row[0] for row in X]
        return X, y

    def test_ridge_shrinks_weights_without_penalizing_intercept(self):
        X, y = self.data()
        plain = RegularizedLinearRegression(alpha=0, learning_rate=0.02, epochs=1500).fit(X, y)
        ridge = RegularizedLinearRegression(
            method="ridge", alpha=0.5, learning_rate=0.02, epochs=1500
        ).fit(X, y)
        self.assertLess(abs(ridge.weights[0]), abs(plain.weights[0]))
        self.assertAlmostEqual(ridge.intercept, 1.0, places=2)

    def test_lasso_soft_threshold_can_set_a_small_weight_to_zero(self):
        X = [[float(x), float(4 * x)] for x in range(-5, 6)]
        y = [1.0 + 2.0 * row[0] for row in X]
        model = RegularizedLinearRegression(
            method="lasso", alpha=0.15, learning_rate=0.001, epochs=3000
        ).fit(X, y)
        self.assertTrue(any(weight == 0.0 for weight in model.weights))
        self.assertLess(model.objective_history[-1], model.objective_history[0])

    def test_both_methods_predict_and_track_objective(self):
        X, y = self.data()
        for method in ("ridge", "lasso"):
            with self.subTest(method=method):
                model = RegularizedLinearRegression(
                    method=method, alpha=0.1, learning_rate=0.02, epochs=1000
                ).fit(X, y)
                self.assertEqual(len(model.objective_history), 1000)
                self.assertAlmostEqual(model.predict([[2.0]])[0], 5.0, delta=0.5)

    def test_rejects_invalid_hyperparameters_and_method(self):
        with self.assertRaisesRegex(ValueError, "method"):
            RegularizedLinearRegression(method="elastic")
        with self.assertRaisesRegex(ValueError, "alpha"):
            RegularizedLinearRegression(alpha=-1)
        with self.assertRaisesRegex(ValueError, "learning_rate"):
            RegularizedLinearRegression(learning_rate=0)
        with self.assertRaisesRegex(ValueError, "epochs"):
            RegularizedLinearRegression(epochs=0)

    def test_rejects_bad_training_shapes_and_non_finite_values(self):
        with self.assertRaisesRegex(ValueError, "same number of samples"):
            RegularizedLinearRegression().fit([[1.0], [2.0]], [1.0])
        with self.assertRaisesRegex(ValueError, "same number of features"):
            RegularizedLinearRegression().fit([[1.0], [2.0, 3.0]], [1.0, 2.0])
        with self.assertRaisesRegex(ValueError, "finite"):
            RegularizedLinearRegression().fit([[float("inf")]], [1.0])

    def test_predict_requires_fit_and_matching_feature_count(self):
        model = RegularizedLinearRegression()
        with self.assertRaisesRegex(RuntimeError, "fit the model"):
            model.predict([[1.0]])
        model.fit([[1.0]], [2.0])
        with self.assertRaisesRegex(ValueError, "same number of features"):
            model.predict([[1.0, 2.0]])


if __name__ == "__main__":
    unittest.main()
