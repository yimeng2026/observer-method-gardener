from pathlib import Path
import sys
import unittest

import mpmath as mp

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from checks.classical_coulomb_gibbs import (
    coulomb_small_radius_lower_bound,
    maxwell_velocity_pdf,
    total_momentum,
)


class ClassicalCoulombGibbsTest(unittest.TestCase):
    def test_maxwell_baseline_normalizes_and_has_equipartition(self):
        mass, thermal_energy = 2.0, 3.0
        density = lambda v: maxwell_velocity_pdf(v, mass, thermal_energy)
        normalization = mp.quad(density, [-mp.inf, 0, mp.inf])
        second_moment = mp.quad(lambda v: v**2 * density(v), [-mp.inf, 0, mp.inf])
        self.assertAlmostEqual(float(normalization), 1.0, places=12)
        self.assertAlmostEqual(float(second_moment), thermal_energy / mass, places=12)

    def test_classical_coulomb_small_radius_lower_bound_diverges(self):
        broad = coulomb_small_radius_lower_bound(a=1.0, cutoff=0.1, upper=1.0)
        narrow = coulomb_small_radius_lower_bound(a=1.0, cutoff=0.01, upper=1.0)
        self.assertAlmostEqual(broad, 9 / 24)
        self.assertAlmostEqual(narrow, 99 / 24)
        self.assertGreater(narrow, broad)

    def test_opposite_velocities_do_not_imply_zero_total_momentum(self):
        self.assertEqual(total_momentum(1.0, 1.0, 2.0, -1.0), -1.0)
        self.assertEqual(total_momentum(1.0, 1.0, 1.0, -1.0), 0.0)


if __name__ == "__main__":
    unittest.main()
