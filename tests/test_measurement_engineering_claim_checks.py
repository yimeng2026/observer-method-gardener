from pathlib import Path
import math
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
try:
    from checks.measurement_engineering_claim_checks import (
        characteristic_constants,
        ct_business_arithmetic,
        ct_dose_and_performance,
        dichroism_and_dose_cancellation,
        engineering_dimensions,
        mtf_and_availability,
        radar_examples,
        standard_quantum_baseline,
    )
except ModuleNotFoundError:
    characteristic_constants = ct_business_arithmetic = None
    ct_dose_and_performance = dichroism_and_dose_cancellation = None
    engineering_dimensions = mtf_and_availability = None
    radar_examples = standard_quantum_baseline = None


class MeasurementEngineeringClaimChecksTest(unittest.TestCase):
    def setUp(self):
        self.assertTrue(all([
            characteristic_constants, ct_business_arithmetic,
            ct_dose_and_performance, dichroism_and_dose_cancellation,
            engineering_dimensions, mtf_and_availability,
            radar_examples, standard_quantum_baseline,
        ]), "measurement-engineering checker functions must exist")

    def assertClose(self, actual, expected, tolerance=1e-9):
        self.assertTrue(
            math.isclose(actual, expected, rel_tol=tolerance, abs_tol=0.0),
            (actual, expected),
        )

    def test_standard_quantum_formulas_are_kept_separate(self):
        result = standard_quantum_baseline()
        self.assertClose(result["positionMomentumBound"], 1.054571817e-34 / 2)
        self.assertClose(result["squeezedProduct"], 0.25)
        self.assertClose(result["chshMaximum"], 2 * math.sqrt(2))
        self.assertClose(result["allanExample"], 14 / 6)

    def test_frequency_and_energy_versions_resolve_the_constant_table(self):
        result = characteristic_constants()
        self.assertClose(result["periodSeconds"], 1.998549276379728e-21)
        self.assertClose(result["ordinaryFrequencyHz"], 5.003629441709088e20)
        self.assertClose(result["angularFrequencyRadPerSecond"], 3.1438730990717737e21)
        self.assertClose(result["photonEnergyJ"], 3.3154399685369753e-13)
        self.assertClose(result["displayedEnergyRatio"], 995343.0106762607)
        self.assertNotEqual(result["photonEnergyJ"], 3.30e-7)

    def test_spacetime_afm_and_ligo_dimensions_are_not_closed(self):
        result = engineering_dimensions()
        self.assertEqual(result["spacetimeLeft"], {"L": 1, "T": 1})
        self.assertEqual(result["spacetimeRight"], {"L": 0, "T": 1})
        self.assertEqual(result["afmDisplacement"], {"L": 1, "T": 0.25})
        self.assertEqual(result["ligoStrain"], {"L": 0.5, "T": -0.5})
        self.assertNotEqual(result["spacetimeLeft"], result["spacetimeRight"])
        self.assertNotEqual(result["afmDisplacement"], {"L": 1, "T": 0})
        self.assertNotEqual(result["ligoStrain"], {"L": 0, "T": 0})

    def test_business_arithmetic_is_nominal_not_currency_aware(self):
        result = ct_business_arithmetic()
        self.assertEqual(result["traditionalTotal"], 400000)
        self.assertEqual(result["quantumTotal"], 650000)
        self.assertClose(result["electricitySaving"], 2.3 / 3.5)
        self.assertEqual(result["annualSaving"], 164250)
        self.assertClose(result["nominalPaybackYears"], 600000 / 464250)
        self.assertFalse(result["currencyAwarePayback"])

    def test_dose_and_performance_arithmetic_exposes_version_conflicts(self):
        result = ct_dose_and_performance()
        self.assertClose(result["snrGain"], math.exp(1.5))
        self.assertClose(result["doseFactor95"], math.exp(-3))
        self.assertClose(result["performanceFactor"], math.exp(4.5) * 20 * 0.615)
        self.assertClose(result["heartDoseFromFactor"], 15 * math.exp(-3))
        self.assertClose(result["heartDoseDisplayedReduction"], 0.8)
        self.assertClose(result["breastPCTVReduction"], 0.6)
        self.assertClose(result["lungPCTVReduction"], 0.6)

    def test_dichroism_factor_and_dose_resolution_cancellation(self):
        result = dichroism_and_dose_cancellation()
        self.assertEqual(result["logRatioOpticalDepthFactor"], 2)
        self.assertNotEqual(result["logRatioOpticalDepthFactor"], 1)
        self.assertClose(result["doseFactorUsingOwnResolution"], 1.0)
        self.assertNotEqual(result["doseFactorUsingOwnResolution"], math.exp(-3))

    def test_radar_example_and_angle_versions(self):
        result = radar_examples()
        self.assertClose(result["kaVelocityWithoutAngle"], 1.5926842658293194e-6)
        self.assertClose(result["kaVelocityWithAngle"], 1.8390733792212778e-6)
        self.assertClose(result["opticalRequiredFrequencyResolution"], 0.6671281903963041)
        self.assertNotEqual(result["kaVelocityWithoutAngle"], result["kaVelocityWithAngle"])

    def test_mtf_and_availability_are_design_arithmetic_not_measurements(self):
        result = mtf_and_availability()
        self.assertClose(result["mtfFrequencyLpPerMm"], 33.302184446307905)
        self.assertClose(result["linePairPitchMm"], 0.03002806021966125)
        self.assertClose(result["singleLineWidthMm"], 0.015014030109830625)
        self.assertClose(result["availabilityBound"], 10000 / 10002)
        self.assertFalse(result["measuredAvailability"])


if __name__ == "__main__":
    unittest.main()
