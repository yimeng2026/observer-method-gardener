from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from checks.goldbach_claim import evaluate_formula, goldbach_partitions, log_integral_from_two, singular_series


class GoldbachClaimTest(unittest.TestCase):
    def test_direct_prime_enumeration_recovers_d1000(self):
        self.assertEqual(goldbach_partitions(1000), 28)
        self.assertEqual(singular_series(1000), 4 / 3)

    def test_log_integral_grid_converges_to_independent_value(self):
        li_zero = 1.04516378011749
        self.assertAlmostEqual(log_integral_from_two(1000) + li_zero, 177.609657990152, delta=2e-6)

    def test_public_formulas_are_estimates_not_proof(self):
        result = evaluate_formula(1000)
        self.assertAlmostEqual(result["hardyLittlewood"], 36.892, delta=0.02)
        self.assertAlmostEqual(result["singleTermEstimate"], 27.90, delta=0.02)
        self.assertAlmostEqual(result["literalIntegralEstimate"], 27.017, delta=0.002)
        self.assertFalse(result["proofOfGoldbach"])
        self.assertEqual(result["actualUnorderedPartitions"], 28)


if __name__ == "__main__":
    unittest.main()
