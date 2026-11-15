import math
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from checks.empirical_claims import summarize_percentage_errors


class EmpiricalClaimsTest(unittest.TestCase):
    def test_published_galaxy_table_has_reproducible_summary(self):
        result = summarize_percentage_errors(
            [210, 220, 230, 235, 232, 215, 190],
            [213, 219, 228, 236, 234, 218, 195],
        )
        self.assertAlmostEqual(result["rmsAbsolutePercent"], 1.3522477588767507)
        self.assertAlmostEqual(result["maxAbsolutePercent"], 2.631578947368421)
        self.assertEqual(len(result["signedPercentErrors"]), 7)

    def test_invalid_table_is_rejected(self):
        for observed, predicted in [([], []), ([1], [1, 2]), ([0], [1]), ([math.nan], [1])]:
            with self.assertRaises(ValueError):
                summarize_percentage_errors(observed, predicted)


if __name__ == "__main__":
    unittest.main()
