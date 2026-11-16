from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from checks.solar_pressure_units_claim import magnetic_gaussian_pa, naive_gaussian_with_tesla, pressure_components


class SolarPressureUnitsClaimTest(unittest.TestCase):
    def test_gas_and_radiation_terms(self):
        result = pressure_components(1e-7, 5778.0, 0.6, 0.01)
        self.assertAlmostEqual(result["gasPa"], 7.944543208106085, delta=1e-12)
        self.assertAlmostEqual(result["radiationPa"], 0.28108645630567014, delta=1e-12)
        self.assertAlmostEqual(result["magneticPa"], 39.78873577297384, delta=1e-10)
        self.assertAlmostEqual(result["totalSI"], 48.0143654373856, delta=1e-10)

    def test_si_and_gaussian_magnetic_pressures_agree_after_conversion(self):
        si = pressure_components(1e-7, 5778.0, 0.6, 0.01)["magneticPa"]
        self.assertAlmostEqual(magnetic_gaussian_pa(100.0), 39.78873577297384, delta=1e-10)
        self.assertAlmostEqual(magnetic_gaussian_pa(100.0), si, delta=1e-10)

    def test_naive_tesla_insertion_in_gaussian_formula_is_not_si(self):
        naive = naive_gaussian_with_tesla(0.01)
        self.assertAlmostEqual(naive, 3.9788735772973834e-6, delta=1e-16)
        self.assertNotAlmostEqual(naive, 39.78873577297384)

    def test_invalid_inputs_are_rejected(self):
        for args in [(0, 5778, 0.6, 0.01), (1e-7, 0, 0.6, 0.01), (1e-7, 5778, 0, 0.01)]:
            with self.assertRaises(ValueError):
                pressure_components(*args)


if __name__ == "__main__":
    unittest.main()
