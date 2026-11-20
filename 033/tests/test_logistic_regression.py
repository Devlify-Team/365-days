import unittest

from logistic_regression import LogisticRegressionGD, sigmoid


class LogisticRegressionGDTests(unittest.TestCase):
    @staticmethod
    def data():
        X = [[-2.0], [-1.0], [-0.5], [0.5], [1.0], [2.0]]
        y = [0, 0, 0, 1, 1, 1]
        return X, y

    def test_learns_a_separable_binary_problem(self):
        X, y = self.data()
        model = LogisticRegressionGD(learning_rate=0.1, epochs=1500).fit(X, y)
        self.assertEqual(model.predict(X), y)
        self.assertLess(model.loss_history[-1], model.loss_history[0])

    def test_probabilities_are_bounded_and_ordered(self):
        X, y = self.data()
        model = LogisticRegressionGD(learning_rate=0.1, epochs=1000).fit(X, y)
        probabilities = model.predict_proba([[-3.0], [0.0], [3.0]])
        self.assertTrue(all(0.0 <= value <= 1.0 for value in probabilities))
        self.assertEqual(probabilities, sorted(probabilities))

    def test_sigmoid_is_stable_for_extreme_scores(self):
        self.assertEqual(sigmoid(1000.0), 1.0)
        self.assertEqual(sigmoid(-1000.0), 0.0)

    def test_accepts_multiple_features(self):
        X = [[-2.0, -1.0], [-1.0, -2.0], [-1.0, -1.0], [1.0, 1.0], [1.0, 2.0], [2.0, 1.0]]
        y = [0, 0, 0, 1, 1, 1]
        model = LogisticRegressionGD(learning_rate=0.1, epochs=1500).fit(X, y)
        self.assertEqual(model.predict(X), y)

    def test_rejects_one_class_and_non_binary_labels(self):
        with self.assertRaisesRegex(ValueError, "both classes"):
            LogisticRegressionGD().fit([[0.0], [1.0]], [1, 1])
        with self.assertRaisesRegex(ValueError, "only 0 or 1"):
            LogisticRegressionGD().fit([[0.0], [1.0]], [0, 2])

    def test_rejects_bad_shapes_and_prediction_before_fit(self):
        with self.assertRaisesRegex(ValueError, "same number of samples"):
            LogisticRegressionGD().fit([[0.0], [1.0]], [0])
        with self.assertRaisesRegex(ValueError, "same number of features"):
            LogisticRegressionGD().fit([[0.0], [1.0, 2.0]], [0, 1])
        model = LogisticRegressionGD()
        with self.assertRaisesRegex(RuntimeError, "fit the model"):
            model.predict([[1.0]])

    def test_rejects_invalid_hyperparameters_and_threshold(self):
        with self.assertRaisesRegex(ValueError, "learning_rate"):
            LogisticRegressionGD(learning_rate=0)
        with self.assertRaisesRegex(ValueError, "epochs"):
            LogisticRegressionGD(epochs=0)
        with self.assertRaisesRegex(ValueError, "threshold"):
            LogisticRegressionGD(threshold=1.0)


if __name__ == "__main__":
    unittest.main()
