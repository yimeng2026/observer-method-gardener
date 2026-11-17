from pathlib import Path
import math
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from checks.dense_prime_constellation_claim import (
    consecutive_prime_tuples,
    displayed_count_estimate,
    residue_coverage,
)


class DensePrimeConstellationClaimTest(unittest.TestCase):
    def test_two_four_eight_tuple_is_unique(self):
        offsets = (0, 2, 4, 8, 10, 14, 16, 20)
        self.assertEqual(residue_coverage(offsets, 3), [0, 1, 2])
        self.assertEqual(
            consecutive_prime_tuples(100000, 8, (2, 4)),
            [(3, 5, 7, 11, 13, 17, 19, 23)],
        )

    def test_ai_offset_pattern_is_blocked_modulo_five(self):
        offsets = (0, 2, 6, 8, 12, 14, 18, 20)
        self.assertEqual(residue_coverage(offsets, 5), [0, 1, 2, 3, 4])
        self.assertEqual(residue_coverage(offsets, 3), [0, 2])

    def test_finite_dense_eight_tuples_refute_not_found_claim(self):
        tuples = consecutive_prime_tuples(100, 8, (2, 4, 6))
        self.assertIn((11, 13, 17, 19, 23, 29, 31, 37), tuples)
        self.assertIn((59, 61, 67, 71, 73, 79, 83, 89), tuples)
        self.assertTrue(all(len(item) == 8 for item in tuples))

    def test_displayed_count_estimate_is_about_one_thousandth(self):
        result = displayed_count_estimate(10**12, 0.00037)
        self.assertAlmostEqual(result, 0.0010889959035667266, places=18)
        self.assertFalse(math.isclose(result, 1.06, rel_tol=1e-3))


if __name__ == "__main__":
    unittest.main()
