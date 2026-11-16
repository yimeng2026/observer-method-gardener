from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from checks.dt_fusion_claim import dt_reference, evaluate_displayed_claim


class DTFusionClaimTest(unittest.TestCase):
    def test_atomic_masses_recover_standard_dt_energy(self):
        result = dt_reference()
        self.assertAlmostEqual(result["massDefectU"], 0.01888289, delta=1e-8)
        self.assertAlmostEqual(result["energyMeV"], 17.59, delta=0.02)
        self.assertGreater(result["massDefectKg"], 3.0e-29)

    def test_displayed_energy_is_not_the_standard_dt_value(self):
        result = evaluate_displayed_claim()
        self.assertLess(result["displayedEnergyOverReference"], 0.30)
        self.assertLess(result["displayedMassOverReference"], 0.30)
        self.assertFalse(result["matchesReference"])
        self.assertTrue(result["displayedMassEnergyInternallyConsistent"])


if __name__ == "__main__":
    unittest.main()
