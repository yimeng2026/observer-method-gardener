from pathlib import Path
import math
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
try:
    from checks.local_universe_claim_checks import (
        casimir,
        dark_energy,
        dark_matter_mass,
        electroweak,
        energy_balance,
        error_table,
        evidence_boundaries,
        gravitational_wave,
        superconductor,
        top_quark,
    )
except ModuleNotFoundError:
    casimir = dark_energy = dark_matter_mass = electroweak = None
    energy_balance = error_table = evidence_boundaries = None
    gravitational_wave = superconductor = top_quark = None


class LocalUniverseClaimChecksTest(unittest.TestCase):
    def setUp(self):
        self.assertTrue(all([
            casimir, dark_energy, dark_matter_mass, electroweak,
            energy_balance, error_table, evidence_boundaries,
            gravitational_wave, superconductor, top_quark,
        ]), "local universe checker functions must exist")

    def assertClose(self, actual, expected, tolerance=1e-9):
        self.assertTrue(
            math.isclose(actual, expected, rel_tol=tolerance, abs_tol=0.0),
            (actual, expected),
        )

    def test_dark_matter_formula_is_not_500_proton_masses(self):
        result = dark_matter_mass()
        self.assertClose(result["massKg"], 1.1586057677574474e-29)
        self.assertClose(result["claimedOverComputed"], 72069.3805638646)
        self.assertClose(result["computedOverClaimed"], 1.3875518176735897e-5)
        self.assertClose(result["massOverProton"], 0.006926883782567117)
        self.assertFalse(result["claimedMassSupported"])
        self.assertFalse(result["ratio500Supported"])

    def test_superconductor_gap_is_not_room_temperature(self):
        result = superconductor()
        self.assertClose(result["gapEv"], 5561.088122440721)
        self.assertClose(result["gapMev"], 5561088.122440721)
        self.assertClose(result["tcDirectK"], 64533747.89240027)
        self.assertClose(result["tcBcsK"], 36666902.21159106)
        self.assertFalse(result["roomTemperatureSupported"])

    def test_dark_energy_w_is_outside_printed_interval_and_mass_bound_passes(self):
        result = dark_energy()
        self.assertTrue(math.isclose(
            result["wOutsideBy"], 3.1e-11, rel_tol=0.0, abs_tol=2e-17,
        ), "Allow for the printed decimal truncation at 12 decimal places")
        self.assertFalse(result["wWithinPrintedInterval"])
        self.assertTrue(result["massBoundSatisfied"])
        self.assertClose(result["rhoRelativePercent"], 2 / 3)

    def test_top_quark_coefficient_does_not_support_173_gev(self):
        result = top_quark()
        self.assertClose(result["y33"], 0.35586172736695606)
        self.assertClose(result["computedMtGev"], 61.95185763225671)
        self.assertClose(result["mtUsingPrintedCoefficient"], 173.21924108048736)
        self.assertFalse(result["printedCoefficientSupported"])

    def test_electroweak_standard_arithmetic_is_broadly_retained(self):
        result = electroweak()
        self.assertClose(result["mwGev"], 80.2612)
        self.assertClose(result["mzGev"], 91.5050417536105)
        self.assertTrue(result["standardArithmeticBroadlyMatches"])

    def test_gravitational_wave_dispersion_is_not_one_e_minus_21(self):
        result = gravitational_wave()
        self.assertClose(result["relativeDispersionAt100Hz"], 2.4549316702836517e-39)
        self.assertFalse(result["printedDispersionSupported"])
        self.assertFalse(result["peakFrequencyDerived"])

    def test_uniform_sphere_energy_is_not_order_unity_balance(self):
        result = energy_balance()
        self.assertClose(result["gravitationalEnergyJ"], -9.080680272108844e68)
        self.assertClose(result["restEnergyJ"], 8.987551787368176e69)
        self.assertClose(result["absoluteGravityOverRest"], 0.10103619413766892)
        self.assertFalse(result["orderUnityBalanceSupported"])

    def test_printed_error_percentages_are_rounding_consistent(self):
        result = error_table()
        self.assertTrue(result["roundingConsistent"])
        rows = {row["name"]: row for row in result["rows"]}
        self.assertClose(rows["age"]["computedPercent"], 0.19583665772104156)
        self.assertClose(rows["top"]["computedPercent"], 0.2546885853206761)
        self.assertClose(rows["higgs"]["computedPercent"], 0.11976047904191617)
        self.assertClose(rows["electron"]["computedPercent"], 0.00019569509920763054)

    def test_casimir_sign_is_positive_but_energy_extraction_is_unvalidated(self):
        result = casimir()
        self.assertClose(result["coefficient"], 0.04775402502752557)
        self.assertGreater(result["coefficient"], 0)
        self.assertFalse(result["energyExtractionValidated"])

    def test_evidence_and_awards_are_not_provided(self):
        result = evidence_boundaries()
        self.assertFalse(result["rawDatasetsProvided"])
        self.assertFalse(result["onlyTwoParameters"])
        self.assertFalse(result["independentPeerReviewProvided"])
        self.assertFalse(result["awardsOrOfficialAppointmentsProvided"])
        self.assertFalse(result["bookCoverIsScientificEvidence"])


if __name__ == "__main__":
    unittest.main()
