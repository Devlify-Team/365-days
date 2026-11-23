import unittest

from gradient_boosting import GradientBoostingRegressor


class GradientBoostingRegressorTests(unittest.TestCase):
    @staticmethod
    def data():
        X = [[float(value)] for value in range(8)]
        y = [1.0, 2.0, 1.5, 4.0, 5.0, 7.5, 7.0, 9.0]
        return X, y

    def test_fits_residual_trees_and_reduces_training_loss(self):
        X, y = self.data()
        model = GradientBoostingRegressor(n_estimators=40, learning_rate=0.1, max_depth=2).fit(X, y)
        predictions = model.predict(X)
        self.assertEqual(len(model.estimators_), 40)
        self.assertEqual(len(model.loss_history), 41)
        self.assertLess(model.loss_history[-1], model.loss_history[0])
        self.assertLess(model.loss_history[-1], 0.5)
        self.assertEqual(len(predictions), len(y))

    def test_predictions_are_deterministic(self):
        X, y = self.data()
        first = GradientBoostingRegressor(n_estimators=12).fit(X, y)
        second = GradientBoostingRegressor(n_estimators=12).fit(X, y)
        self.assertEqual(first.predict(X), second.predict(X))
        self.assertEqual(first.loss_history, second.loss_history)

    def test_zero_depth_keeps_the_mean_prediction(self):
        X = [[0.0], [1.0], [2.0]]
        y = [2.0, 4.0, 6.0]
        model = GradientBoostingRegressor(n_estimators=5, max_depth=0).fit(X, y)
        self.assertEqual(model.initial_prediction_, 4.0)
        for prediction in model.predict(X):
            self.assertAlmostEqual(prediction, 4.0)
        self.assertAlmostEqual(model.loss_history[0], model.loss_history[-1])

    def test_handles_multiple_features(self):
        X = [[0.0, 0.0], [0.0, 1.0], [1.0, 0.0], [1.0, 1.0], [2.0, 2.0]]
        y = [0.0, 1.0, 1.0, 2.0, 4.0]
        model = GradientBoostingRegressor(n_estimators=10, max_depth=2).fit(X, y)
        self.assertTrue(all(isinstance(value, float) for value in model.predict(X)))
        self.assertLess(model.loss_history[-1], model.loss_history[0])

    def test_rejects_bad_shapes_and_non_finite_values(self):
        with self.assertRaisesRegex(ValueError, "same number of samples"):
            GradientBoostingRegressor().fit([[0.0], [1.0]], [0.0])
        with self.assertRaisesRegex(ValueError, "same number of features"):
            GradientBoostingRegressor().fit([[0.0], [1.0, 2.0]], [0.0, 1.0])
        with self.assertRaisesRegex(ValueError, "finite"):
            GradientBoostingRegressor().fit([[float("nan")]], [0.0])
        with self.assertRaisesRegex(ValueError, "finite"):
            GradientBoostingRegressor().fit([[0.0]], [float("inf")])

    def test_rejects_invalid_parameters_and_prediction_before_fit(self):
        with self.assertRaisesRegex(ValueError, "n_estimators"):
            GradientBoostingRegressor(n_estimators=0)
        with self.assertRaisesRegex(ValueError, "learning_rate"):
            GradientBoostingRegressor(learning_rate=0)
        with self.assertRaisesRegex(ValueError, "max_depth"):
            GradientBoostingRegressor(max_depth=-1)
        with self.assertRaisesRegex(ValueError, "min_samples_split"):
            GradientBoostingRegressor(min_samples_split=1)
        with self.assertRaisesRegex(ValueError, "min_samples_leaf"):
            GradientBoostingRegressor(min_samples_leaf=0)
        with self.assertRaisesRegex(RuntimeError, "fit the model"):
            GradientBoostingRegressor().predict([[0.0]])


if __name__ == "__main__":
    unittest.main()
