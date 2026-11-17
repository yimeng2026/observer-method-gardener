from pathlib import Path
import math
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from checks.ranking_physics_formulas import (
    correction_integral_coefficients,
    exponential_rebaseline,
    negative_exponential_deflection_correction,
)


class RankingPhysicsFormulasTest(unittest.TestCase):
    def test_exponential_rebaseline_compares_incompatible_sides(self):
        result = exponential_rebaseline(0.1)
        self.assertAlmostEqual(result["leftK2Over3"], 1 / 300)
        self.assertAlmostEqual(result["rightExponential"], 1.1000254691767588)
        self.assertNotAlmostEqual(result["leftK2Over3"], result["rightExponential"])
        self.assertAlmostEqual(result["onePlusK"], 1.1)

    def test_integral_denominators_are_six_seven_eight(self):
        result = correction_integral_coefficients()
        self.assertEqual(result["firstDenominator"], 6)
        self.assertEqual(result["secondDenominator"], 7)
        self.assertEqual(result["thirdDenominator"], 8)
        self.assertNotEqual((result["firstDenominator"], result["secondDenominator"], result["thirdDenominator"]), (7, 8, 9))

    def test_negative_exponential_correction_is_micro_arcseconds_not_e19(self):
        result = negative_exponential_deflection_correction(1.32712440018e20, 6.957e8)
        self.assertAlmostEqual(result, -3.7169020232909573e-6, delta=1e-18)


if __name__ == "__main__":
    unittest.main()
