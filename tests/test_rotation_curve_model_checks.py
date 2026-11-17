from pathlib import Path
import math
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
try:
    from checks.rotation_curve_model_checks import (
        dark_matter_fraction,
        galaxy_fit_statistics,
        observation_arithmetic,
        rotation_curve_limits,
        scale_and_dark_matter,
    )
except ModuleNotFoundError:
    dark_matter_fraction = galaxy_fit_statistics = observation_arithmetic = None
    rotation_curve_limits = scale_and_dark_matter = None


class RotationCurveModelChecksTest(unittest.TestCase):
    def setUp(self):
        self.assertTrue(all([
            dark_matter_fraction, galaxy_fit_statistics, observation_arithmetic,
            rotation_curve_limits, scale_and_dark_matter,
        ]))

    def assertClose(self, actual, expected, tolerance=1e-9):
        self.assertTrue(math.isclose(actual, expected, rel_tol=tolerance, abs_tol=tolerance), (actual, expected))

    def test_scale_is_61_decades_and_dark_mass_ratio_is_not_499(self):
        result = scale_and_dark_matter()
        self.assertEqual(result["scaleDecades"], 61)
        self.assertClose(result["darkMatterRatio"], 2927423868252617.5)
        self.assertNotEqual(result["darkMatterRatio"], 499.697)

    def test_positive_inverse_square_term_diverges_at_center(self):
        result = rotation_curve_limits()
        self.assertClose(result["smallXProduct"], 0.5)
        self.assertEqual(result["zeroTermCentralVelocityExponent"], 0.5)
        self.assertEqual(result["requiredFiniteCoreVelocityExponent"], 1.0)
        self.assertNotEqual(result["zeroTermCentralVelocityExponent"], 1.0)

    def test_outer_slope_formula_is_not_the_derivative_of_rotation_curve(self):
        result = rotation_curve_limits()
        self.assertClose(result["actualOuterSlope"], -0.46098487181169745)
        self.assertClose(result["displayedOuterSlope"], -5.000002499999999e-7)
        self.assertNotEqual(result["actualOuterSlope"], result["displayedOuterSlope"])

    def test_dark_matter_fraction_requires_a_physical_domain(self):
        result = dark_matter_fraction()
        self.assertEqual(result["atZero"], 1.0)
        self.assertEqual(result["atOne"], 0.0)
        self.assertClose(result["atOnePointTwo"], -0.0906070659236271)
        self.assertLess(result["atOnePointTwo"], 0.0)

    def test_galaxy_fit_statistics_are_not_the_displayed_values(self):
        result = galaxy_fit_statistics()
        self.assertClose(result["milkyWayChi2PerPoint"], 0.4492063492063491)
        self.assertClose(result["m31Chi2PerPoint"], 0.1421464285714286)
        self.assertNotEqual(result["milkyWayChi2PerPoint"], 0.68)
        self.assertNotEqual(result["m31Chi2PerPoint"], 0.45)

    def test_outer_slopes_do_not_match_the_displayed_approximations(self):
        result = galaxy_fit_statistics()
        self.assertClose(result["milkyWayOuterSlope"], -0.7142857142857143)
        self.assertClose(result["m31OuterSlope"], -1.0)
        self.assertNotEqual(result["milkyWayOuterSlope"], -0.48)
        self.assertNotEqual(result["m31OuterSlope"], -0.51)

    def test_three_observation_residuals_are_reproduced(self):
        result = observation_arithmetic()
        self.assertClose(result["w0Sigma"], 1 / 15)
        self.assertClose(result["heliumSigma"], 0.05)
        self.assertClose(result["milkyWaySigma"], 1.9)


if __name__ == "__main__":
    unittest.main()
