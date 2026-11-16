from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from checks.solar_corona_claim import clock_unit_variants, corona_volumetric_heating, planck_ratio_squared


class SolarCoronaClaimTest(unittest.TestCase):
    def test_displayed_planck_ratio_has_the_opposite_exponent(self):
        result = planck_ratio_squared(lambda_c_m=6.8e-12, planck_length_m=1.616255e-35)
        self.assertGreater(result["displayedRatioSquared"], 1e47)
        self.assertAlmostEqual(result["reciprocalRatioSquared"], 5.645e-48, delta=1e-50)
        self.assertFalse(result["matchesDisplayedOneEMinus48"])

    def test_corona_energy_arithmetic_reveals_thousandfold_mismatch(self):
        self.assertEqual(corona_volumetric_heating(flux_w_m2=2.1e7, area_m2=1e18, height_m=1e8), 0.21)

    def test_satellite_seconds_and_nanoseconds_are_not_interchangeable(self):
        variants = clock_unit_variants()
        self.assertEqual(variants["pointOneSecondNs"], 1e8)
        self.assertEqual(variants["pointOneNanosecondNs"], 0.1)
        self.assertEqual(variants["secondsToNanosecondsRatio"], 1e9)
        self.assertEqual(variants["annualRateNsPerYear"], 0.15)


if __name__ == "__main__":
    unittest.main()
