from pathlib import Path
import math
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from checks.mercury_precession_claim import orbital_parameters, precession_arcsec_century, secular_particular_coefficient

GM = 1.32712440018e20
A = 5.791e10
E = 0.2056
C = 299792458.0


class MercuryPrecessionClaimTest(unittest.TestCase):
    def test_standard_baseline_and_missing_factor_three(self):
        result = orbital_parameters(GM, A, E, C)
        self.assertAlmostEqual(result["alpha2"], 2.662405418567655e-8, delta=1e-18)
        self.assertAlmostEqual(result["sixPiOverTwoPi"], 3.0)
        self.assertAlmostEqual(result["twoPiArcsecPerCentury"], 42.97941704149046 / 3, delta=1e-8)
        self.assertAlmostEqual(result["sixPiArcsecPerCentury"], 42.97941704149046, delta=1e-8)

    def test_characteristic_speed_is_not_perihelion_speed(self):
        result = orbital_parameters(GM, A, E, C)
        self.assertAlmostEqual(result["characteristicSpeed"], 48916.77276594036, delta=1e-6)
        self.assertAlmostEqual(result["perihelionSpeed"], 58974.0612466177, delta=1e-6)
        self.assertNotAlmostEqual(result["characteristicSpeed"], result["perihelionSpeed"])

    def test_displayed_resonant_particular_solution_has_only_two_pi(self):
        result = secular_particular_coefficient(GM, C, A * (1 - E**2), E)
        self.assertAlmostEqual(result["twiceB"], result["forcingCosineCoefficient"])
        self.assertAlmostEqual(result["precessionRadians"], 2 * math.pi * result["alpha2"])
        self.assertNotAlmostEqual(result["precessionRadians"], 6 * math.pi * result["alpha2"])

    def test_period_conversion_is_explicit(self):
        result = precession_arcsec_century(GM, A, E, 87.9691, C)
        self.assertAlmostEqual(result["orbitsPerCentury"], 415.2026109167878, delta=1e-8)
        self.assertAlmostEqual(result["arcsecPerCentury"], 42.97941704149046, delta=1e-8)


if __name__ == "__main__":
    unittest.main()
