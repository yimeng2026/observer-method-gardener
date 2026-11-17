from pathlib import Path
import math
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
try:
    from checks.black_hole_observation_plan_checks import (
        lense_thirring_baseline,
        observation_evidence,
        pa_amplitude,
        period_and_scaling,
    )
except ModuleNotFoundError:
    lense_thirring_baseline = observation_evidence = None
    pa_amplitude = period_and_scaling = None


class BlackHoleObservationPlanChecksTest(unittest.TestCase):
    def setUp(self):
        self.assertTrue(all([
            lense_thirring_baseline, observation_evidence,
            pa_amplitude, period_and_scaling,
        ]), "black-hole observation-plan checker functions must exist")

    def assertClose(self, actual, expected, tolerance=1e-9):
        self.assertTrue(
            math.isclose(actual, expected, rel_tol=tolerance, abs_tol=0.0),
            (actual, expected),
        )

    def test_period_formula_matches_m87_but_not_sgr_a(self):
        result = period_and_scaling()
        self.assertClose(result["m87Period"], 2.8669090909090906, 1e-8)
        self.assertGreater(result["sgrPeriod"], 900)
        self.assertLess(result["sgrPeriod"], 910)
        self.assertGreater(result["sgrClaimedOverComputed"], 5.5)
        self.assertGreater(result["sgrPeriodIfFactorOne"], 5000)
        self.assertLess(result["sgrPeriodIfFactorOne"], 5050)
        self.assertGreater(result["m87PeriodWithSixPointFive"], 2.4)
        self.assertLess(result["m87PeriodWithSixPointFive"], 2.45)

    def test_cadence_phase_and_hubble_boundaries(self):
        result = period_and_scaling()
        self.assertClose(result["cadenceAtTwoYears"], 3.0)
        self.assertGreater(result["cadenceAt292Years"], 2.0)
        self.assertLess(result["cadenceAt292Years"], 2.1)
        self.assertClose(result["phaseThresholdDegrees"], 18.0)
        self.assertLess(result["grsPeriodOverHubbleTime"], 1.0)
        self.assertFalse(result["grsExceedsHubbleTime"])

    def test_pa_amplitude_is_not_the_displayed_four_micro_radians(self):
        result = pa_amplitude()
        self.assertClose(result["deltaPaRadians"], 2e-5 / math.sin(math.radians(17)))
        self.assertGreater(1 / result["printedOverComputedRatio"], 17)
        self.assertLess(result["deltaPaDegrees"], 0.004)
        self.assertFalse(result["degreeScaleDerived"])

    def test_lense_thirring_formula_needs_spin_and_proper_dimensions(self):
        result = lense_thirring_baseline()
        self.assertFalse(result["printedFormulaHasAngularDimensions"])
        self.assertGreater(result["properPerOrbitRadians"], 1.6e-5)
        self.assertLess(result["properPerOrbitRadians"], 1.8e-5)
        self.assertLess(result["properPerOrbitDegrees"], 0.004)
        self.assertFalse(result["modulationPercentageDerived"])

    def test_eht_rate_is_only_an_upper_angular_speed(self):
        result = observation_evidence()
        self.assertClose(result["fullTurnRateDegrees"], 0.072)
        self.assertGreater(result["yearsToTenDegreeAccuracy"], 138)
        self.assertGreater(result["yearsToFiveDegreeAccuracy"], 69)
        self.assertFalse(result["multiEpochMeasurementPerformed"])
        self.assertFalse(result["absenceOfEvidenceSupportsTheoryUnconditionally"])


if __name__ == "__main__":
    unittest.main()
