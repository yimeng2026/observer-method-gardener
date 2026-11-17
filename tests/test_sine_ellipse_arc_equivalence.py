from pathlib import Path
import sys
import unittest

import mpmath as mp

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from checks.sine_ellipse_arc_equivalence import sine_period_arc_length


class SineEllipseArcEquivalenceTest(unittest.TestCase):
    def test_direct_period_integral_matches_ellipse_perimeter(self):
        with mp.workdps(50):
            for a, b in [(mp.mpf(2), mp.mpf(1)), (mp.mpf(3), mp.mpf("1.5"))]:
                result = sine_period_arc_length(a, b)
                self.assertLess(result["absoluteDiscrepancy"], mp.mpf("1e-40"))
                self.assertEqual(result["period"], 2 * mp.pi * b)

    def test_two_to_one_ellipse_has_the_expected_arc_length(self):
        with mp.workdps(50):
            result = sine_period_arc_length(2, 1)
            expected = mp.mpf("9.6884482205476761984285031963918294119539183978866008250831")
            self.assertLess(abs(result["directArcLength"] - expected), mp.mpf("1e-40"))
            self.assertEqual(result["amplitude"], mp.sqrt(3))
            self.assertEqual(result["waveNumber"], 1)

    def test_invalid_semi_axes_are_rejected(self):
        for a, b in [(1, 1), (1, 2), (2, 0), (-2, 1)]:
            with self.subTest(a=a, b=b):
                with self.assertRaises(ValueError):
                    sine_period_arc_length(a, b)


if __name__ == "__main__":
    unittest.main()
