from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from checks.quaternion_cubic import cubic_residual, quadratic_root_from_unit_pure, quaternion_norm


class QuaternionCubicTest(unittest.TestCase):
    def test_pure_unit_i_is_a_counterexample_to_the_ai_claim(self):
        self.assertEqual(cubic_residual((0.0, 1.0, 0.0, 0.0)), (1.0, -1.0, 0.0, 0.0))

    def test_minus_one_and_complete_quadratic_family_satisfy_cubic(self):
        self.assertAlmostEqual(quaternion_norm(cubic_residual((-1.0, 0.0, 0.0, 0.0))), 0.0)
        for unit in [(1, 0, 0), (0, 1, 0), (0, 0, 1), (1 / 14**0.5, 2 / 14**0.5, 3 / 14**0.5)]:
            root = quadratic_root_from_unit_pure(unit)
            self.assertLess(quaternion_norm(cubic_residual(root)), 1e-12)

    def test_non_unit_direction_is_rejected(self):
        with self.assertRaises(ValueError):
            quadratic_root_from_unit_pure((1.0, 1.0, 1.0))


if __name__ == "__main__":
    unittest.main()
