from pathlib import Path
import math
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
try:
    from checks.bell_geometry_claim_checks import (
        black_hole_case,
        chsh_baseline,
        correction_versions,
        energy_predictions,
        energy_scale,
        evidence_boundaries,
        interference_baseline,
        wilson_loop,
    )
except ModuleNotFoundError:
    black_hole_case = chsh_baseline = correction_versions = None
    energy_predictions = energy_scale = evidence_boundaries = None
    interference_baseline = wilson_loop = None


class BellGeometryClaimChecksTest(unittest.TestCase):
    def setUp(self):
        self.assertTrue(all([
            black_hole_case, chsh_baseline, correction_versions,
            energy_predictions, energy_scale, evidence_boundaries,
            interference_baseline, wilson_loop,
        ]), "Bell geometry checker functions must exist")

    def assertClose(self, actual, expected, tolerance=1e-9):
        self.assertTrue(
            math.isclose(actual, expected, rel_tol=tolerance, abs_tol=0.0),
            (actual, expected),
        )

    def test_standard_chsh_maximum_is_not_a_constant_for_every_setting(self):
        result = chsh_baseline()
        self.assertClose(result["singletMaximum"], 2 * math.sqrt(2))
        self.assertClose(result["sameDirectionCorrelation"], -1)
        self.assertClose(result["orthogonalCorrelation"], 0)
        self.assertFalse(result["standardQmAlwaysMaximal"])
        self.assertFalse(result["belowTwoProvesLocalRealism"])

    def test_wilson_loop_at_z_one_seventieth_is_not_minus_sqrt_half(self):
        result = wilson_loop()
        self.assertClose(result["phaseOverPi"], 17.5)
        self.assertAlmostEqual(result["computedCorrelation"], 0, places=14)
        self.assertAlmostEqual(result["computedS"], 0, places=14)
        self.assertFalse(result["claimedCorrelationSupported"])
        self.assertFalse(result["smallZTaylorExpansionValid"])

    def test_z_one_recovers_magnitude_but_not_printed_negative_sign(self):
        result = wilson_loop()
        self.assertClose(result["correlationAtZOne"], math.sqrt(2) / 2)
        self.assertClose(result["sAtZOne"], 2 * math.sqrt(2))

    def test_curvature_versions_and_topological_dimensions_conflict(self):
        result = correction_versions()
        self.assertClose(result["curvatureCoefficientRatio"], 4900)
        self.assertFalse(result["curvatureVersionsConsistent"])
        self.assertFalse(result["topologicalCorrectionDimensionless"])

    def test_characteristic_energy_is_329_kev_not_207_gev(self):
        result = energy_scale()
        self.assertClose(result["energyJoules"], 5.2766601712076245e-14)
        self.assertClose(result["energyGeV"], 0.0003293432234143807)
        self.assertClose(result["claimedOverComputed"], 628523.6351729999)
        self.assertFalse(result["claimedEnergySupported"])

    def test_tev_and_fcc_energy_ratios(self):
        result = energy_predictions()
        self.assertClose(result["tevRatioSquaredUsingPrintedScale"], (1000 / 207)**2)
        self.assertGreater(result["tevRatioSquaredUsingPrintedScale"], 23)
        self.assertFalse(result["tevTenToMinusFourSupported"])
        self.assertClose(result["fccRatioSquaredUsingPrintedScale"], (100 / 207)**2)
        self.assertTrue(result["fccInternalArithmeticMatches"])

    def test_cosmological_anisotropy_scale_is_not_one_e_minus_five(self):
        result = energy_predictions()
        self.assertClose(result["cosmologicalKappa"], 3.58984317409e-77)
        self.assertFalse(result["cosmologicalKappaClaimSupported"])

    def test_black_hole_case_arithmetic_is_kept_without_locality_claim(self):
        result = black_hole_case()
        self.assertClose(result["visibilityProduct"], 0.0065)
        self.assertClose(result["predictedS"], 2 * math.sqrt(2) * 0.0065)
        self.assertTrue(result["arithmeticConsistent"])
        self.assertFalse(result["factorsIndependentlyDerived"])
        self.assertFalse(result["localRealismRestored"])

    def test_interference_algebra_and_visible_wavelength_ratio(self):
        result = interference_baseline()
        self.assertClose(result["twoEqualAmplitudesAtZeroPhase"], 4)
        self.assertClose(result["visibleLambdaRatio"], 5.99153e-13 / 5e-7)
        self.assertTrue(result["visibleRatioOrderSupported"])
        self.assertFalse(result["extraPhaseMeasured"])

    def test_experimental_and_agn_evidence_are_not_provided(self):
        result = evidence_boundaries()
        self.assertFalse(result["rawBellDatasetProvided"])
        self.assertFalse(result["prospectiveProtocolProvided"])
        self.assertFalse(result["independentReplicationProvided"])
        self.assertFalse(result["agnAngularCorrelationIsBellTest"])


if __name__ == "__main__":
    unittest.main()
