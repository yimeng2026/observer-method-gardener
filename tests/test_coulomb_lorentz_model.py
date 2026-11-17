from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from checks.coulomb_lorentz_model import (
    C,
    E_CHARGE,
    M_E,
    M_P,
    R_BOHR,
    coulomb_circular_orbit,
    magnetic_coulomb_ratio,
)


class CoulombLorentzModelTest(unittest.TestCase):
    def test_scalar_magnetic_coulomb_ratio_uses_speed_product_over_c_squared(self):
        ratio = magnetic_coulomb_ratio(3e7, 2e7)
        self.assertAlmostEqual(ratio, 6e14 / C**2, delta=1e-15)
        self.assertGreater(ratio, 0.0066)
        self.assertLess(ratio, 0.0067)

    def test_circular_baseline_recovers_reduced_two_body_constants(self):
        result = coulomb_circular_orbit()
        self.assertAlmostEqual(result["reducedMass"], 9.10442528891677e-31, delta=1e-42)
        self.assertAlmostEqual(result["relativeSpeed"], 2188286.9080156004, delta=0.01)
        self.assertAlmostEqual(result["energy"], -2.179872361100598e-18, delta=1e-25)
        self.assertAlmostEqual(result["angularMomentum"], 1.0542847660092601e-34, delta=1e-41)
        centripetal = result["reducedMass"] * result["relativeSpeed"]**2 / R_BOHR
        self.assertAlmostEqual(centripetal, result["coulombForce"], delta=1e-20)

    def test_center_of_mass_velocities_and_post_scalar_magnetic_scale(self):
        result = coulomb_circular_orbit()
        self.assertAlmostEqual(M_P * result["protonSpeed"], M_E * result["electronSpeed"], delta=1e-22)
        self.assertAlmostEqual(result["relativeSpeed"], result["electronSpeed"] + result["protonSpeed"], delta=1e-9)
        self.assertAlmostEqual(result["postScalarMagneticRatio"], 2.8985807885545365e-8, delta=1e-15)
        self.assertAlmostEqual(result["relativeSpeed"] / C, 0.007299339425061856, delta=1e-12)

    def test_invalid_physical_inputs_are_rejected(self):
        with self.assertRaises(ValueError):
            magnetic_coulomb_ratio(1, 1, c=0)
        with self.assertRaises(ValueError):
            coulomb_circular_orbit(r=0)
        with self.assertRaises(ValueError):
            coulomb_circular_orbit(e=0)


if __name__ == "__main__":
    unittest.main()
