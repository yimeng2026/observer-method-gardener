from pathlib import Path
import math
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from checks.turn_performance_claim import (
    chord_geometry_angle,
    coordinated_turn_bank,
    load_factor_from_net_acceleration,
    turn_radius,
)


class TurnPerformanceClaimTest(unittest.TestCase):
    def test_displayed_radii_follow_the_selected_g_values(self):
        self.assertAlmostEqual(turn_radius(1020, 49 * 9.8), 2166.597251145356, places=9)
        self.assertAlmostEqual(turn_radius(1029, 9 * 9.81), 11992.7624872579, places=9)

    def test_coordinated_bank_angle_is_not_chord_geometry(self):
        self.assertAlmostEqual(coordinated_turn_bank(9), 83.62062979155719, places=12)
        self.assertAlmostEqual(coordinated_turn_bank(50), 88.85400800161142, places=12)
        radius = turn_radius(1020, 49 * 9.8)
        chord_angle = chord_geometry_angle(radius, 20)
        self.assertLess(chord_angle, 0.3)
        self.assertNotAlmostEqual(chord_angle, coordinated_turn_bank(50))

    def test_net_acceleration_and_support_load_are_distinguished(self):
        result = load_factor_from_net_acceleration(49)
        self.assertAlmostEqual(result, 49.01020301937138, places=12)
        self.assertNotEqual(result, 49)


if __name__ == "__main__":
    unittest.main()
