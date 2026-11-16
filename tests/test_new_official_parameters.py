from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from checks.new_official_parameters import parameter_variants


class NewOfficialParametersTest(unittest.TestCase):
    def test_displayed_base_mass_matches_but_graviton_values_conflict(self):
        result = parameter_variants()
        self.assertAlmostEqual(result["laterMassMeV"], 0.00485, delta=0.00001)
        self.assertAlmostEqual(result["displayedMassRatio"], 1.0, delta=0.01)
        self.assertAlmostEqual(result["z0Ratio"], 10.0, delta=0.1)
        self.assertAlmostEqual(result["darkMatterDisplayedKgEV"], 0.773, delta=0.001)
        self.assertAlmostEqual(result["gravitonFormulaMeV"], 0.002402618010883438, delta=1e-12)
        self.assertNotAlmostEqual(result["gravitonDisplayedKgEV"], 0.069, delta=1e-6)

    def test_mass_is_not_fixed_without_version_and_unit_ledger(self):
        result = parameter_variants()
        self.assertFalse(result["parametersEndogenous"])


if __name__ == "__main__":
    unittest.main()
