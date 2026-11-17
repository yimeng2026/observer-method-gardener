from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
try:
    from checks.qg_submission_comparison_checks import comparison_table
except ModuleNotFoundError:
    comparison_table = None


class QGSubmissionComparisonChecksTest(unittest.TestCase):
    def rows(self):
        self.assertIsNotNone(comparison_table, "comparison-table checker must exist")
        return {row["id"]: row for row in comparison_table()}

    def test_cosmology_rows_reproduce_the_displayed_rounded_percentages(self):
        rows = self.rows()
        expected = {
            "H0": 0.003857566765578635,
            "omegaM": 0.002922077922077922,
            "omegaB": 0.006172839506172839,
            "omegaLambda": 0.001300578034682081,
        }
        displayed = {
            "H0": 0.0039,
            "omegaM": 0.0029,
            "omegaB": 0.0062,
            "omegaLambda": 0.0013,
        }
        for key, value in expected.items():
            with self.subTest(key=key):
                self.assertAlmostEqual(rows[key]["recomputedRelativeError"], value, delta=1e-15)
                self.assertAlmostEqual(rows[key]["displayedRelativeError"], displayed[key], delta=1e-12)
                self.assertGreater(value, 1e-8)

    def test_electron_and_proton_mass_errors_are_both_about_1p5e_minus_8(self):
        rows = self.rows()
        self.assertAlmostEqual(rows["electronMass"]["recomputedRelativeError"], 1.5533432846472353e-8, delta=1e-20)
        self.assertAlmostEqual(rows["protonMass"]["recomputedRelativeError"], 1.5359119497444377e-8, delta=1e-20)
        self.assertEqual(rows["electronMass"]["displayedRelativeError"], 1.5e-8)
        self.assertEqual(rows["protonMass"]["displayedRelativeError"], 1.5e-8)

    def test_alpha_inverse_error_is_ten_times_larger_than_displayed(self):
        row = self.rows()["alphaInverse"]
        self.assertAlmostEqual(row["recomputedRelativeError"], 6.129776158198393e-10, delta=1e-22)
        self.assertEqual(row["displayedRelativeError"], 6e-11)
        self.assertGreater(row["recomputedRelativeError"], 10 * row["displayedRelativeError"])


if __name__ == "__main__":
    unittest.main()
