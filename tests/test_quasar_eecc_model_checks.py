from pathlib import Path
import math
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
try:
    from checks.quasar_eecc_model_checks import (
        blr_quadrupole,
        energy_and_stability,
        jet_and_orbit_baseline,
        kernel_and_units,
        redshift_and_period,
        sgr_a_comment,
    )
except ModuleNotFoundError:
    blr_quadrupole = energy_and_stability = None
    jet_and_orbit_baseline = kernel_and_units = None
    redshift_and_period = sgr_a_comment = None


class QuasarEeccModelChecksTest(unittest.TestCase):
    def setUp(self):
        self.assertTrue(all([
            blr_quadrupole, energy_and_stability, jet_and_orbit_baseline,
            kernel_and_units, redshift_and_period, sgr_a_comment,
        ]), "quasar EECC checker functions must exist")

    def assertClose(self, actual, expected, tolerance=1e-9):
        self.assertTrue(
            math.isclose(actual, expected, rel_tol=tolerance, abs_tol=0.0),
            (actual, expected),
        )

    def test_kernel_vanishes_at_small_z_and_mass_formula_needs_c(self):
        result = kernel_and_units()
        self.assertLess(result["kernelAt003"], 1e-12)
        self.assertLess(result["kernelAt00123"], 1e-12)
        self.assertLess(result["kernelAt0005"], 1e-12)
        self.assertFalse(result["pointNineKernelCompatible"])
        self.assertClose(result["printedMomentumOverMass"], 299792458.0)

    def test_jet_opening_baseline_is_six_degrees_not_point_one_degree(self):
        result = jet_and_orbit_baseline()
        self.assertClose(result["openingBaselineRadians"], math.sqrt(10) / 30)
        self.assertGreater(result["openingRatioToPointOneDegree"], 60)
        self.assertFalse(result["pointOneDegreeBaselineReproduced"])

    def test_polarization_angle_and_nodal_coefficient(self):
        result = jet_and_orbit_baseline()
        self.assertClose(result["evpaStandard"], math.pi / 8)
        self.assertClose(result["evpaPrinted"], math.pi / 4)
        self.assertClose(result["nodalPrintedOverStandard"], 4.0)

    def test_redshift_exponents_are_not_the_claimed_minus_065(self):
        result = redshift_and_period()
        self.assertClose(result["alphaMinusGamma"], -1.27)
        self.assertClose(result["gammaMinusTwoAlpha"], 0.99)
        self.assertNotEqual(result["alphaMinusGamma"], -0.65)
        self.assertNotEqual(result["gammaMinusTwoAlpha"], -0.65)
        self.assertClose(result["observedExponentAfterTimeDilation"], 0.35)

    def test_three_c_273_period_is_not_186_years_in_either_calibration(self):
        result = redshift_and_period()
        self.assertGreater(result["periodEarlierCalibration"], 70)
        self.assertLess(result["periodEarlierCalibration"], 72)
        self.assertGreater(result["periodLaterCalibration"], 83)
        self.assertLess(result["periodLaterCalibration"], 85)
        self.assertGreater(result["periodEarlierOverTarget"], 30)
        self.assertClose(result["opticalMassExponentAfterSubstitution"], -1.0)
        self.assertClose(result["opticalRedshiftExponentAfterSubstitution"], 0.075)

    def test_geometric_efficiency_exceeds_unity_and_power_units_jump(self):
        result = energy_and_stability()
        self.assertClose(result["geometricFactor"], 1000 * (1 + math.log(1e6)))
        self.assertGreater(result["extractionEfficiency"], 1.0)
        self.assertGreater(result["powerUnitJumpRatio"], 1e7)
        self.assertTrue(result["powerFractionOmitsGeometry"])

    def test_stability_and_spin_equilibrium_are_not_derived(self):
        result = energy_and_stability()
        self.assertFalse(result["stiffnessMatrixProvided"])
        self.assertFalse(result["equilibriumSpinDemonstrated"])
        self.assertFalse(result["observationalFitPerformed"])

    def test_quadrupole_derivative_has_opposite_sign_to_printed_equation(self):
        result = blr_quadrupole()
        self.assertClose(result["omegaSquaredQuadrupoleCoefficient"], 1.5)
        self.assertClose(result["printedQuadrupoleCoefficient"], -1.5)
        self.assertClose(result["correctSignedRelativeShift"], -7.5e-12)
        self.assertClose(result["printedSignedRelativeShift"], 7.5e-12)

    def test_blr_amplitude_and_final_exponent_fail_their_own_numbers(self):
        result = blr_quadrupole()
        self.assertGreater(result["claimedInstantOverPrintedArithmetic"], 3e9)
        self.assertClose(result["finalFormulaValue"], 250.0)
        self.assertNotEqual(result["finalFormulaValue"], 0.28)

    def test_sgr_a_flatness_is_many_orders_below_the_claim(self):
        result = sgr_a_comment()
        self.assertLess(result["zetaFromCommentFormula"], 1e-22)
        self.assertGreater(result["claimedZetaOverComputed"], 1e17)
        self.assertLess(result["polarRadiusFromComputedZeta"], 1e-10)

    def test_sgr_a_equatorial_shape_and_radius_ratio_are_not_near_circle(self):
        result = sgr_a_comment()
        self.assertLess(result["etaFromCommentFormula"], -1e7)
        self.assertClose(result["semiMajorOverSchwarzschild"], 5.9375)
        self.assertFalse(result["nearCircleAndThinDiskConsistent"])


if __name__ == "__main__":
    unittest.main()
