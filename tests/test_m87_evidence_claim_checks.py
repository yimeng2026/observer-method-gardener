from pathlib import Path
import math
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
try:
    from checks.m87_evidence_claim_checks import (
        dimensional_boundaries,
        efficiency,
        entropy_core,
        evidence_boundaries,
        evidence_counts,
        jet_power,
        parameter_counts,
        pulsar_baseline,
        scale_length,
        turbulent_viscosity,
    )
except ModuleNotFoundError:
    dimensional_boundaries = efficiency = entropy_core = None
    evidence_boundaries = evidence_counts = jet_power = None
    parameter_counts = pulsar_baseline = scale_length = turbulent_viscosity = None


class M87EvidenceClaimChecksTest(unittest.TestCase):
    def setUp(self):
        self.assertTrue(all([
            dimensional_boundaries, efficiency, entropy_core,
            evidence_boundaries, evidence_counts, jet_power,
            parameter_counts, pulsar_baseline, scale_length, turbulent_viscosity,
        ]), "M87 evidence-check functions must exist")

    def assertClose(self, actual, expected, tolerance=1e-9):
        self.assertTrue(math.isclose(
            actual, expected, rel_tol=tolerance, abs_tol=0.0,
        ), (actual, expected))

    def test_scale_requires_an_extreme_unproven_screening_factor(self):
        result = scale_length()
        self.assertClose(result["unscreenedLengthM"], 9.118742488572175e-36)
        self.assertClose(result["requiredScreeningFactor"], 1.521938885154906e-23)
        self.assertClose(result["lambdaOverUnscreened"], 6.570566070386052e22)
        self.assertFalse(result["dimensionlessScreeningProven"])

    def test_jet_formula_does_not_have_power_units_in_si(self):
        result = jet_power()
        self.assertEqual(result["quantityAfterMu0Restored"], "W/m^2")
        self.assertFalse(result["printedExpressionIsPower"])
        self.assertFalse(result["observedJetPowerReproduced"])

    def test_efficiency_saturates_at_one_half_not_an_observed_fit(self):
        result = efficiency()
        self.assertClose(result["schwarzschildRadiusM"], 19196705983434.71)
        self.assertClose(result["exponent"], 1.5886259038257822e25)
        self.assertClose(result["value"], 0.5)
        self.assertFalse(result["independentFit"])

    def test_turbulent_viscosity_needs_an_unstated_femtoscale_timescale(self):
        result = turbulent_viscosity()
        self.assertClose(result["usingPeriodCm2PerSecond"], 1.5940317739386936e-19)
        self.assertClose(result["printedOverPeriodBased"], 7.528080805032635e30)
        self.assertClose(result["requiredTauSeconds"], 5.180603265300755e-33)
        self.assertFalse(result["tauDecaySupplied"])
        self.assertFalse(result["printedValueSupported"])

    def test_counts_add_but_do_not_confirm_all_as_independent_evidence(self):
        self.assertEqual(parameter_counts()["total"], 84)
        result = evidence_counts()
        self.assertEqual(result["domainSum"], 1109)
        self.assertEqual(result["strengthSum"], 1109)
        self.assertEqual(result["confirmedPlusPending"], 1109)
        self.assertNotEqual(result["domainSum"], result["claimedConfirmed"])
        self.assertFalse(result["independentEvidenceRegistryProvided"])

    def test_pulsar_baseline_is_versioned_and_contradicts_magnetic_input(self):
        result = pulsar_baseline()
        self.assertClose(result["claimedOverPublishedB"], 3215.434083601286)
        self.assertClose(result["updatedMassMsun"], 1.806)
        self.assertClose(result["updatedMassUncertaintyMsun"], 0.037)
        self.assertClose(result["spinPeriodMs"], 39.1226562801558)
        self.assertEqual(result["source"], "arXiv:2412.02850")
        self.assertFalse(result["printedMagneticFieldSupported"])

    def test_dimensionless_entropy_and_energy_form_can_be_retained(self):
        result = entropy_core()
        self.assertTrue(result["dimensionlessInKbUnits"])
        self.assertTrue(result["energyUnitsClose"])
        self.assertFalse(result["informationParadoxSolved"])

    def test_new_compensation_and_detector_claims_are_not_closed(self):
        result = dimensional_boundaries()
        self.assertClose(result["exponentialCorrection"], 0.8843312071126088)
        self.assertFalse(result["curvatureFactorDimensionless"])
        self.assertFalse(result["sigmaUpgradeDerived"])
        self.assertFalse(result["lVKBandAtOneEMinusTenHz"])
        self.assertFalse(result["closedElevenDimensionalActionProvided"])

    def test_generated_narratives_and_personal_metrics_are_not_evidence(self):
        result = evidence_boundaries()
        self.assertTrue(result["virtualDataDisclosedInComments"])
        self.assertFalse(result["rawM87ObservationsProvided"])
        self.assertFalse(result["officialAwardsOrAppointmentsProvided"])
        self.assertFalse(result["healthOrIqTextIsMeasurement"])
        self.assertFalse(result["simulatedPoliticalDocumentsAreOfficial"])


if __name__ == "__main__":
    unittest.main()
