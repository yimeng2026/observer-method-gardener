from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from checks.fine_structure_thermal_claim import energy_alpha_relative, energy_fluctuation_ratio, thermal_alpha_coefficient


class FineStructureThermalClaimTest(unittest.TestCase):
    def test_energy_derivative_sign_and_one_kelvin_example(self):
        delta_e = 1.5 * 8.617333262145e-5
        result = energy_alpha_relative(delta_e, -13.6)
        self.assertAlmostEqual(result, -4.752205843094669e-6, delta=1e-16)
        self.assertLess(result, 0)

    def test_thermal_coefficient_is_not_1p43e_minus_6(self):
        result = thermal_alpha_coefficient(300.0)
        self.assertAlmostEqual(result["absoluteCoefficient"], 0.0014256617529284006, delta=1e-15)
        self.assertAlmostEqual(result["signedCoefficient"], -0.0014256617529284006, delta=1e-15)
        self.assertNotAlmostEqual(result["absoluteCoefficient"], 1.43e-6)

    def test_energy_fluctuation_requires_division_by_energy_scale(self):
        result = energy_fluctuation_ratio(300.0, 1.5 * 8.617333262145e-5)
        self.assertAlmostEqual(result["sigmaEnergyEV"], 0.03166210415365272, delta=1e-14)
        self.assertAlmostEqual(result["relativeFluctuation"], 0.0023280958936509354, delta=1e-14)

    def test_invalid_inputs_are_rejected(self):
        with self.assertRaises(ValueError):
            energy_alpha_relative(1.0, 0.0)
        with self.assertRaises(ValueError):
            thermal_alpha_coefficient(0.0)


if __name__ == "__main__":
    unittest.main()
