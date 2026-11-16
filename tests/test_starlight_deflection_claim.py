from pathlib import Path
import math
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from checks.starlight_deflection_claim import deflection_terms, log_expansion, prefactor_exponent

GM_SUN = 1.32712440018e20
R_SUN = 6.957e8
C = 299792458.0


class StarlightDeflectionClaimTest(unittest.TestCase):
    def test_solar_correction_is_micro_arcseconds_not_e19(self):
        result = deflection_terms(GM_SUN, R_SUN, C)
        self.assertAlmostEqual(result["b"], 2.122502570433235e-6, delta=1e-18)
        self.assertAlmostEqual(result["baseArcseconds"], 1.751190325797501, delta=1e-12)
        self.assertAlmostEqual(result["correctionArcseconds"], 1.8584470670658151e-6, delta=1e-15)
        self.assertGreater(result["correctionArcseconds"] / (math.pi * 1e-19), 1e12)
        self.assertGreater(result["correctionArcseconds"] / 6.958e-19, 1e12)
        self.assertNotAlmostEqual(result["relativeCorrection"], 4e-19)

    def test_log_times_exponential_series(self):
        b = 0.001
        result = log_expansion(b)
        self.assertAlmostEqual(result["seriesThirdOrder"], b - 1.5 * b**2 + 5 * b**3 / 6)
        self.assertLess(abs(result["logTimesExponential"] - result["seriesThirdOrder"]), 1e-9)

    def test_momentum_prefactor_is_only_algebra_without_a_metric(self):
        at_surface = prefactor_exponent(GM_SUN, R_SUN, R_SUN, C)
        at_double = prefactor_exponent(GM_SUN, R_SUN, 2 * R_SUN, C)
        b = GM_SUN / (R_SUN * C**2)
        self.assertAlmostEqual(at_surface, 0)
        self.assertAlmostEqual(at_double, b / 2)


if __name__ == "__main__":
    unittest.main()
