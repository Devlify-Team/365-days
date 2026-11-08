import unittest

from src.train import fit_line


class FitLineTests(unittest.TestCase):
    def test_recovers_simple_line(self):
        rows = [{"x": float(x), "y": float(2 * x + 1)} for x in range(5)]
        self.assertAlmostEqual(fit_line(rows)["slope"], 2.0)
        self.assertAlmostEqual(fit_line(rows)["intercept"], 1.0)

    def test_requires_two_rows(self):
        with self.assertRaisesRegex(ValueError, "at least two"):
            fit_line([{"x": 1.0, "y": 3.0}])

    def test_rejects_constant_x_values(self):
        rows = [{"x": 1.0, "y": 2.0}, {"x": 1.0, "y": 4.0}]
        with self.assertRaisesRegex(ValueError, "must not all be equal"):
            fit_line(rows)


if __name__ == "__main__":
    unittest.main()
