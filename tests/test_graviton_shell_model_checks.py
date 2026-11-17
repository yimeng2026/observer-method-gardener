from pathlib import Path
import math
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
try:
    from checks.graviton_shell_model_checks import (
        action_dimensions,
        decay_channel_differences,
        energy_and_thermal_scale,
        energy_density_ratio,
        finite_shell_count_and_cutoff,
        frequency_conversions,
        geometry_and_cutoffs,
        mercury_baseline,
        microphysical_frequency_version,
        spectral_sequence,
    )
except ModuleNotFoundError:
    action_dimensions = decay_channel_differences = None
    energy_and_thermal_scale = energy_density_ratio = None
    finite_shell_count_and_cutoff = frequency_conversions = None
    geometry_and_cutoffs = mercury_baseline = None
    microphysical_frequency_version = spectral_sequence = None


class GravitonShellModelChecksTest(unittest.TestCase):
    def setUp(self):
        self.assertTrue(all([
            action_dimensions, decay_channel_differences,
            energy_and_thermal_scale, energy_density_ratio,
            finite_shell_count_and_cutoff, frequency_conversions,
            geometry_and_cutoffs, mercury_baseline,
            microphysical_frequency_version, spectral_sequence,
        ]), "graviton-shell checker functions must exist")

    def assertClose(self, actual, expected, tolerance=1e-9):
        self.assertTrue(
            math.isclose(actual, expected, rel_tol=tolerance, abs_tol=0.0),
            (actual, expected),
        )

    def test_lambda_mass_binding_energy_is_not_the_displayed_energy(self):
        result = energy_and_thermal_scale()
        self.assertClose(result["lambdaMassKg"], 3.5176729395907616e-24)
        self.assertClose(result["bindingEnergyJ"], 5.502637345899416e-84)
        self.assertNotEqual(result["bindingEnergyJ"], 2.1e-46)

    def test_displayed_energy_temperature_and_length_are_inconsistent(self):
        result = energy_and_thermal_scale()
        self.assertClose(result["displayedTemperatureK"], 1.521023808368383e-23)
        self.assertClose(result["displayedLengthM"], 1.5054889388378866e20)
        self.assertNotEqual(result["displayedTemperatureK"], 1.5e-5)
        self.assertNotEqual(result["displayedLengthM"], 1.6e26)

    def test_energy_density_ratio_is_linear_but_coefficient_is_wrong(self):
        result = energy_density_ratio()
        self.assertClose(result["coefficientPerK"], 5.212761006839915e-17)
        self.assertClose(result["at27K"], 1.4074454718467772e-16)
        self.assertClose(result["at1e15K"], 0.052127610068399145)
        self.assertNotEqual(result["at1e15K"], 1e-5)

    def test_bohr_radius_and_cutoff_versions_cannot_be_merged(self):
        result = geometry_and_cutoffs()
        self.assertClose(result["bohrRadiusM"], 5.714285714e25)
        self.assertClose(result["planckCutoff"], 6.25e15)
        self.assertClose(result["alpha45Cutoff"], 5.714285714e44)
        self.assertClose(result["alpha39Cutoff"], 1.694915254e38)

    def test_decay_channels_use_the_displayed_energy_table(self):
        result = decay_channel_differences()
        expected = {
            "2S0->1S0": 9.90e-28,
            "2P1->1S0": 9.91e-28,
            "2P2->1S0": 9.92e-28,
            "2P3->1S0": 9.93e-28,
            "3S0->2P1": 1.82e-28,
            "3P1->2S0": 1.84e-28,
            "3D1->2P1": 1.84e-28,
        }
        self.assertEqual(set(result), set(expected))
        for channel, value in expected.items():
            with self.subTest(channel=channel):
                self.assertClose(result[channel], value)

    def test_transition_and_radiation_frequency_conversions(self):
        result = frequency_conversions()
        self.assertClose(result["normalized2To1Hz"], 2.3772914628741136e-13)
        self.assertClose(result["displayedE0TransitionHz"], 1.8134919315636883e-13)
        self.assertClose(result["milliEv23Hz"], 556137525679.5311)
        self.assertClose(result["halfMillimetreHz"], 599584916000.0)
        self.assertNotEqual(result["normalized2To1Hz"], 2.4e-8)
        self.assertNotEqual(result["displayedE0TransitionHz"], 2.4e-8)

    def test_spectral_table_and_high_shell_claim_fail_their_own_rule(self):
        result = spectral_sequence()
        self.assertClose(result["2->1Hz"], 1.8075e-8)
        self.assertClose(result["3->2Hz"], 3.3472222222222223e-9)
        self.assertClose(result["4->3Hz"], 1.1715277777777777e-9)
        self.assertClose(result["5->4Hz"], 5.4225e-10)
        self.assertClose(result["9->8Hz"], 7.903163580246915e-11)
        self.assertClose(result["9->8WavelengthM"], 3.793322192511593e18)
        self.assertNotEqual(result["4->3Hz"], 3.79e-9)
        self.assertNotEqual(result["5->4Hz"], 2.43e-9)
        self.assertNotEqual(result["9->8WavelengthM"], 50.2e-6)

    def test_microphysical_mass_does_not_generate_the_advertised_frequency(self):
        result = microphysical_frequency_version()
        self.assertClose(result["alphaFromMass"], 2.5544313186429877e-121)
        self.assertClose(result["comptonWavelengthM"], 3.197884490537056e25)
        self.assertClose(result["baseFrequencyHz"], 4.867842592934723e-260)
        self.assertNotEqual(result["alphaFromMass"], 1.75e-45)
        self.assertNotEqual(result["baseFrequencyHz"], 2.41e-8)

    def test_five_dimensional_c4_action_has_the_wrong_dimensions(self):
        self.assertEqual(action_dimensions(4), {"M": 1, "L": 3, "T": -2})
        self.assertEqual(action_dimensions(3), {"M": 1, "L": 2, "T": -1})

    def test_finite_shell_arithmetic_does_not_prove_nine_shells(self):
        result = finite_shell_count_and_cutoff()
        self.assertEqual(result["displayedStateTotal"], 85)
        self.assertClose(result["radialRoot"], math.sqrt(1e26 / 1.2e26))
        self.assertEqual(result["strictFloor"], 0)
        self.assertEqual(result["nearestInteger"], 1)
        self.assertFalse(result["supportsNineShells"])

    def test_mercury_standard_term_and_metric_correction_dimensions(self):
        result = mercury_baseline()
        self.assertClose(result["compactness"], 2.5500215329469452e-8)
        self.assertClose(result["radiansPerOrbit"], 5.018830123573565e-7)
        self.assertClose(result["arcsecondsPerCentury"], 42.982862333138016)
        self.assertEqual(result["alphaSquaredOverRSquaredLengthExponent"], -2)
        self.assertFalse(result["metricCorrectionIsDimensionless"])


if __name__ == "__main__":
    unittest.main()
