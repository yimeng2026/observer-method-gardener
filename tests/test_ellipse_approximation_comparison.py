from pathlib import Path
import sys
import unittest

import mpmath as mp

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from checks.ellipse_approximation_comparison import (
    ellipse_exact,
    ramanujan_first,
    ramanujan_second,
)


class EllipseApproximationComparisonTest(unittest.TestCase):
    def test_near_circle_rejects_the_ai_12750_result(self):
        exact = ellipse_exact(2025, 2024)
        second = ramanujan_second(2025, 2024)
        first = ramanujan_first(2025, 2024)
        self.assertTrue(mp.nstr(exact, 45).startswith("12720.30884835844066437367524079"))
        self.assertLess(abs(second - exact), mp.mpf("1e-30"))
        self.assertLess(abs(first - exact), mp.mpf("1e-17"))
        self.assertGreater(mp.mpf("12750.04") - exact, 29)

    def test_extreme_case_recovers_the_integral_image_value(self):
        exact = ellipse_exact(20251949, 1)
        self.assertTrue(mp.nstr(exact, 45).startswith("81007796.000001748972995628111818866"))
        absolute_error = abs(4 * mp.mpf(20251949) - exact)
        relative_error = absolute_error / exact
        self.assertLess(absolute_error, mp.mpf("0.00000175"))
        self.assertLess(relative_error, mp.mpf("3e-14"))

    def test_extreme_case_separates_absolute_and_relative_approximation_errors(self):
        a = mp.mpf(20251949)
        exact = ellipse_exact(a, 1)
        self.assertGreater(abs(ramanujan_first(a, 1) - exact), mp.mpf("3e5"))
        self.assertGreater(abs(ramanujan_second(a, 1) - exact), mp.mpf("3e4"))
        self.assertLess(abs(4 * a - exact), mp.mpf("0.00000175"))
        self.assertNotEqual(ramanujan_second(a, 1), exact)

    def test_circle_limit_is_exact_for_all_three_displayed_forms(self):
        with mp.workdps(60):
            expected = 2 * mp.pi * 7
        self.assertLess(abs(ellipse_exact(7, 7) - expected), mp.mpf("1e-40"))
        self.assertLess(abs(ramanujan_first(7, 7) - expected), mp.mpf("1e-40"))
        self.assertLess(abs(ramanujan_second(7, 7) - expected), mp.mpf("1e-40"))


if __name__ == "__main__":
    unittest.main()
