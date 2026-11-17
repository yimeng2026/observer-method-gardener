from fractions import Fraction
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from checks.biaxial_refraction_energy_claim import displayed_energy_coefficients


class BiaxialRefractionEnergyClaimTest(unittest.TestCase):
    def test_two_open_channels_violate_energy_conservation(self):
        result = displayed_energy_coefficients(Fraction(1), Fraction(2), Fraction(1))
        self.assertEqual(result["R"], Fraction(1, 4))
        self.assertEqual(result["t1"], Fraction(1))
        self.assertEqual(result["t2"], Fraction(-1, 2))
        self.assertEqual(result["T1"], Fraction(2))
        self.assertEqual(result["T2"], Fraction(1, 4))
        self.assertEqual(result["energySum"], Fraction(5, 2))

    def test_single_channel_limit_recovers_fresnel_energy_conservation(self):
        result = displayed_energy_coefficients(Fraction(1), Fraction(2), Fraction(0))
        self.assertEqual(result["R"], Fraction(1, 9))
        self.assertEqual(result["T1"], Fraction(8, 9))
        self.assertEqual(result["T2"], Fraction(0))
        self.assertEqual(result["energySum"], Fraction(1))


if __name__ == "__main__":
    unittest.main()
