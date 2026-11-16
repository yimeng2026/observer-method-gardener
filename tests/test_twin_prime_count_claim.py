from pathlib import Path
import math
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from checks.twin_prime_count_claim import clement_condition, hardy_littlewood_estimate, mean_gap_heuristic, twin_count


class TwinPrimeCountClaimTest(unittest.TestCase):
    def test_independent_counts_recover_reference_values(self):
        expected = {100: 8, 1000: 35, 10000: 205, 100000: 1224, 1000000: 8169}
        for limit, count in expected.items():
            self.assertEqual(twin_count(limit), count)

    def test_integral_and_displayed_relative_errors(self):
        result = hardy_littlewood_estimate(100000)
        self.assertAlmostEqual(result["integralFrom2"], 945.7595892874221, places=9)
        self.assertAlmostEqual(result["truncatedEstimate"], 1249.2848560144032, places=7)
        actual = 1224
        self.assertAlmostEqual((1620 - actual) / actual, 0.3235294117647059)
        self.assertAlmostEqual(100 * (1620 - actual) / actual, 32.35294117647059)
        self.assertNotAlmostEqual(100 * (1620 - actual) / actual, 0.3235294118)

    def test_clement_criterion_matches_finite_twin_pairs(self):
        for p in range(3, 102):
            is_twin_first = all((p % d for d in range(2, math.isqrt(p) + 1))) and all((p + 2) % d for d in range(2, math.isqrt(p + 2) + 1))
            self.assertEqual(clement_condition(p), is_twin_first, msg=f"p={p}")

    def test_gap_formula_is_a_smooth_heuristic_not_a_step_function_derivative(self):
        coefficient = mean_gap_heuristic(1000000) / math.log(1000000)**2
        self.assertAlmostEqual(coefficient, 0.7572937872994642, places=12)


if __name__ == "__main__":
    unittest.main()
