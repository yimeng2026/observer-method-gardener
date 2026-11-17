from pathlib import Path
import sys
import unittest

import mpmath as mp

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
try:
    from checks.heptadecagon_force_ellipse_checks import (
        constant_force_example,
        ellipse_perimeter_checks,
        heptadecagon_radicals,
    )
except ModuleNotFoundError:
    constant_force_example = ellipse_perimeter_checks = None
    heptadecagon_radicals = None


class HeptadecagonForceEllipseChecksTest(unittest.TestCase):
    def setUp(self):
        mp.mp.dps = 70
        self.assertTrue(all([
            constant_force_example, ellipse_perimeter_checks,
            heptadecagon_radicals,
        ]), "heptadecagon, force and ellipse checker functions must exist")

    def test_radical_cosine_and_tangent_match_direct_trigonometry(self):
        result = heptadecagon_radicals()
        self.assertLess(abs(mp.mpf(result["cosineDifference"])), mp.mpf("1e-60"))
        self.assertLess(abs(mp.mpf(result["tangentDifference"])), mp.mpf("1e-60"))
        self.assertLess(
            abs(mp.mpf(result["directTangent"]) - mp.mpf("0.387402063885491516883567189432960618852670798292614028")),
            mp.mpf("1e-14"),
        )
        self.assertGreater(mp.mpf(result["deltaRadicand"]), 0)

    def test_constant_force_closed_time_matches_independent_integration(self):
        result = constant_force_example()
        self.assertLess(
            abs(mp.mpf(result["closedNormalizedTime"]) - mp.mpf("0.686140661634507")),
            mp.mpf("1e-14"),
        )
        self.assertLess(
            abs(mp.mpf(result["closedNormalizedTime"]) - mp.mpf(result["integratedNormalizedTime"])),
            mp.mpf("1e-40"),
        )
        self.assertGreater(mp.mpf(result["finalGamma"]), mp.mpf(result["initialGamma"]))

    def test_ellipse_perimeter_matches_direct_integral_and_displayed_decimal(self):
        result = ellipse_perimeter_checks()
        self.assertLess(
            abs(mp.mpf(result["exact"]) - mp.mpf(result["directIntegral"])),
            mp.mpf("1e-35"),
        )
        self.assertLess(
            abs(mp.mpf(result["exact"]) - mp.mpf("12489.0023036622094390187216477")),
            mp.mpf("1e-9"),
        )

    def test_wolfram_transformed_integral_matches_standard_elliptic_value(self):
        result = ellipse_perimeter_checks()
        self.assertLess(
            abs(mp.mpf(result["exact"]) - mp.mpf(result["wolframTransformedIntegral"])),
            mp.mpf("1e-20"),
        )


if __name__ == "__main__":
    unittest.main()
