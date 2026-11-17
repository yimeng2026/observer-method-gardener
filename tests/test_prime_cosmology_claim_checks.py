from pathlib import Path
import math
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
try:
    from checks.prime_cosmology_claim_checks import (
        constant_formulas,
        euler_phi_identity,
        evidence_boundaries,
        prime_gap_formula,
        updated_gravity,
        zeta_zero_spacing,
    )
except ModuleNotFoundError:
    constant_formulas = euler_phi_identity = evidence_boundaries = None
    prime_gap_formula = updated_gravity = zeta_zero_spacing = None


class PrimeCosmologyClaimChecksTest(unittest.TestCase):
    def setUp(self):
        self.assertTrue(all([
            constant_formulas, euler_phi_identity, evidence_boundaries,
            prime_gap_formula, updated_gravity, zeta_zero_spacing,
        ]), "prime cosmology checker functions must exist")

    def assertClose(self, actual, expected, tolerance=1e-9):
        self.assertTrue(
            math.isclose(actual, expected, rel_tol=tolerance, abs_tol=0.0),
            (actual, expected),
        )

    def test_prime_gap_correction_is_large_and_negative_not_one(self):
        result = prime_gap_formula()
        self.assertClose(result["halfCotangent"], -19.078252238692455)
        self.assertClose(result["gammaOverPi"], 0.18373345259830798)
        self.assertClose(result["constantCorrection"], -18.894518786094147)
        self.assertFalse(result["claimedOneSupported"])

    def test_gap_formula_gives_negative_value_at_first_prime(self):
        result = prime_gap_formula()
        self.assertClose(result["gapAtP2"], -18.2013716055342)
        self.assertTrue(result["negativeAtP2"])
        self.assertTrue(result["logPrimeLeadingTermRetained"])

    def test_zero_spacing_has_factor_two_and_no_cmb_mapping(self):
        result = zeta_zero_spacing()
        self.assertClose(result["displayedCmbSpacing"], 3.8748858119929)
        self.assertClose(result["standardMeanSpacing"], 7.7497716239858)
        self.assertClose(result["displayedOverStandard"], 0.5)
        self.assertFalse(result["cmbMappingDerived"])
        self.assertFalse(result["primeErrorGueEstablished"])

    def test_euler_totient_divisor_convolution_is_exact(self):
        result = euler_phi_identity()
        self.assertTrue(result["divisorConvolutionHolds"])
        self.assertEqual(result["convolutionCheckedThrough"], 100)

    def test_euler_dirichlet_series_matches_independent_closed_form(self):
        result = euler_phi_identity()
        self.assertClose(result["partialAtFour"], 1.110626523169791)
        self.assertClose(result["closedAtFour"], 1.110626535326148)
        self.assertLess(result["absoluteDifference"], 2e-8)
        self.assertFalse(result["identityProvesFiveDimensionalOperator"])

    def test_fine_structure_formula_does_not_recover_alpha(self):
        result = constant_formulas()
        self.assertClose(result["alphaRhs"], 0.00028302798768656626)
        self.assertClose(result["alphaOverActual"], 0.03878502306136266)
        self.assertFalse(result["alphaFormulaMatches"])

    def test_original_gravity_and_cosmological_constant_formulas_fail(self):
        result = constant_formulas()
        self.assertClose(result["originalG"], 4.900749581343565e30)
        self.assertFalse(result["originalGMatches"])
        self.assertClose(result["cosmologicalConstant"], 2.82974121752258e22)
        self.assertFalse(result["cosmologicalConstantMatches"])

    def test_spin_polarization_angle_is_not_zero_or_point_468(self):
        result = updated_gravity()
        self.assertClose(result["cosThetaSp"], 0.9989490749343205)
        self.assertClose(result["thetaSp"], 0.04584995509700342)
        self.assertFalse(result["point468Supported"])

    def test_updated_gravity_versions_do_not_match_displayed_central_value(self):
        result = updated_gravity()
        self.assertClose(result["updatedG"], 7.44996740043774e-11)
        self.assertClose(result["updatedGOverMeasured"], 1.1162170415530828)
        self.assertFalse(result["updatedGMatches"])
        self.assertClose(result["gUsingPoint468"], 6.697490196588665e-11)
        self.assertClose(result["point468RelativeError"], 0.0034745511272590384)
        self.assertFalse(result["point468MatchesCentralValue"])

    def test_cross_domain_and_reference_evidence_is_missing(self):
        result = evidence_boundaries()
        self.assertFalse(result["spectralZetaEquivalenceProven"])
        self.assertFalse(result["rawPrimeDatasetProvided"])
        self.assertFalse(result["cmbDatasetProvided"])
        self.assertFalse(result["preregisteredCrossDomainStatisticProvided"])
        self.assertFalse(result["futureReferenceIsPublishedEvidence"])
        self.assertFalse(result["prlCitationVerified"])


if __name__ == "__main__":
    unittest.main()
