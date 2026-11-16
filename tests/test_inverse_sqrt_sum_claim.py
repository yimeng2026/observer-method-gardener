from decimal import Decimal
import math
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from checks.inverse_sqrt_sum_claim import inverse_sqrt_sum_certificate


class InverseSqrtSumClaimTest(unittest.TestCase):
    def test_large_sum_has_certified_integer_part_39998(self):
        result = inverse_sqrt_sum_certificate(400002025)
        lower = Decimal(result["lower"])
        upper = Decimal(result["upper"])
        self.assertGreater(lower, Decimal(39998))
        self.assertLess(upper, Decimal(39999))
        self.assertEqual(int(lower), 39998)
        self.assertEqual(int(upper), 39998)

    def test_bounds_contain_small_exact_sums(self):
        for n in [1, 2, 3, 10, 100]:
            result = inverse_sqrt_sum_certificate(n)
            actual = sum(1 / math.sqrt(k) for k in range(1, n + 1))
            self.assertLessEqual(float(result["lower"]), actual)
            self.assertGreaterEqual(float(result["upper"]), actual)

    def test_non_positive_or_non_integer_input_is_rejected(self):
        for n in [0, -1, 1.5, True]:
            with self.assertRaises(ValueError):
                inverse_sqrt_sum_certificate(n)

    def test_displayed_s100_lower_exceeds_actual_and_upper(self):
        from checks.inverse_sqrt_sum_claim import displayed_s100_bounds
        result = displayed_s100_bounds()
        self.assertGreater(result["lower"], result["actual"])
        self.assertGreater(result["lower"], result["upper"])
        self.assertGreater(result["upper"], result["actual"])


if __name__ == "__main__":
    unittest.main()
