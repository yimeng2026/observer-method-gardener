from pathlib import Path
import math
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from checks.quaternion_wavefunction_claim import displayed_product, qexp_closed, qexp_series, qmul


class QuaternionWavefunctionClaimTest(unittest.TestCase):
    def assertQuaternionAlmostEqual(self, left, right, places=10):
        for a, b in zip(left, right):
            self.assertAlmostEqual(a, b, places=places)

    def test_hamilton_multiplication_is_noncommutative(self):
        ij = qmul((0, 1, 0, 0), (0, 0, 1, 0))
        ji = qmul((0, 0, 1, 0), (0, 1, 0, 0))
        self.assertEqual(ij, (0, 0, 0, 1))
        self.assertEqual(ji, (0, 0, 0, -1))
        self.assertNotEqual(ij, ji)

    def test_closed_exponential_matches_independent_series(self):
        for alpha, beta, gamma in [(0.2, 0.3, -0.4), (0.0, math.pi / 4, math.pi / 4), (-0.2, 1.2, 0.7)]:
            self.assertQuaternionAlmostEqual(qexp_closed(alpha, beta, gamma), qexp_series(alpha, beta, gamma), places=9)

    def test_product_factorization_and_j_component_are_not_general(self):
        beta, gamma = 0.4, 0.8
        product = displayed_product(beta, gamma)
        direct = qexp_closed(0.0, beta, gamma)
        self.assertNotAlmostEqual(product[0], direct[0])
        self.assertAlmostEqual(product[2], math.cos(beta) * math.sin(gamma))
        self.assertNotAlmostEqual(product[2], math.sin(beta) * math.sin(gamma))

    def test_zero_norm_and_single_imaginary_axis_recover_euler_formula(self):
        self.assertQuaternionAlmostEqual(qexp_closed(0.3, 0.0, 0.0), (math.exp(0.3), 0.0, 0.0, 0.0))
        beta = 0.7
        self.assertQuaternionAlmostEqual(qexp_closed(0.0, beta, 0.0), (math.cos(beta), math.sin(beta), 0.0, 0.0))


if __name__ == "__main__":
    unittest.main()
