import math
import unittest

from ml_from_scratch import LinearRegressionGD


class LinearRegressionGDTests(unittest.TestCase):
    def test_learns_a_simple_line_and_predicts(self):
        X = [[0.0], [1.0], [2.0], [3.0], [4.0]]
        y = [1.0, 3.0, 5.0, 7.0, 9.0]
        model = LinearRegressionGD(learning_rate=0.03, epochs=1500).fit(X, y)
        self.assertAlmostEqual(model.weights[0], 2.0, places=3)
        self.assertAlmostEqual(model.bias, 1.0, places=3)
        self.assertAlmostEqual(model.predict([[5.0]])[0], 11.0, places=3)

    def test_loss_decreases_during_training(self):
        model = LinearRegressionGD(learning_rate=0.03, epochs=100).fit(
            [[0.0], [1.0], [2.0], [3.0]], [1.0, 3.0, 5.0, 7.0]
        )
        self.assertGreater(model.loss_history[0], model.loss_history[-1])
        self.assertEqual(len(model.loss_history), 100)

    def test_fits_more_than_one_feature(self):
        X = [[0.0, 0.0], [1.0, 0.0], [0.0, 1.0], [1.0, 1.0], [2.0, 1.0]]
        y = [4.0, 6.0, 1.0, 3.0, 5.0]  # y = 2*x0 - 3*x1 + 4
        model = LinearRegressionGD(learning_rate=0.04, epochs=3000).fit(X, y)
        self.assertAlmostEqual(model.weights[0], 2.0, places=2)
        self.assertAlmostEqual(model.weights[1], -3.0, places=2)
        self.assertAlmostEqual(model.bias, 4.0, places=2)

    def test_rejects_empty_or_mismatched_training_data(self):
        with self.assertRaisesRegex(ValueError, "X must be a non-empty"):
            LinearRegressionGD().fit([], [])
        with self.assertRaisesRegex(ValueError, "same number of samples"):
            LinearRegressionGD().fit([[1.0], [2.0]], [3.0])

    def test_rejects_inconsistent_or_non_finite_features(self):
        with self.assertRaisesRegex(ValueError, "same number of columns"):
            LinearRegressionGD().fit([[1.0], [2.0, 3.0]], [1.0, 2.0])
        with self.assertRaisesRegex(ValueError, "finite"):
            LinearRegressionGD().fit([[math.inf]], [1.0])

    def test_rejects_prediction_before_fit_and_wrong_width(self):
        model = LinearRegressionGD()
        with self.assertRaisesRegex(RuntimeError, "fit the model"):
            model.predict([[1.0]])
        model.fit([[1.0]], [2.0])
        with self.assertRaisesRegex(ValueError, "same number of columns"):
            model.predict([[1.0, 2.0]])

    def test_rejects_invalid_hyperparameters(self):
        with self.assertRaisesRegex(ValueError, "learning_rate"):
            LinearRegressionGD(learning_rate=0)
        with self.assertRaisesRegex(ValueError, "epochs"):
            LinearRegressionGD(epochs=0)


if __name__ == "__main__":
    unittest.main()
