from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from checks.six_force_engineering import casimir_energy_density_magnitude, fusion_gain


class SixForceEngineeringTest(unittest.TestCase):
    def test_displayed_fusion_inputs_and_output_imply_gain_sixty(self):
        self.assertEqual(fusion_gain(input_powers_mw=[10.0, 5.0, 5.0], fusion_output_mw=1200.0), 60.0)

    def test_displayed_casimir_formula_does_not_give_one_kj_per_m3(self):
        result = casimir_energy_density_magnitude(distance_m=1e-9)
        self.assertGreater(result, 6e8)
        self.assertLess(result, 7e8)


if __name__ == "__main__":
    unittest.main()
