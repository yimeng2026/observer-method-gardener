from pathlib import Path
import sys
import unittest

import mpmath as mp

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from checks.ellipsoid_surface_claim import (
    article_surface_area,
    direct_surface_area,
    standard_surface_area,
)


class EllipsoidSurfaceClaimTest(unittest.TestCase):
    def test_article_formula_matches_standard_elliptic_expression(self):
        article = article_surface_area(5, 3, 2)
        standard = standard_surface_area(5, 3, 2)
        self.assertLess(abs(article - standard), mp.mpf("1e-40"))
        self.assertTrue(mp.nstr(article, 45).startswith("134.7751767249036344646017980727215"))
        self.assertFalse(mp.nstr(article, 45).startswith("134.775176724903634464601842410659640467"))

    def test_article_formula_matches_direct_parametric_surface_integral(self):
        article = article_surface_area(5, 3, 2)
        direct = direct_surface_area(5, 3, 2)
        self.assertLess(abs(article - direct), mp.mpf("1e-20"))

    def test_direct_integral_recovers_sphere_without_degenerate_elliptic_parameters(self):
        direct = direct_surface_area(2, 2, 2)
        # The reference pi must have comparable precision to the returned integral.
        with mp.workdps(60):
            expected = 16 * mp.pi
        self.assertLess(abs(direct - expected), mp.mpf("1e-20"))


if __name__ == "__main__":
    unittest.main()
