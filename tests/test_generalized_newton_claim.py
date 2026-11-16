from pathlib import Path
import math
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from checks.generalized_newton_claim import (
    polar_acceleration,
    relativistic_parallel_perpendicular_force,
    schwarzschild_radial_coefficients,
    displayed_radial_coefficients,
    transverse_cross_product,
    proper_time_factor,
)


class GeneralizedNewtonClaimTest(unittest.TestCase):
    def test_polar_acceleration_and_relativistic_split(self):
        radial, angular = polar_acceleration(r=2.0, r_dot=0.3, r_ddot=0.4, theta_dot=0.2, theta_ddot=0.5)
        self.assertAlmostEqual(radial, 0.4 - 2.0 * 0.2**2)
        self.assertAlmostEqual(angular, 2.0 * 0.5 + 2 * 0.3 * 0.2)
        parallel, perpendicular = relativistic_parallel_perpendicular_force(
            rest_mass=2.0, speed_ratio=0.6, parallel_acceleration=0.2, perpendicular_acceleration=0.3
        )
        self.assertAlmostEqual(parallel, 2.0 * 1.25**3 * 0.2)
        self.assertAlmostEqual(perpendicular, 2.0 * 1.25 * 0.3)

    def test_cross_product_leaves_the_orbital_plane(self):
        force = transverse_cross_product(rest_mass=1.0, speed=3.0, radius=2.0)
        self.assertEqual(force[:2], (0.0, 0.0))
        self.assertNotEqual(force[2], 0.0)

    def test_schwarzschild_radial_inverse_factors(self):
        actual = schwarzschild_radial_coefficients(r=4.0)
        displayed = displayed_radial_coefficients(r=4.0)
        self.assertAlmostEqual(actual["time"], -1 / 32)
        self.assertAlmostEqual(actual["radius"], 1 / 8)
        self.assertAlmostEqual(displayed["time"], -1 / 8)
        self.assertAlmostEqual(displayed["radius"], 1 / 4)
        self.assertNotEqual(actual, displayed)

    def test_weak_field_proper_time_is_not_general_radial_formula(self):
        # Units with c=1; motion is radial and A>0.
        exact = proper_time_factor(a=0.1, radial_speed=0.04, inverse_metric_denominator=True)
        displayed = proper_time_factor(a=0.1, radial_speed=0.04, inverse_metric_denominator=False)
        self.assertAlmostEqual(exact, math.sqrt(0.1 - 0.04**2 / 0.1))
        self.assertAlmostEqual(displayed, math.sqrt(0.1 - 0.04**2))
        self.assertGreater(displayed, exact)


if __name__ == "__main__":
    unittest.main()
