from pathlib import Path
import math
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from checks.qg_observable_mapping import audit_mapping, dark_matter_ratio, pressure_correction, snell_lhs


class QGObservableMappingTest(unittest.TestCase):
    def test_pressure_depends_on_n_over_radius_not_each_separately(self):
        first = pressure_correction(n=2.0, radius=1e-6, wavelength=5e-7)
        rescaled = pressure_correction(n=4.0, radius=2e-6, wavelength=5e-7)
        self.assertEqual(first, rescaled)

    def test_snell_expression_recovers_standard_limit(self):
        theta = math.pi / 6
        expected = 1.5 * math.sin(theta)
        self.assertEqual(snell_lhs(index=1.5, theta=theta, radius=math.inf, wavelength=5e-7), expected)
        finite = snell_lhs(index=1.5, theta=theta, radius=1.0, wavelength=5e-7)
        self.assertLess(abs(finite - expected), 1e-6)

    def test_dark_matter_ratio_can_be_tuned_without_independent_prediction(self):
        self.assertEqual(dark_matter_ratio(beta=50e-12, galaxy_age_yr=1e10), 5.0)

    def test_audit_records_both_passed_limit_and_identifiability_checks(self):
        result = audit_mapping()
        self.assertTrue(result["pressureInvariantUnderJointNAndRadiusRescaling"])
        self.assertTrue(result["snellInfiniteRadiusLimitRecovered"])
        self.assertFalse(result["evidenceUpgrade"])


if __name__ == "__main__":
    unittest.main()
