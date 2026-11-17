from pathlib import Path
import math
import sys
import unittest

import mpmath as mp

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from checks.research_example_number_theory import (
    derivative_comparison,
    integral_derivatives,
    prime_gap_scan,
    symmetry_counterexample,
)


class ResearchExampleNumberTheoryTest(unittest.TestCase):
    def test_smooth_pnt_derivative_is_not_reciprocal_one_plus_log(self):
        result = derivative_comparison(math.e**2)
        self.assertAlmostEqual(result["exactDerivative"], 0.25)
        self.assertAlmostEqual(result["claimedDerivative"], 1 / 3)
        self.assertNotAlmostEqual(result["exactDerivative"], result["claimedDerivative"])

    def test_displayed_ei_prefactor_reproduces_the_ode(self):
        x = math.e**2
        result = integral_derivatives(x)
        expected = 1 / (1 + math.log(x))
        self.assertAlmostEqual(result["unscaledEiDerivative"], math.e * expected)
        self.assertAlmostEqual(result["displayedScaledDerivative"], expected)

    def test_symmetry_alone_does_not_force_zeros_onto_half_line(self):
        result = symmetry_counterexample(0.2)
        self.assertEqual(result["roots"], [0.2, 0.8])
        self.assertAlmostEqual(result["valueAt0.1"], result["valueAt0.9"])
        self.assertTrue(all(root != 0.5 for root in result["roots"]))

    def test_million_gap_scan_is_only_finite_evidence(self):
        result = prime_gap_scan(1000000)
        self.assertEqual(result["pairs"], 78496)
        self.assertEqual(result["maxRatioPrime"], 370261)
        self.assertEqual(result["maxRatioGap"], 112)
        self.assertAlmostEqual(result["maxGapOverLog"], 8.735011647190985, places=14)
        self.assertTrue(result["allGapsAtLeast2"])
        self.assertTrue(result["allGapsBelow36Log"])


if __name__ == "__main__":
    unittest.main()
