from pathlib import Path
import math
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from checks.magnetic_temperature_claim import delta_b_micro_tesla


class MagneticTemperatureClaimTest(unittest.TestCase):
    def test_all_six_displayed_examples_are_recomputed(self):
        expected = {
            (1, 0.5): 3.0723452187747027,
            (1, 2): 6.144690437549405,
            (3, 0.5): 9.217035656324109,
            (3, 2): 18.434071312648218,
            (5, 0.5): 15.361726093873514,
            (5, 2): 30.72345218774703,
        }
        for (b0, dt), value in expected.items():
            self.assertAlmostEqual(delta_b_micro_tesla(b0, dt), value, places=9)
            self.assertNotAlmostEqual(delta_b_micro_tesla(b0, dt), {(1, 0.5): 25.4, (1, 2): 35.9, (3, 0.5): 76.2, (3, 2): 107.7, (5, 0.5): 127, (5, 2): 179.5}[(b0, dt)])

    def test_temperature_ratio_is_two_not_square_root_of_two(self):
        ratio = delta_b_micro_tesla(1, 2) / delta_b_micro_tesla(1, 0.5)
        self.assertAlmostEqual(ratio, 2.0)
        self.assertNotAlmostEqual(ratio, math.sqrt(2))

    def test_invalid_physical_inputs_are_rejected(self):
        for b0, dt in [(0, 1), (-1, 1), (1, 0), (1, -0.5)]:
            with self.assertRaises(ValueError):
                delta_b_micro_tesla(b0, dt)


if __name__ == "__main__":
    unittest.main()
