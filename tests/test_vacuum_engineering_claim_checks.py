from pathlib import Path
import math
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
try:
    from checks.vacuum_engineering_claim_checks import (
        document_evidence,
        fusion_economics,
        performance_table,
        vacuum_density,
    )
except ModuleNotFoundError:
    document_evidence = fusion_economics = None
    performance_table = vacuum_density = None


class VacuumEngineeringClaimChecksTest(unittest.TestCase):
    def setUp(self):
        self.assertTrue(all([
            vacuum_density, fusion_economics,
            performance_table, document_evidence,
        ]), "vacuum engineering checker functions must exist")

    def assertClose(self, actual, expected, tolerance=1e-9):
        self.assertTrue(
            math.isclose(actual, expected, rel_tol=tolerance, abs_tol=0.0),
            (actual, expected),
        )

    def test_vacuum_energy_prefactor_is_about_ten_thousand_times_larger(self):
        result = vacuum_density()
        self.assertClose(result["computedScale"], 2.4532731795590316e23)
        self.assertGreater(result["computedScaleOverDisplayed"], 9990)
        self.assertLess(result["computedScaleOverDisplayed"], 10000)
        self.assertFalse(result["displayedScaleSupported"])

    def test_density_and_zero_error_claims_fail(self):
        result = vacuum_density()
        self.assertClose(result["computedDensity"], 5.242070578423779e-6)
        self.assertGreater(result["computedOverClaimedDensity"], 9800)
        self.assertLess(result["computedOverClaimedDensity"], 9820)
        self.assertClose(result["printedPairRelativeDifference"], 0.01 / 5.33)
        self.assertFalse(result["zeroErrorSupported"])

    def test_calibration_and_friedmann_evidence_are_not_closed(self):
        result = vacuum_density()
        self.assertFalse(result["calibrationFactorIndependentlyDerived"])
        self.assertFalse(result["independentDatasetProvided"])
        self.assertFalse(result["friedmannExtraTermClosedIfSameGamma"])

    def test_fusion_power_efficiency_is_forty_not_forty_five_percent(self):
        result = fusion_economics()
        self.assertClose(result["grossElectricMwAt45Percent"], 2250)
        self.assertClose(result["printedEfficiency"], 0.4)
        self.assertFalse(result["efficiencyConsistent"])

    def test_six_year_simple_payback_is_not_supported(self):
        result = fusion_economics()
        self.assertClose(result["annualRevenueUsd"], 350400000)
        self.assertClose(result["paybackAtFullCapacity"], 16e9 / 350400000)
        self.assertClose(result["paybackAt85Percent"], 16e9 / (350400000 * 0.85))
        self.assertFalse(result["sixYearPaybackSupported"])

    def test_market_share_arithmetic_does_not_support_annual_value(self):
        result = fusion_economics()
        self.assertClose(result["fusionShareKwh"], 15e12)
        self.assertClose(result["annualRevenueAtShownPriceUsd"], 3e11)
        self.assertClose(result["claimedAnnualValueUsd"], 1.5e12)
        self.assertFalse(result["shownPriceSupportsClaimedValue"])

    def test_performance_table_simple_ratios_are_retained(self):
        result = performance_table()
        self.assertClose(result["powerDensityRatio"], 1e6)
        self.assertClose(result["fuelUtilizationRatio"], 950)
        self.assertClose(result["availabilityRatio"], 98 / 30)
        self.assertClose(result["gainRatio"], 150)

    def test_effective_confinement_and_q1500_are_not_measurements(self):
        result = performance_table()
        self.assertClose(result["printedEffectiveGain"], 1e19)
        self.assertFalse(result["effectiveConfinementGainDerived"])
        self.assertFalse(result["q1500Measured"])
        self.assertFalse(result["hundredYearLeadDerived"])

    def test_simulated_memo_and_engineering_claims_have_no_official_evidence(self):
        result = document_evidence()
        self.assertTrue(result["simulationLabelPresent"])
        self.assertTrue(result["memoDateAfterPost"])
        self.assertFalse(result["officialAuthenticationProvided"])
        self.assertFalse(result["classificationMarkingsAuthenticateDocument"])
        self.assertFalse(result["listedAttachmentsIncluded"])
        self.assertFalse(result["engineeringPerformanceValidated"])


if __name__ == "__main__":
    unittest.main()
