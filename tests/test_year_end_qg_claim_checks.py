from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from checks.year_end_qg_claim_checks import (
    cosmological_constant_rate,
    dark_matter_mass,
    dimensional_findings,
    gravitational_wave_suppression,
    hubble_and_integral_factor,
    proton_log10_lifetime_years,
    qg_energy_scale,
)


class YearEndQGClaimChecksTest(unittest.TestCase):
    def test_qg_energy_scale_is_mev_not_tev(self):
        result = qg_energy_scale()
        self.assertAlmostEqual(result["MeV"], 0.329343238035905, delta=1e-12)
        self.assertAlmostEqual(result["TeV"], 3.29343238035905e-7, delta=1e-15)
        self.assertNotAlmostEqual(result["TeV"], 0.33, delta=1e-9)

    def test_gravitational_wave_suppression_is_not_the_displayed_value(self):
        actual = gravitational_wave_suppression()
        self.assertAlmostEqual(actual, 4.909862904610673e-39, delta=1e-48)
        self.assertNotAlmostEqual(actual, 2.3e-20, delta=1e-45)

    def test_proton_lifetime_exponent_is_not_1p6e34_years(self):
        log10_years = proton_log10_lifetime_years()
        self.assertAlmostEqual(log10_years, 8200.850791829613, delta=1e-9)
        self.assertNotAlmostEqual(log10_years, 34, delta=1)

    def test_hubble_conversion_and_integral_factor(self):
        result = hubble_and_integral_factor()
        self.assertAlmostEqual(result["h0SI"], 2.174694490332e-18, delta=1e-30)
        self.assertAlmostEqual(result["h0KmSPerMpc"], 67.10406035410247, delta=1e-10)
        self.assertAlmostEqual(result["integralFactor"], 753.4378257658794, delta=1e-9)

    def test_cosmological_rate_and_dark_matter_mass(self):
        rate = cosmological_constant_rate()
        mass = dark_matter_mass()
        self.assertAlmostEqual(rate, -8.584715929900633e-13, delta=1e-22)
        self.assertNotAlmostEqual(rate, -1.2e-10, delta=1e-15)
        self.assertAlmostEqual(mass["kg"], 8.358091624306e-25, delta=1e-34)
        self.assertAlmostEqual(mass["GeV"], 468.8545552526038, delta=1e-9)
        self.assertNotAlmostEqual(mass["kg"], 8.359857e-25, delta=1e-29)

    def test_dimensions_are_not_closed_without_extra_physical_factors(self):
        result = dimensional_findings()
        self.assertEqual(result["kappaBaseDimension"], "M^2 L^-4 T")
        self.assertEqual(result["requiredIntegralFactorDimension"], "M^-2 L^3 T^-1")
        self.assertEqual(result["annihilationPrefactorDimension"], "L^2")
        self.assertFalse(result["annihilationRateDimensionallyClosed"])


if __name__ == "__main__":
    unittest.main()
