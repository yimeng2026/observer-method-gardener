from pathlib import Path
import math
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from checks.classical_ether_arm_times import ether_arm_round_trips


class ClassicalEtherArmTimesTest(unittest.TestCase):
    def test_zero_motion_removes_arm_difference(self):
        result = ether_arm_round_trips(length=1.0, speed_ratio=0.0, c=1.0)
        self.assertEqual(result["longitudinal"], 2.0)
        self.assertEqual(result["transverse"], 2.0)
        self.assertEqual(result["timeDifference"], 0.0)

    def test_moving_simple_ether_model_has_nonzero_arm_difference(self):
        result = ether_arm_round_trips(length=1.0, speed_ratio=0.5, c=1.0)
        self.assertAlmostEqual(result["longitudinal"], 8 / 3)
        self.assertAlmostEqual(result["transverse"], 4 / math.sqrt(3))
        self.assertGreater(result["timeDifference"], 0)
        self.assertAlmostEqual(result["timeDifference"], 8 / 3 - 4 / math.sqrt(3))


if __name__ == "__main__":
    unittest.main()
