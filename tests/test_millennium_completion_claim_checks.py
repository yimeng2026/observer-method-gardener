from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
try:
    from checks.millennium_completion_claim_checks import (
        payment_terms,
        problem_registry,
        proof_logic,
        zero_table,
    )
except ModuleNotFoundError:
    payment_terms = problem_registry = proof_logic = zero_table = None


class MillenniumCompletionClaimChecksTest(unittest.TestCase):
    def setUp(self):
        self.assertTrue(all([
            payment_terms, problem_registry, proof_logic, zero_table,
        ]), "millennium completion checker functions must exist")

    def test_five_printed_zeros_match_known_truncations(self):
        result = zero_table()
        self.assertEqual(len(result["absoluteErrors"]), 5)
        self.assertLess(result["maximumAbsoluteError"], 1e-15)
        self.assertAlmostEqual(
            result["maximumAbsoluteError"],
            9.926284795938969e-16,
            delta=1e-30,
        )
        self.assertTrue(result["allPrintedErrorsBelowOneEMinus15"])

    def test_zero_table_is_not_a_general_proof_or_parameter_derivation(self):
        result = zero_table()
        self.assertFalse(result["parametersGenerateValues"])
        self.assertFalse(result["finiteCheckProvesAllZeros"])
        self.assertFalse(result["conjugatePairsProveCriticalLine"])

    def test_dirac_symmetry_steps_do_not_prove_riemann_hypothesis(self):
        result = proof_logic()
        self.assertFalse(result["spectralIdentityDemonstrated"])
        self.assertFalse(result["chiralityProvesCriticalLine"])
        self.assertFalse(result["hermiticityProvesCriticalLine"])
        self.assertFalse(result["conjugateSymmetryProvesCriticalLine"])

    def test_closed_odd_dimensional_manifold_cannot_have_euler_two(self):
        result = proof_logic()
        self.assertEqual(result["closedOddDimensionalEulerCharacteristic"], 0)
        self.assertFalse(result["closedFiveManifoldCanHaveEulerTwo"])
        self.assertTrue(result["boundaryOrOtherSettingMustBeSpecified"])

    def test_checkmarks_and_prototypes_are_not_seven_general_proofs(self):
        result = problem_registry()
        self.assertEqual(result["completeProofDocumentsProvided"], 0)
        self.assertFalse(result["allSevenCompleted"])
        self.assertTrue(result["poincarePreviouslySolved"])
        self.assertFalse(result["satTspPrototypesProvePEqualsNp"])
        self.assertFalse(result["zConstantProvesNsRegularity"])
        self.assertFalse(result["knownEllipticCurvesProveBsd"])
        self.assertFalse(result["massNumberProvesYangMills"])

    def test_payment_demands_change_by_factor_five_and_do_not_verify_proof(self):
        result = payment_terms()
        self.assertEqual(result["firstDemandWanYuan"], 1000)
        self.assertEqual(result["laterDemandWanYuan"], 5000)
        self.assertEqual(result["laterOverFirst"], 5)
        self.assertFalse(result["paymentSubstitutesForPublicProof"])

    def test_external_acceptance_evidence_is_not_provided(self):
        result = problem_registry()
        self.assertFalse(result["independentPeerReviewProvided"])
        self.assertFalse(result["prizeRecognitionProvided"])
        self.assertFalse(result["publicProofAvailable"])


if __name__ == "__main__":
    unittest.main()
