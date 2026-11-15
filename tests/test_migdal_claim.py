from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from checks.migdal_claim import audit_migdal_claim


class MigdalClaimTest(unittest.TestCase):
    def test_public_numbers_reproduce_arithmetic_but_not_enhancement_claim(self):
        result = audit_migdal_claim()
        self.assertAlmostEqual(result["relativeEnergyDifferencePercent"], 0.02688172043012128)
        self.assertAlmostEqual(result["enhancementExponent"], 0.9916666666666666)
        self.assertAlmostEqual(result["enhancementFactor"], 1.5259797058775284)
        self.assertFalse(result["enhancementMatchesPublishedHundredToThousandRange"])
        self.assertFalse(result["evidenceUpgrade"])

    def test_invalid_enhancement_inputs_are_rejected(self):
        for ratio, xi, theta in [(0, 1, 1), (1, -1, 1), (1, 1, float("nan"))]:
            with self.assertRaises(ValueError):
                audit_migdal_claim(ratio=ratio, xi=xi, theta_m_radians=theta)


if __name__ == "__main__":
    unittest.main()
