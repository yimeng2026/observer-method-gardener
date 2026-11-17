from pathlib import Path
import math
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
try:
    from checks.resonance_prediction_checks import (
        branching_and_spectrum,
        collider_yields,
        evidence_counts,
        mass_and_dark_energy,
        mass_ratios,
        mixing_angle,
        shell_geometry,
        width_coupling_and_lifetime,
    )
except ModuleNotFoundError:
    branching_and_spectrum = collider_yields = evidence_counts = None
    mass_and_dark_energy = mass_ratios = mixing_angle = None
    shell_geometry = width_coupling_and_lifetime = None


class ResonancePredictionChecksTest(unittest.TestCase):
    def setUp(self):
        functions = [
            branching_and_spectrum, collider_yields, evidence_counts,
            mass_and_dark_energy, mass_ratios, mixing_angle,
            shell_geometry, width_coupling_and_lifetime,
        ]
        self.assertTrue(all(functions), "resonance checker functions must exist")

    def assertClose(self, actual, expected, tolerance=1e-10):
        self.assertTrue(math.isclose(actual, expected, rel_tol=tolerance, abs_tol=tolerance), (actual, expected))

    def test_displayed_mass_formula_gives_mev_not_tev(self):
        result = mass_and_dark_energy()
        self.assertClose(result["baseMeV"], 0.32934322341438066)
        self.assertClose(result["predictedMeV"], 18.75822708549158)
        self.assertClose(result["predictedTeV"], 1.875822708549158e-5)
        self.assertGreater(result["targetToPredictedMassRatio"], 2e5)
        self.assertEqual(result["deltaThetaLogSensitivity"], -0.25)

    def test_dark_energy_quantum_unit_conversion(self):
        result = mass_and_dark_energy()
        self.assertClose(result["oneMilliEvKg"], 1.7826619216278975e-39)
        self.assertClose(result["displayedKgInEv"], 5.609588603804451e-34)
        self.assertNotEqual(result["displayedKgInEv"], 1e-3)

    def test_width_is_reproducible_but_displayed_lifetime_is_not(self):
        result = width_coupling_and_lifetime()
        self.assertClose(result["widthGeV"], 86.43813336782553)
        self.assertClose(result["lifetimeSecondsAt87GeV"], 7.565654677011494e-27)
        self.assertNotEqual(result["lifetimeSecondsAt87GeV"], 5e-27)

    def test_displayed_factors_do_not_yield_the_chosen_coupling(self):
        result = width_coupling_and_lifetime()
        self.assertClose(result["kappaFromDisplayedFactors"], 85.64178953863544)
        self.assertEqual(result["chosenKappa"], 5.24e-4)
        self.assertGreater(result["kappaFromDisplayedFactors"] / result["chosenKappa"], 1e5)

    def test_mass_ratios_expose_mev_gev_mixing(self):
        result = mass_ratios()
        self.assertClose(result["proton"], 4575.431889036459)
        self.assertClose(result["electron"], 8401191.496782461)
        self.assertClose(result["darkMatter"], 9.156357663384691)
        self.assertClose(result["massOver8p6GeV"], 499.1860465116279)
        self.assertClose(result["massOver8p6RelativeDifference"], 0.06469275155635956)
        self.assertLess(result["proton"], 4.58e6 / 100)
        self.assertLess(result["electron"], 8.41e9 / 100)
        self.assertLess(result["darkMatter"], 9.15e3 / 100)

    def test_graviton_and_planck_ratios_are_not_reproduced(self):
        result = mass_ratios()
        self.assertClose(result["graviton"], 6.957243297139092e44)
        self.assertClose(result["planck"], 3.518852459016393e-16)
        self.assertNotEqual(result["graviton"], 3.9e61)
        self.assertNotEqual(result["planck"], 1.75e-16)

    def test_mixing_angle_and_components_are_not_reproduced(self):
        result = mixing_angle()
        self.assertClose(result["radians"], 0.0010535819908720628)
        self.assertClose(result["degrees"], 0.06036580144796003)
        self.assertClose(result["cosSquared"], 0.9999988899653992)
        self.assertClose(result["sinSquared"], 1.1100346007640912e-6)
        self.assertNotEqual(result["radians"], 0.148)
        self.assertNotEqual(result["sinSquared"], 0.022)

    def test_shell_five_interval_is_empty(self):
        result = shell_geometry()
        self.assertClose(result["r5Meters"], 9.535816161833838e-14)
        self.assertClose(result["r5OverLambda"], 0.15915494309189535)
        self.assertGreater(result["shell5LowerOverLambda"], result["shell5UpperOverLambda"])
        self.assertFalse(result["shell5Nonempty"])

    def test_raw_event_arithmetic_is_kept_but_energy_scaling_conflicts(self):
        result = collider_yields()
        for key, expected in {"run2": 238, "run3": 510, "gg300": 312, "tt300": 111, "zh300": 45, "gamma300": 5.1}.items():
            self.assertClose(result[key], expected)
        self.assertEqual(result["heConstantCrossSection"], 25500)
        self.assertEqual(result["heAdvertisedTimesFour"], 102000)
        self.assertEqual(result["fccConstantCrossSection"], 51000)
        self.assertEqual(result["fccAdvertisedTimesTwenty"], 1020000)

    def test_counts_add_up_but_error_bins_exclude_the_claimed_maximum(self):
        result = evidence_counts()
        self.assertEqual(result["categoryTotal"], 416)
        self.assertEqual(result["errorBinTotal"], 416)
        self.assertEqual(result["newParticlePrecisionTotal"], 128)
        self.assertEqual(result["newParticleTimingTotal"], 128)
        self.assertFalse(result["claimedMaximumInsideErrorBins"])

    def test_branching_arithmetic_is_kept_and_resonance_tolerance_fails(self):
        result = branching_and_spectrum()
        self.assertClose(result["branchingSum"], 1.0)
        self.assertClose(result["ggCrossSection"], 1.037)
        self.assertClose(result["ttCrossSection"], 0.374)
        self.assertClose(result["actualMassRatio"], 3.0328441649196365)
        self.assertClose(result["targetMassRatio"], 3.0168209096526786)
        self.assertFalse(result["actualWithinDisplayedTolerance"])


if __name__ == "__main__":
    unittest.main()
