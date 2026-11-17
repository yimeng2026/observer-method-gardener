from pathlib import Path
import math
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
try:
    from checks.field_equation_ansatz_checks import (
        far_field_yukawa,
        fr_coefficient_conditions,
        metric_versions,
        scale_and_shadow,
        simplified_constant_curvature,
    )
except ModuleNotFoundError:
    far_field_yukawa = fr_coefficient_conditions = None
    metric_versions = scale_and_shadow = None
    simplified_constant_curvature = None


class FieldEquationAnsatzChecksTest(unittest.TestCase):
    def setUp(self):
        self.assertTrue(all([
            far_field_yukawa, fr_coefficient_conditions,
            metric_versions, scale_and_shadow,
            simplified_constant_curvature,
        ]), "field-equation ansatz checker functions must exist")

    def assertClose(self, actual, expected, tolerance=1e-9):
        self.assertTrue(
            math.isclose(actual, expected, rel_tol=tolerance, abs_tol=0.0),
            (actual, expected),
        )

    def test_yukawa_form_solves_the_far_modified_helmholtz_equation(self):
        result = far_field_yukawa()
        self.assertLess(abs(result["relativeResidual"]), 1e-12)
        self.assertClose(result["ell"], math.sqrt(3) * 6e-13)

    def test_constant_curvature_cases_and_sign(self):
        result = simplified_constant_curvature()
        self.assertEqual(result["zeroCurvatureRoot"], 0.0)
        self.assertClose(result["nonzeroCurvatureRoot"], -1 / 0.02)
        self.assertClose(result["lambdaEffective"], -1 / (4 * 0.02))
        self.assertClose(result["curvatureFromLambda"], -1 / 0.02)
        self.assertTrue(result["negativeConstantCurvatureForPositiveXi"])

    def test_fr_form_requires_equal_coefficients_and_ignoring_other_terms(self):
        result = fr_coefficient_conditions()
        self.assertClose(result["fQuadraticCoefficient"], 0.01)
        self.assertClose(result["fPrimeLinearCoefficient"], 0.02)
        self.assertTrue(result["equalCoefficientsRecoverFr"])
        self.assertFalse(result["fullEquationAutomaticallyFr"])

    def test_two_metric_ansatze_have_different_core_curvature(self):
        result = metric_versions()
        self.assertClose(result["exponentialKappa"], 2 / 27)
        self.assertClose(result["rationalKappa"], 1 / 9)
        self.assertClose(result["exponentialCoreR"], 12 * 2 / 27)
        self.assertClose(result["rationalCoreR"], 12 / 9)
        self.assertClose(result["exponentialAAtZero"], 1.0)
        self.assertClose(result["rationalAAtZero"], 1.0)
        self.assertFalse(result["completeFieldSolutionEstablished"])

    def test_shadow_scale_and_micro_black_hole_radius(self):
        result = scale_and_shadow()
        self.assertClose(result["sgrShadowFractionSquared"], 2.5e-45)
        self.assertClose(result["microSchwarzschildRadius"], 1.485232053823733e-15)
        self.assertClose(result["lambdaOverMicroRadius"], 403.97727645003266)
        self.assertFalse(result["microRadiusCloseToLambda"])
        self.assertClose(result["lambdaOverPlanckLength"], 3.712e22, 2e-4)


if __name__ == "__main__":
    unittest.main()
