from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from checks.photon_cosmos_numerics import fragment_deflection_terms, fragment_redshift_terms


class PhotonCosmosNumericsTest(unittest.TestCase):
    def test_fragment_main_term_and_log_one_plus_correction(self):
        result = fragment_deflection_terms(1.32712440018e20, 6.957e8)
        self.assertAlmostEqual(result["baseArcseconds"], 1.751190325797501, places=12)
        self.assertAlmostEqual(result["pageLeadingArcseconds"], 0.43779758144937525, places=12)
        self.assertAlmostEqual(result["correctionArcseconds"], 1.8584470670700016e-6, delta=1e-18)
        self.assertAlmostEqual(result["totalArcseconds"], 1.7511921842445681, places=12)

    def test_fragment_redshift_arithmetic(self):
        result = fragment_redshift_terms(3.19431099780734)
        self.assertAlmostEqual(result["frequencyRatio"], 0.0409947611280232, places=16)
        self.assertAlmostEqual(result["redshift"], 23.39336082181535, places=12)


if __name__ == "__main__":
    unittest.main()
