from pathlib import Path
import math
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
try:
    from checks.eebh_parameter_table_checks import (
        field_equation_boundary,
        gw_phase,
        m87_table,
        model_statistics,
        quadrupole_and_shadow,
        s02_orbit,
        sgr_a_table,
    )
except ModuleNotFoundError:
    field_equation_boundary = gw_phase = None
    m87_table = model_statistics = None
    quadrupole_and_shadow = s02_orbit = sgr_a_table = None


class EebhParameterTableChecksTest(unittest.TestCase):
    def setUp(self):
        self.assertTrue(all([
            field_equation_boundary, gw_phase, m87_table, model_statistics,
            quadrupole_and_shadow, s02_orbit, sgr_a_table,
        ]), "EEBH parameter-table checker functions must exist")

    def assertClose(self, actual, expected, tolerance=1e-9):
        self.assertTrue(
            math.isclose(actual, expected, rel_tol=tolerance, abs_tol=0.0),
            (actual, expected),
        )

    def test_m87_volume_density_and_gravitational_radius(self):
        result = m87_table()
        self.assertClose(result["aOverGravitationalRadius"], 0.0909375)
        self.assertGreater(result["volume"], 4e30)
        self.assertLess(result["volume"], 5e30)
        self.assertGreater(result["density"], 1e8)
        self.assertLess(result["density"], 2e8)
        self.assertGreater(result["densityFromDisplayedVolume"], 200)
        self.assertLess(result["densityFromDisplayedVolume"], 400)

    def test_m87_rotation_inertia_torque_and_period(self):
        result = m87_table()
        self.assertClose(result["gammaFromSpeed"], 1 / math.sqrt(1 - 0.98**2))
        self.assertClose(result["rotationPeriodHours"], 5.184, 0.01)
        self.assertGreater(result["angularMomentum"], 3e61)
        self.assertLess(result["angularMomentum"], 4e61)
        self.assertGreater(result["inertia"], 2e62)
        self.assertLess(result["inertia"], 3e62)
        self.assertGreater(result["amplification"], 2e4)
        self.assertLess(result["amplification"], 3e4)
        self.assertGreater(result["torqueOverDisplayedJ"], 3e-19)
        self.assertLess(result["torqueOverDisplayedJ"], 4e-19)
        self.assertGreater(result["periodFromDisplayedOmegaYears"], 9.0)
        self.assertLess(result["periodFromDisplayedOmegaYears"], 9.2)
        self.assertGreater(result["betaFromFormula"], 2e-8)
        self.assertLess(result["betaFromFormula"], 3e-8)

    def test_sgr_a_volume_density_and_gravitational_radius(self):
        result = sgr_a_table()
        self.assertClose(result["aOverGravitationalRadius"], 0.0893, 1e-4)
        self.assertGreater(result["volume"], 1e21)
        self.assertLess(result["volume"], 2e21)
        self.assertGreater(result["density"], 2e14)
        self.assertLess(result["density"], 3e14)
        self.assertGreater(result["densityFromDisplayedVolume"], 6e8)
        self.assertLess(result["densityFromDisplayedVolume"], 7e8)

    def test_sgr_a_rotation_amplification_torque_and_period(self):
        result = sgr_a_table()
        self.assertClose(result["gammaFromSpeed"], 1 / math.sqrt(1 - 0.70**2))
        self.assertClose(result["rotationPeriodHours"], 0.004715651299391284)
        self.assertGreater(result["angularMomentum"], 7e54)
        self.assertLess(result["angularMomentum"], 9e54)
        self.assertGreater(result["displayedJOverPhysical"], 1000)
        self.assertGreater(result["amplification"], 1500)
        self.assertLess(result["amplification"], 2200)
        self.assertGreater(result["torqueOverDisplayedJ"], 4e-25)
        self.assertLess(result["torqueOverDisplayedJ"], 5e-25)
        self.assertGreater(result["periodFromDisplayedOmegaYears"], 7000)
        self.assertLess(result["periodFromDisplayedOmegaYears"], 8000)

    def test_quadrupole_versions_and_shadow_formula(self):
        result = quadrupole_and_shadow()
        self.assertLess(abs(result["m87J2FromEarlierFormula"]), 0.001)
        self.assertLess(abs(result["sgrJ2FromEarlierFormula"]), 0.001)
        self.assertLess(abs(result["sgrJ2FromLaterFormula"]), 0.002)
        self.assertClose(result["sgrShadowFormulaValue"], -0.33875)
        self.assertNotEqual(result["sgrShadowFormulaValue"], 0.72)

    def test_s02_gr_precession_and_quadrupole_ratio(self):
        result = s02_orbit()
        self.assertGreater(result["grDegrees"], 0.20)
        self.assertLess(result["grDegrees"], 0.22)
        self.assertLess(abs(result["j2CorrectionRatio"]), 0.0004)
        self.assertGreater(result["totalFromPrintedFormulas"], 0.20)
        self.assertLess(result["totalFromPrintedFormulas"], 0.22)
        self.assertFalse(result["thirtySixPercentSupported"])

    def test_model_evidence_ratios_and_statistical_boundary(self):
        result = model_statistics()
        self.assertClose(result["kerrNewtonLogRatio"], 41.8)
        self.assertClose(result["eebhNewtonLogRatio"], 60.0)
        self.assertClose(result["kerrNewtonExpectedRatio"], math.exp(41.8))
        self.assertClose(result["eebhNewtonExpectedRatio"], math.exp(60.0))
        self.assertFalse(result["parameterCountsAndLikelihoodProvided"])

    def test_gw_phase_frequency_power_and_magnitude(self):
        result = gw_phase()
        self.assertClose(result["frequencyExponentAfterCancellation"], -1.0)
        self.assertGreater(result["phase"], 1e-37)
        self.assertLess(result["phase"], 1e-35)
        self.assertGreater(result["claimedPhaseOverComputed"], 1e36)
        self.assertClose(result["snrMismatchProduct"], 4.8)
        self.assertFalse(result["mismatchDerivedFromWaveform"])

    def test_field_equation_and_observation_boundaries(self):
        result = field_equation_boundary()
        self.assertFalse(result["bianchiClosureShown"])
        self.assertFalse(result["exactSolutionProvided"])
        self.assertFalse(result["observationalFitPerformed"])
        self.assertFalse(result["evidenceUpgrade"])


if __name__ == "__main__":
    unittest.main()
