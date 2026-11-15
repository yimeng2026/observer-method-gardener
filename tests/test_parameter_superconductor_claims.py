from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from checks.parameter_superconductor_claims import audit_parameter_superconductor


class ParameterSuperconductorClaimsTest(unittest.TestCase):
    def test_public_units_and_temperature_bound_are_reproducible(self):
        result = audit_parameter_superconductor()
        self.assertEqual(result["neutrinoTheoryEV"], [8.6, 12.7, 50000.0])
        self.assertEqual(result["factorAboveCommonMillielectronvoltScale"], [1000.0, 1000.0, 1000000.0])
        self.assertAlmostEqual(result["superconductorUpperK"], 0.05652094155329249)
        self.assertTrue(result["superconductorUpperBelowClaimed90K"])
        self.assertFalse(result["evidenceUpgrade"])

    def test_invalid_superconductor_inputs_are_rejected(self):
        for energy, theta, ratio in [(0, 0.11, 1000), (0.02, -0.11, 1000), (0.02, 0.11, 1)]:
            with self.assertRaises(ValueError):
                audit_parameter_superconductor(energy_ev=energy, theta=theta, length_ratio=ratio)


if __name__ == "__main__":
    unittest.main()
