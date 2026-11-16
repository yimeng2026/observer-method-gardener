from fractions import Fraction
from pathlib import Path
import sys
import unittest

import mpmath as mp

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from checks.prime_counting_estimates import evaluate_estimates, legendre_pi, mertens_prefactor, sieve_product


class PrimeCountingEstimatesTest(unittest.TestCase):
    def test_x8e25_main_comment_values_and_screenshot_mismatch(self):
        result = evaluate_estimates("8e25")
        expected = {
            "xOverLog": "1.3412901151834674e24",
            "li": "1.3645731465572533e24",
            "scaledEi": "1.3416808399175136e24",
            "riemannR": "1.3645731465570979e24",
        }
        for key, value in expected.items():
            self.assertLess(abs(mp.mpf(result[key]) - mp.mpf(value)) / mp.mpf(value), mp.mpf("1e-12"))
        self.assertGreater(mp.mpf("1.724e24") - mp.mpf(result["li"]), mp.mpf("0.3e24"))
        self.assertGreater(abs(mp.mpf("1.715e24") - mp.mpf(result["xOverLog"])) / mp.mpf(result["xOverLog"]), mp.mpf("0.2"))
        self.assertGreater(abs(mp.mpf("1.721e24") - mp.mpf(result["riemannR"])) / mp.mpf(result["riemannR"]), mp.mpf("0.2"))

    def test_legendre_formula_exposes_naive_product_counterexample(self):
        self.assertEqual(legendre_pi(25), 9)
        self.assertEqual(legendre_pi(100), 25)
        self.assertEqual(sieve_product(25), Fraction(20, 3))
        self.assertNotEqual(float(sieve_product(25)), legendre_pi(25))

    def test_mertens_product_has_extra_prefactor(self):
        self.assertGreater(mertens_prefactor(), 1.12)
        self.assertLess(mertens_prefactor(), 1.13)

    def test_riemannr_large_value_is_not_returned_as_exact_prime_count(self):
        result = evaluate_estimates("1e30")
        self.assertLess(abs(mp.mpf(result["riemannR"]) - mp.mpf("1.46923988977204e28")) / mp.mpf("1.46923988977204e28"), mp.mpf("1e-13"))
        self.assertIsNone(result["exactPi"])
        self.assertEqual(result["status"], "smooth_estimates_not_exact_counts")


if __name__ == "__main__":
    unittest.main()
