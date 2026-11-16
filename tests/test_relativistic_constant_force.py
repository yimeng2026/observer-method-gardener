from pathlib import Path
import math
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from checks.relativistic_constant_force import constant_force_state, displayed_initial_residuals, displayed_mass_ratio


class RelativisticConstantForceTest(unittest.TestCase):
    def test_initial_conditions_and_sub_luminal_limit(self):
        state0 = constant_force_state(0, force=3, rest_mass=2, initial_speed=2, c=5)
        self.assertAlmostEqual(state0["v"], 2)
        self.assertAlmostEqual(state0["x"], 0)
        self.assertAlmostEqual(state0["gamma"], 1 / math.sqrt(1 - (2 / 5)**2))
        state = constant_force_state(1e6, force=3, rest_mass=2, initial_speed=2, c=5)
        self.assertLess(abs(state["v"]), 5)
        self.assertGreater(state["v"], 0)
        self.assertGreater(state["gamma"], state0["gamma"])

    def test_kinematics_and_work_energy_identity(self):
        force, mass, c, t = 3.0, 2.0, 5.0, 1.2
        state = constant_force_state(t, force, mass, 2.0, c)
        step = 1e-5
        before = constant_force_state(t - step, force, mass, 2.0, c)
        after = constant_force_state(t + step, force, mass, 2.0, c)
        derivative = (after["x"] - before["x"]) / (2 * step)
        self.assertAlmostEqual(derivative, state["v"], delta=1e-8)
        self.assertAlmostEqual(force * state["x"], mass * c**2 * (state["gamma"] - state0_gamma(2, c)), delta=1e-9)

    def test_displayed_speed_and_position_fail_nonzero_initial_conditions(self):
        result = displayed_initial_residuals(force=3, rest_mass=2, initial_speed=2, c=5)
        self.assertNotAlmostEqual(result["speedVersionA"], 2)
        self.assertNotAlmostEqual(result["speedVersionB"], 2)
        self.assertNotAlmostEqual(result["positionVersionA"], 0)

    def test_displayed_mass_ratio_depends_on_initial_gamma(self):
        ratio = displayed_mass_ratio(0.8, 0.6, 1.0)
        gamma = 1 / math.sqrt(1 - 0.8**2)
        gamma0 = 1 / math.sqrt(1 - 0.6**2)
        self.assertAlmostEqual(ratio, gamma / gamma0)
        self.assertNotAlmostEqual(ratio, gamma)


def state0_gamma(v, c):
    return 1 / math.sqrt(1 - (v / c)**2)


if __name__ == "__main__":
    unittest.main()
