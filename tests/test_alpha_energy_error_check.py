from pathlib import Path
import sys
import unittest

import mpmath as mp

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from checks.alpha_energy_error_check import (
    ALPHA_CODATA_2022,
    kinetic_relative_correction,
    reciprocal_137_errors,
)


class AlphaEnergyErrorCheckTest(unittest.TestCase):
    def test_relativistic_kinetic_correction_is_not_one_over_40000(self):
        correction = kinetic_relative_correction(ALPHA_CODATA_2022)
        self.assertGreater(correction, mp.mpf("0.00003993"))
        self.assertLess(correction, mp.mpf("0.00003995"))
        with mp.workdps(60):
            reciprocal = 1 / correction
        self.assertAlmostEqual(reciprocal, 25037.3756472241164088, delta=1e-6)
        self.assertNotAlmostEqual(correction, 1 / 40000, delta=1e-8)

    def test_one_over_137_has_distinct_speed_and_energy_errors(self):
        errors = reciprocal_137_errors()
        self.assertAlmostEqual(errors["speedRelativeError"], 0.00026276771963593137, delta=1e-15)
        self.assertAlmostEqual(errors["energyRelativeError"], 0.0005256044861463638, delta=1e-15)
        self.assertNotAlmostEqual(errors["energyRelativeError"], 1 / 40000, delta=1e-8)

    def test_small_beta_limit_has_three_quarters_beta_squared_leading_term(self):
        beta = mp.mpf("0.0001")
        ratio = kinetic_relative_correction(beta) / (mp.mpf(3) / 4 * beta**2)
        self.assertAlmostEqual(ratio, 1.0, delta=1e-7)


if __name__ == "__main__":
    unittest.main()
