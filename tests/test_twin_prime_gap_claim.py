from fractions import Fraction
import math
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from checks.twin_prime_gap_claim import displayed_gap_bounds, product_c2, twin_pairs


class TwinPrimeGapClaimTest(unittest.TestCase):
    def test_actual_consecutive_pairs_and_minimum_gap(self):
        pairs = twin_pairs(110)
        following = {p: next_p for p, next_p in zip(pairs, pairs[1:])}
        self.assertEqual(following.get(3), 5)
        self.assertEqual(following.get(5), 11)
        self.assertEqual(following.get(71), 101)
        self.assertEqual(following.get(71, 71) - 71, 30)
        self.assertEqual(min(next_p - p for p, next_p in zip(pairs, pairs[1:]) if p >= 5), 6)

    def test_p71_product_and_displayed_upper_arithmetic(self):
        self.assertEqual(product_c2(71), Fraction(175, 256))
        result = displayed_gap_bounds(71)
        expected_upper = 6 * (1 + math.log(71)**2 / (6 * float(Fraction(175, 256))))
        self.assertAlmostEqual(result["upper"], expected_upper)
        self.assertGreater(result["upper"], 32)
        self.assertNotEqual(round(result["upper"]), 30)
        self.assertLessEqual(30, result["upper"])

    def test_asymptotic_mean_main_term_matches_the_displayed_heuristic(self):
        result = displayed_gap_bounds(71)
        self.assertAlmostEqual(result["asymptoticMeanMainTerm"], math.log(71)**2 / (2 * result["c2"]))


if __name__ == "__main__":
    unittest.main()
