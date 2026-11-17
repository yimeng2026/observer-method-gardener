from pathlib import Path
import math
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from checks.generalized_lorentz_factor_claim import (
    coulomb_mass_ratios,
    gravitational_potential_terms,
    work_energy_state,
)


class GeneralizedLorentzFactorClaimTest(unittest.TestCase):
    def test_work_energy_has_no_extra_half(self):
        result = work_energy_state(work=4.5, rest_mass=2.0, c=3.0)
        self.assertAlmostEqual(result["gamma"], 1.25)
        self.assertAlmostEqual(result["speed"], 1.8)
        self.assertAlmostEqual(result["kineticEnergy"], 4.5)
        self.assertNotEqual(result["gamma"], 1 + 4.5 / (2 * 2.0 * 3.0**2))

    def test_displayed_coulomb_force_integrates_linearly_not_to_exponential(self):
        result = coulomb_mass_ratios(k_e2=1.0, rest_mass=1.0, c=1.0, reference_radius=2.0, radius=4.0)
        self.assertAlmostEqual(result["directIntegratedRatio"], 0.75)
        self.assertAlmostEqual(result["claimedExponentialRatio"], math.exp(-0.25))
        self.assertNotAlmostEqual(result["directIntegratedRatio"], result["claimedExponentialRatio"])

    def test_gravitational_potential_retains_outer_radius_and_reference_term(self):
        result = gravitational_potential_terms(gm=1.0, rest_mass=1.0, c=1.0, reference_radius=2.0, radius=4.0)
        self.assertAlmostEqual(result["exactPotential"], -math.exp(-0.25) / 4)
        self.assertAlmostEqual(result["firstOrderPotential"], -0.1875)
        self.assertNotAlmostEqual(result["firstOrderPotential"], result["missingRadiusDisplayedForm"])


if __name__ == "__main__":
    unittest.main()
