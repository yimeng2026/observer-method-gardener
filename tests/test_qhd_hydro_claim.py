from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from checks.qhd_hydro_claim import audit_qhd_hydro_claim


class QhdHydroClaimTest(unittest.TestCase):
    def test_best_and_failed_public_examples_are_both_retained(self):
        result = audit_qhd_hydro_claim()
        self.assertAlmostEqual(result["meanAbsoluteErrorM"], 0.05)
        self.assertAlmostEqual(result["maxAbsoluteErrorM"], 0.09)
        self.assertTrue(result["directionMismatchExamples"][0]["station"] == "重庆")
        self.assertFalse(result["evidenceUpgrade"])


if __name__ == "__main__":
    unittest.main()
