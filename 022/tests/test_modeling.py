import unittest

from src.modeling import fit_ridge_line, rmse


class ModelingTests(unittest.TestCase):
    def test_fits_exact_line_without_regularization(self):
        rows = [{"x": float(x), "y": float(2 * x + 1)} for x in range(5)]
        model = fit_ridge_line(rows)
        self.assertAlmostEqual(model["slope"], 2.0)
        self.assertAlmostEqual(model["intercept"], 1.0)

    def test_regularization_shrinks_slope(self):
        rows = [{"x": float(x), "y": float(2 * x + 1)} for x in range(5)]
        plain = fit_ridge_line(rows, alpha=0.0)
        regularized = fit_ridge_line(rows, alpha=2.0)
        self.assertLess(regularized["slope"], plain["slope"])

    def test_rmse_is_zero_for_perfect_predictions(self):
        rows = [{"x": 0.0, "y": 1.0}, {"x": 2.0, "y": 5.0}]
        self.assertAlmostEqual(rmse(rows, {"slope": 2.0, "intercept": 1.0}), 0.0)

    def test_rejects_negative_regularization(self):
        with self.assertRaisesRegex(ValueError, "non-negative"):
            fit_ridge_line([{"x": 0.0, "y": 1.0}, {"x": 1.0, "y": 2.0}], alpha=-1.0)


if __name__ == "__main__":
    unittest.main()
