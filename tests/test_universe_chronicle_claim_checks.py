from pathlib import Path
import math
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
try:
    from checks.universe_chronicle_claim_checks import (
        black_hole,
        cosmology,
        cramer_claim,
        evidence_boundaries,
        navier_stokes,
        skewes_formula,
        w_boson_formula,
        yang_mills_gap,
    )
except ModuleNotFoundError:
    black_hole = cosmology = cramer_claim = evidence_boundaries = None
    navier_stokes = skewes_formula = w_boson_formula = yang_mills_gap = None


class UniverseChronicleClaimChecksTest(unittest.TestCase):
    def setUp(self):
        self.assertTrue(all([
            black_hole, cosmology, cramer_claim, evidence_boundaries,
            navier_stokes, skewes_formula, w_boson_formula, yang_mills_gap,
        ]), "universe chronicle checker functions must exist")

    def assertClose(self, actual, expected, tolerance=1e-9):
        self.assertTrue(
            math.isclose(actual, expected, rel_tol=tolerance, abs_tol=0.0),
            (actual, expected),
        )

    def test_age_text_correction_is_factor_ten(self):
        result = cosmology()
        self.assertClose(result["printedAgeYears"], 1.376e9)
        self.assertClose(result["correctedAgeYears"], 13.76e9)
        self.assertClose(result["correctionFactor"], 10)
        self.assertFalse(result["printedAgeSupported"])

    def test_hubble_asymptote_is_kept_but_torus_sign_conflicts(self):
        result = cosmology()
        self.assertClose(result["hInfinity"], 1.8067448231665922e-18)
        self.assertTrue(result["hInfinityArithmeticMatches"])
        self.assertFalse(result["torusDeSitterSignCompatible"])

    def test_black_hole_temperature_and_evaporation_claims_fail(self):
        result = black_hole()
        self.assertClose(result["temperatureK"], 6.170073824811395e-17)
        self.assertClose(result["evaporationYears"], 2.0956824232325815e94)
        self.assertFalse(result["claimedTemperatureSupported"])
        self.assertFalse(result["claimedEvaporationSupported"])

    def test_gap_formula_gives_kev_not_eighty_gev(self):
        result = yang_mills_gap()
        self.assertClose(result["factor"], 0.026198855601805827)
        self.assertClose(result["deltaGev"], 8.628415553666636e-6)
        self.assertClose(result["deltaKev"], 8.628415553666636)
        self.assertGreater(result["claimedGapOverComputed"], 9e6)
        self.assertFalse(result["claimed80GevSupported"])

    def test_w_mass_display_formula_is_not_80_379_gev(self):
        result = w_boson_formula()
        self.assertClose(result["massKg"], 7.417811844595707e-24)
        self.assertClose(result["massGev"], 4161.087278860976)
        self.assertClose(result["computedOverClaimed"], 51.76833848220276)
        self.assertFalse(result["claimedMassSupported"])
        self.assertFalse(result["onlyTwoParameters"])

    def test_ns_saturation_arithmetic_is_kept_without_unit_mapping_or_proof(self):
        result = navier_stokes()
        self.assertClose(result["omegaMax"], 7148006268849525914.0)
        self.assertTrue(result["omegaArithmeticMatches"])
        self.assertFalse(result["dimensionless75MappingDerived"])
        self.assertFalse(result["classicalGlobalRegularityProven"])

    def test_z_uncertainty_propagation_percentages_are_consistent(self):
        result = navier_stokes()
        self.assertClose(result["gradientRelativePercent"], 0.035)
        self.assertClose(result["ckRelativePercent"], 1 / 300 * 7)
        self.assertTrue(result["uncertaintyPropagationMatches"])

    def test_cramer_formula_confuses_sine_with_cosine(self):
        result = cramer_claim()
        self.assertClose(result["sinSquared"], 0.0006863800348442726)
        self.assertClose(result["cosSquared"], 0.9993136199651557)
        self.assertClose(result["cUsingPrintedSin"], 1855.0066728325484)
        self.assertClose(result["cUsingCos"], 1.2741140711957456)
        self.assertFalse(result["printedSinSupported"])
        self.assertFalse(result["claimedCUsingPrintedFormulaSupported"])
        self.assertFalse(result["conjectureProven"])

    def test_published_skewes_bound_conversion_is_kept(self):
        result = skewes_formula()
        self.assertClose(result["publishedLog10"], 316.1452457131331)
        self.assertClose(result["publishedCoefficient"], 1.3971586154525363)
        self.assertTrue(result["publishedConversionMatches"])

    def test_proposed_skewes_exponent_is_dimensionful_and_wrong(self):
        result = skewes_formula()
        self.assertClose(result["proposedExponent"], 10487679358603.486)
        self.assertClose(result["proposedLog10"], 4554741273412.1294)
        self.assertFalse(result["dimensionallyClosed"])
        self.assertFalse(result["proposedBoundMatchesPublished"])

    def test_book_data_and_millennium_evidence_are_missing(self):
        result = evidence_boundaries()
        self.assertTrue(result["selfCorrectionRecorded"])
        self.assertFalse(result["completedBookProvided"])
        self.assertFalse(result["rawDatasetsProvided"])
        self.assertFalse(result["axiomaticYangMillsConstruction"])
        self.assertFalse(result["classicalNavierStokesProof"])
        self.assertFalse(result["onlyTwoParameters"])
        self.assertFalse(result["prizeRecognitionProvided"])


if __name__ == "__main__":
    unittest.main()
