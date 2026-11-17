from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from checks.electron_radius_claim import (
    CODATA_2022,
    POST_INPUTS,
    classical_electron_radius,
    shell_outside_field_energy,
    surface_speed_for_uniform_sphere_spin,
    uniform_solid_self_energy,
)


class ElectronRadiusClaimTest(unittest.TestCase):
    def test_post_constants_recover_metres_but_not_the_displayed_femtometres(self):
        radius = classical_electron_radius(**POST_INPUTS)
        radius_fm = radius * 1e15
        self.assertGreater(radius_fm, 2.81)
        self.assertLess(radius_fm, 2.82)
        self.assertAlmostEqual(radius_fm, 0.2818 * 10, delta=0.005)

    def test_codata_inputs_recover_the_independent_reference_value(self):
        radius = classical_electron_radius(**CODATA_2022)
        self.assertAlmostEqual(radius, 2.8179403205e-15, delta=1.5e-24)

    def test_shell_and_uniform_solid_energies_have_distinct_numeric_factors(self):
        k = 3.0
        charge = 5.0
        radius = 2.0
        shell = shell_outside_field_energy(radius=radius, coulomb_k=k, charge=charge)
        solid = uniform_solid_self_energy(radius=radius, coulomb_k=k, charge=charge)
        self.assertAlmostEqual(shell, 0.5 * k * charge**2 / radius, delta=1e-14)
        self.assertAlmostEqual(solid, 0.6 * k * charge**2 / radius, delta=1e-14)
        self.assertNotAlmostEqual(shell, k * charge**2 / radius, delta=1e-14)

    def test_uniform_sphere_mechanical_spin_is_not_a_viable_electron_model(self):
        radius = classical_electron_radius(**CODATA_2022)
        mass = CODATA_2022["m_e"]
        light_speed = CODATA_2022["c"]
        surface_speed = surface_speed_for_uniform_sphere_spin(radius=radius, m_e=mass)
        independently_expected_speed = 5 * 1.054571817e-34 / (4 * mass * radius)
        self.assertAlmostEqual(surface_speed / independently_expected_speed, 1.0, delta=1e-9)
        self.assertGreater(surface_speed / light_speed, 170.0)
        self.assertLess(surface_speed / light_speed, 175.0)


if __name__ == "__main__":
    unittest.main()
