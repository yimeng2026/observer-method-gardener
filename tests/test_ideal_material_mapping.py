from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from checks.ideal_material_mapping import electron_length_conventions, lattice_table_errors_percent


class IdealMaterialMappingTest(unittest.TestCase):
    def test_displayed_electron_length_requires_reduced_compton_convention(self):
        result = electron_length_conventions()
        self.assertAlmostEqual(result["hTimesCOverElectronEnergyM"], 2.426310238e-12, delta=1e-21)
        self.assertAlmostEqual(result["hbarTimesCOverElectronEnergyM"], 3.86159268e-13, delta=1e-21)
        self.assertAlmostEqual(result["conventionRatio"], 6.283185307, delta=1e-9)

    def test_lattice_table_arithmetic_does_not_establish_prediction(self):
        errors = lattice_table_errors_percent()
        self.assertAlmostEqual(errors["Al"], 0.4938271605, delta=1e-9)
        self.assertAlmostEqual(errors["Cu"], 0.5540166205, delta=1e-9)
        self.assertAlmostEqual(errors["Fe"], 0.6968641115, delta=1e-9)
        self.assertTrue(all(value < 1.0 for value in errors.values()))


if __name__ == "__main__":
    unittest.main()
