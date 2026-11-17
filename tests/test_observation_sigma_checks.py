from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
try:
    from checks.observation_sigma_checks import observation_rows, unverifiable_sigma_rows
except ModuleNotFoundError:
    observation_rows = unverifiable_sigma_rows = None


class ObservationSigmaChecksTest(unittest.TestCase):
    def setUp(self):
        self.assertIsNotNone(observation_rows)
        self.assertIsNotNone(unverifiable_sigma_rows)

    def test_five_displayed_sigmas_are_reproduced(self):
        rows = {row["id"]: row for row in observation_rows()}
        expected = {
            "starlight": 0.2,
            "solarRedshift": 1.0,
            "milkyWayRotation": 0.2,
            "hubble": 0.0,
            "omegaM": 0.0,
        }
        for key, value in expected.items():
            with self.subTest(key=key):
                self.assertAlmostEqual(rows[key]["recomputedSigma"], value, delta=1e-12)
                self.assertAlmostEqual(rows[key]["displayedSigma"], value, delta=1e-12)

    def test_mercury_sigma_is_two_not_one_point_nine(self):
        row = {row["id"]: row for row in observation_rows()}["mercury"]
        self.assertAlmostEqual(row["recomputedSigma"], 2.0, delta=1e-12)
        self.assertEqual(row["displayedSigma"], 1.9)
        self.assertNotEqual(row["recomputedSigma"], row["displayedSigma"])

    def test_numeric_status_rows_without_theory_values_cannot_be_verified(self):
        self.assertEqual(unverifiable_sigma_rows(), [10, 12])


if __name__ == "__main__":
    unittest.main()
