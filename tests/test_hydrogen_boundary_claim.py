from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from checks.hydrogen_boundary_claim import boundary_check, lyman_limit


class HydrogenBoundaryClaimTest(unittest.TestCase):
    def test_displayed_micron_boundary_is_not_direct_epsilon_product(self):
        result = boundary_check(0.0014253345, 1.98607647e-6)
        self.assertAlmostEqual(result["directMeters"], 5.2842295636768613e-11, delta=1e-22)
        self.assertAlmostEqual(result["displayedOverDirect"], 37584.97707313935, delta=1e-8)
        self.assertAlmostEqual(result["displayedOverA0"], 37531.40590863529, delta=1e-7)
        self.assertNotAlmostEqual(result["displayedOverA0"], 3748.0)

    def test_lyman_limit_two_mass_conventions(self):
        infinite = lyman_limit(reduced_mass=False)
        reduced = lyman_limit(reduced_mass=True)
        self.assertAlmostEqual(infinite["lambdaNm"], 91.12670505823876, delta=1e-10)
        self.assertAlmostEqual(reduced["lambdaNm"], 91.17633421299283, delta=1e-10)
        self.assertAlmostEqual(reduced["rydbergPerMeter"], 10967758.340272225, delta=1e-6)
        self.assertNotAlmostEqual(reduced["lambdaNm"], 91.02)

    def test_invalid_inputs_are_rejected(self):
        with self.assertRaises(ValueError):
            boundary_check(1.0, 1e-6)
        with self.assertRaises(ValueError):
            lyman_limit(reduced_mass=True, electron_mass=0)


if __name__ == "__main__":
    unittest.main()
