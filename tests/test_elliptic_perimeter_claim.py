from pathlib import Path
import sys
import unittest

import mpmath as mp

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from checks.elliptic_perimeter_claim import ellipse_perimeter, endpoint_models


class EllipticPerimeterClaimTest(unittest.TestCase):
    def test_displayed_integral_matches_standard_perimeter(self):
        for a, b in [(2.0, 1.0), (3.0, 1.5)]:
            result = ellipse_perimeter(a, b)
            self.assertLess(result["relativeDiscrepancy"], 0.0005)
            self.assertAlmostEqual(result["standardPerimeter"], float(4 * mp.mpf(a) * mp.ellipe(1 - (b / a)**2)), places=10)

    def test_both_endpoint_singularities_are_integrable_inverse_square_roots(self):
        a, b = 2.0, 1.0
        models = endpoint_models(a, b)
        self.assertEqual(models["leftExponent"], 0.5)
        self.assertEqual(models["rightExponent"], 0.5)
        t_left = 1 + 1e-8
        t_right = a / b - 1e-8
        f = lambda t: t**2 / mp.sqrt((t**2 - 1) * (1 - b**2 * t**2 / a**2))
        left_ratio = float(f(t_left)) * (t_left - 1)**0.5 / models["leftCoefficient"]
        right_ratio = float(f(t_right)) * (a / b - t_right)**0.5 / models["rightCoefficient"]
        self.assertAlmostEqual(left_ratio, 1.0, delta=0.001)
        self.assertAlmostEqual(right_ratio, 1.0, delta=0.001)

    def test_circle_limit_is_not_an_integrable_member_of_the_displayed_family(self):
        with self.assertRaises(ValueError):
            ellipse_perimeter(2.0, 2.0)


if __name__ == "__main__":
    unittest.main()
