from fractions import Fraction
from pathlib import Path
import math
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from checks.prime_quadruplet_claim import (
    count_heuristics,
    prime_quadruplets,
    quadruplet_constant,
    small_prime_factors,
)


class PrimeQuadrupletClaimTest(unittest.TestCase):
    def test_small_prime_correction_factors(self):
        self.assertEqual(small_prime_factors(), {
            2: Fraction(8),
            3: Fraction(27, 16),
            5: Fraction(125, 256),
            7: Fraction(1029, 1296),
        })

    def test_product_recovers_the_displayed_constant(self):
        self.assertAlmostEqual(quadruplet_constant(1000000), 4.15118, delta=0.00001)

    def test_finite_prime_quadruplet_examples(self):
        self.assertEqual(prime_quadruplets(200), [
            (5, 7, 11, 13),
            (11, 13, 17, 19),
            (101, 103, 107, 109),
            (191, 193, 197, 199),
        ])

    def test_local_density_is_not_cumulative_count(self):
        result = count_heuristics(10**6, 4.15118)
        self.assertAlmostEqual(result["localDensity"], 0.0001139472396567115, places=18)
        self.assertAlmostEqual(result["cumulativeCount"], 113.94723965671149, places=10)
        self.assertAlmostEqual(result["cumulativeCount"], 10**6 * result["localDensity"], places=10)
        self.assertFalse(math.isclose(result["localDensity"], result["cumulativeCount"]))


if __name__ == "__main__":
    unittest.main()
