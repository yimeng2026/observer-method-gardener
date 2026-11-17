from pathlib import Path
import sys
import unittest

import mpmath as mp

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from checks.blue_star_harmonic_claim import (
    arithmetic_partial_sum_integrals,
    expansion_coefficients,
    harmonic_residuals,
)


class BlueStarHarmonicClaimTest(unittest.TestCase):
    def test_beta_repackages_the_existing_second_order_correction(self):
        with mp.workdps(90):
            coefficients = expansion_coefficients()
            previous_correction = (1 - mp.euler) / 2 - mp.mpf(1) / 12
            self.assertLess(abs(coefficients["beta"] - 10 * previous_correction), mp.mpf("1e-70"))
            self.assertLess(abs(coefficients["inverseNSquaredDisplayed"] + mp.mpf(1) / 12), mp.mpf("1e-70"))
            self.assertEqual(coefficients["inverseNSquaredCorrectedResidual"], 0)
            self.assertTrue(str(coefficients["beta"]).startswith("1.28058834215900236363410621625465451145586998696704867"))

    def test_large_n_base_residual_matches_the_image_sign_and_scale(self):
        with mp.workdps(80):
            result = harmonic_residuals(10**800)
            expected = -mp.mpf("0.1") * expansion_coefficients()["beta"] / mp.mpf(10) ** 1600
            relative_error = abs((result["baseResidual"] - expected) / expected)
            self.assertLess(relative_error, mp.mpf("1e-30"))
            self.assertLess(result["baseResidual"], 0)

    def test_correction_cancels_order_two_but_does_not_make_an_identity(self):
        # Compare against an expectation with enough digits for the O(10^-901) residual.
        with mp.workdps(1100):
            result = harmonic_residuals(10**300)
            coefficients = expansion_coefficients()
            expected_order_three = coefficients["correctedLeadingCoefficient"] / mp.mpf(10) ** 900
            relative_error = abs((result["correctedResidual"] - expected_order_three) / expected_order_three)
            self.assertLess(relative_error, mp.mpf("1e-100"))
            self.assertNotEqual(result["correctedResidual"], 0)
            self.assertGreater(result["correctedResidual"], 0)
            self.assertLess(abs(result["correctedResidual"]), abs(result["baseResidual"]))

    def test_arithmetic_partial_sum_integrals_are_ordinary_polynomial_integrals(self):
        integrals = arithmetic_partial_sum_integrals()
        self.assertEqual(integrals["fromMinusOneToZero"], "-1/12")
        self.assertEqual(integrals["fromZeroToOneShifted"], "-1/12")
        self.assertEqual(integrals["operation"], "ordinary polynomial integration, not analytic continuation")


if __name__ == "__main__":
    unittest.main()
