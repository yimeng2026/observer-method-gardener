from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from checks.harmonic_claim import expansion_coefficients, harmonic_errors, exact_harmonic


class HarmonicClaimTest(unittest.TestCase):
    def test_exact_harmonic_baseline(self):
        self.assertAlmostEqual(exact_harmonic(10), 2.928968253968254, delta=1e-15)

    def test_first_and_second_order_coefficients_match_standard_expansion(self):
        coefficients = expansion_coefficients()
        self.assertAlmostEqual(coefficients["inverseN"], 0.5, delta=1e-15)
        self.assertAlmostEqual(coefficients["inverseNSquared"], -1 / 12, delta=1e-15)

    def test_absolute_error_decreases_on_selected_large_inputs(self):
        errors = harmonic_errors([10, 100, 1000])
        self.assertGreater(errors[0]["absoluteError"], errors[1]["absoluteError"])
        self.assertGreater(errors[1]["absoluteError"], errors[2]["absoluteError"])
        self.assertTrue(all(item["zeta1HasFiniteValue"] is False for item in errors))


if __name__ == "__main__":
    unittest.main()
