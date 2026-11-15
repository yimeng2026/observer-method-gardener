from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from checks.dsf_claim import audit_dsf_claim


class DsfClaimTest(unittest.TestCase):
    def test_hubble_percent_and_cmb_exponential_are_reproducible(self):
        result = audit_dsf_claim()
        self.assertEqual(result["hubbleRelativePercentRange"], [0.1, 1.0])
        self.assertFalse(result["hubbleRangeMatchesTenPercentClaim"])
        self.assertAlmostEqual(result["cmbExponentialFactor"], 0.999999999999986)
        self.assertFalse(result["evidenceUpgrade"])


if __name__ == "__main__":
    unittest.main()
