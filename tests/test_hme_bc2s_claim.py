from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from checks.hme_bc2s_claim import audit_hme_bc2s_claim


class HmeBc2sClaimTest(unittest.TestCase):
    def test_observed_mass_predates_and_contradicts_the_claimed_window(self):
        result = audit_hme_bc2s_claim()
        self.assertEqual(result["absoluteDifferenceMeV"], 39.0)
        self.assertTrue(result["outsideClaimedPlusMinus15MeV"])
        self.assertTrue(result["exceedsOwn30MeVRevisionThreshold"])
        self.assertTrue(result["observationPredatesPost"])
        self.assertFalse(result["evidenceUpgrade"])


if __name__ == "__main__":
    unittest.main()
