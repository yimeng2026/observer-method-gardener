from pathlib import Path
import sys
import unittest

import mpmath as mp

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from checks.desboves_model_audit import (
    displayed_derivative,
    displayed_y,
    find_displayed_minimum,
    find_displayed_root,
    prime_pi,
    primes_between_squares,
    smooth_pi_derivative,
    smooth_pi_model,
)


class DesbovesModelAuditTest(unittest.TestCase):
    def test_smooth_model_has_the_claimed_derivative_but_arbitrary_constant(self):
        with mp.workdps(50):
            x = mp.mpf(10)
            h = mp.mpf("1e-5")
            central_difference = (smooth_pi_model(x + h) - smooth_pi_model(x - h)) / (2 * h)
            shifted_difference = (
                smooth_pi_model(x + h) + 7 - smooth_pi_model(x - h) - 7
            ) / (2 * h)
            self.assertLess(abs(central_difference - smooth_pi_derivative(x)), mp.mpf("1e-8"))
            self.assertLess(abs(smooth_pi_derivative(x) - 1 / (1 + mp.log(x))), mp.mpf("1e-30"))
            self.assertLess(abs(shifted_difference - smooth_pi_derivative(x)), mp.mpf("1e-8"))

    def test_displayed_interval_lower_bound_has_immediate_counterexamples(self):
        for x in (mp.mpf("6.7"), 9, 10):
            self.assertGreater(x / mp.log(x), prime_pi(x))
        self.assertEqual(prime_pi(10), 4)

    def test_displayed_root_and_local_minimum_are_numerically_recovered(self):
        root = find_displayed_root()
        minimum = find_displayed_minimum()
        self.assertGreater(root, mp.mpf("0.15724"))
        self.assertLess(root, mp.mpf("0.15725"))
        self.assertLess(abs(displayed_y(root)), mp.mpf("1e-25"))
        self.assertGreater(minimum["x"], mp.mpf("1.2677"))
        self.assertLess(minimum["x"], mp.mpf("1.2679"))
        self.assertGreater(minimum["y"], mp.mpf("0.6729"))
        self.assertLess(minimum["y"], mp.mpf("0.6730"))
        self.assertLess(abs(displayed_derivative(minimum["x"])), mp.mpf("1e-20"))
        self.assertGreater(minimum["secondDerivative"], 0)

    def test_finite_square_interval_checks_do_not_promote_to_theorem(self):
        self.assertEqual(primes_between_squares(1), [2, 3])
        self.assertEqual(primes_between_squares(2), [5, 7])
        self.assertEqual(primes_between_squares(3), [11, 13])
        self.assertEqual(primes_between_squares(4), [17, 19, 23])
        self.assertTrue(all(len(primes_between_squares(n)) >= 2 for n in range(1, 1001)))


if __name__ == "__main__":
    unittest.main()
