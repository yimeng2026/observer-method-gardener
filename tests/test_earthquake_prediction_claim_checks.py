from pathlib import Path
import math
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
try:
    from checks.earthquake_prediction_claim_checks import (
        cosmic_periods,
        curvature_and_gradient,
        evidence_boundaries,
        rupture_and_magnitude,
    )
except ModuleNotFoundError:
    cosmic_periods = curvature_and_gradient = None
    evidence_boundaries = rupture_and_magnitude = None


class EarthquakePredictionClaimChecksTest(unittest.TestCase):
    def setUp(self):
        self.assertTrue(all([
            cosmic_periods, curvature_and_gradient,
            evidence_boundaries, rupture_and_magnitude,
        ]), "earthquake prediction checker functions must exist")

    def assertClose(self, actual, expected, tolerance=1e-9):
        self.assertTrue(
            math.isclose(actual, expected, rel_tol=tolerance, abs_tol=0.0),
            (actual, expected),
        )

    def test_super_period_is_not_seven_thousand_years(self):
        result = cosmic_periods()
        self.assertGreater(result["superPeriodYears"], 8e10)
        self.assertLess(result["claimedPeriodOverComputed"], 1e-6)
        self.assertGreater(result["computedOverClaimedPeriod"], 1e6)
        self.assertFalse(result["sevenThousandSupported"])

    def test_lcm_scaling_does_not_produce_2145_event(self):
        result = cosmic_periods()
        self.assertEqual(result["lcmYears"], 8228220)
        self.assertLess(abs(result["eventTimeYears"]), 1e-11)
        self.assertNotEqual(round(result["eventTimeYears"], 1), 2145.7)
        self.assertFalse(result["eventDateEstablished"])

    def test_curvature_and_chi_values(self):
        result = curvature_and_gradient()
        self.assertClose(result["deltaR"], 2.4e-6)
        self.assertGreater(result["chiQ"], 4.9e-42)
        self.assertLess(result["chiQ"], 5.2e-42)
        self.assertFalse(result["deltaRMatchesClaim"])

    def test_poisson_and_vertical_gradient_dimensions_are_not_closed(self):
        result = curvature_and_gradient()
        self.assertFalse(result["poissonDimensionsClosed"])
        self.assertFalse(result["verticalGradientDimensionsClosed"])
        self.assertFalse(result["precursorGradientDerived"])

    def test_rupture_geometry_magnitude_depth_and_duration(self):
        result = rupture_and_magnitude()
        self.assertClose(result["sqrtMomentOverModulus"], math.sqrt(1.2e23 / 7.5e10))
        self.assertFalse(result["sqrtHasLengthUnits"])
        self.assertClose(result["momentMagnitude"], (2 / 3) * (math.log10(1.2e23) - 9.1))
        self.assertFalse(result["depthWithinTransitionZone"])
        self.assertClose(result["ruptureDurationSeconds"], 350 / 4.8)

    def test_prediction_and_benchmark_evidence_is_missing(self):
        result = evidence_boundaries()
        self.assertFalse(result["paleoDatasetProvided"])
        self.assertFalse(result["machineLearningBenchmarkProvided"])
        self.assertFalse(result["prospectiveProtocolProvided"])
        self.assertFalse(result["operationalForecastValidated"])


if __name__ == "__main__":
    unittest.main()
