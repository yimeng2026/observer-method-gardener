from pathlib import Path
import math
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from checks.dispute_numerical_claims import displayed_g_estimate, starlight_remainder_scales


class DisputeNumericalClaimsTest(unittest.TestCase):
    def test_ai_own_gravity_numbers_are_not_far_below_reference(self):
        result = displayed_g_estimate(1.52e-13, 5500.0, 6.674e-11)
        self.assertAlmostEqual(result["calculated"], 6.652676621241225e-11, delta=1e-24)
        self.assertAlmostEqual(result["relativeBelowReference"], 0.0031949923222616937, places=15)

    def test_starlight_remainder_and_exponential_claims_are_inconsistent(self):
        result = starlight_remainder_scales(1.32712440018e20, 6.957e8)
        self.assertAlmostEqual(result["kCubedArcseconds"], 1.9722856176907427e-12, delta=1e-24)
        self.assertAlmostEqual(result["exponential"], 0.999997877499682, places=15)
        self.assertAlmostEqual(result["oneMinusExponential"], 2.122500317947029e-6, delta=1e-18)
        self.assertNotAlmostEqual(result["exponential"], 1e-19)


if __name__ == "__main__":
    unittest.main()
