from pathlib import Path
import math
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
try:
    from checks.eecc_grb_engine_checks import (
        accretion_reconnection,
        agn_beaming_example,
        beaming_and_duration,
        jet_event_example,
        lorentz_and_variability,
        rotation_engine,
        smbh_example,
        unit_and_profile_checks,
    )
except ModuleNotFoundError:
    accretion_reconnection = agn_beaming_example = None
    beaming_and_duration = jet_event_example = None
    lorentz_and_variability = rotation_engine = None
    smbh_example = unit_and_profile_checks = None


class EeccGrbEngineChecksTest(unittest.TestCase):
    def setUp(self):
        self.assertTrue(all([
            accretion_reconnection, agn_beaming_example,
            beaming_and_duration, jet_event_example,
            lorentz_and_variability, rotation_engine,
            smbh_example, unit_and_profile_checks,
        ]), "EECC GRB checker functions must exist")

    def assertClose(self, actual, expected, tolerance=1e-9):
        self.assertTrue(
            math.isclose(actual, expected, rel_tol=tolerance, abs_tol=0.0),
            (actual, expected),
        )

    def test_rotation_energy_versions_and_magnetic_scales(self):
        result = rotation_engine()
        self.assertClose(result["momentOfInertia"], 9.3636e38)
        self.assertClose(result["rotationalEnergyFromInertia"], 1.17045e46)
        self.assertClose(result["rotationalEnergyFromRestMass"], 8.088796606134766e45)
        self.assertClose(result["rotationalEnergyVersionRatio"], 1.17045e46 / 8.088796606134766e45)
        self.assertClose(result["surfaceMagneticField"], 1e8 * (1e6 / 5.1e4)**2)
        self.assertClose(result["reconnectionArea"], math.pi * 5.1e4**2 * 1e-6)

    def test_engine_power_conflicts_survive_rounded_and_exact_substitution(self):
        result = rotation_engine()
        self.assertClose(result["enginePowerFromPrintedRoundedValues"], 1.41e29, 0.01)
        self.assertClose(result["enginePowerFromWrittenFormula"], 1.44e31, 0.01)
        self.assertClose(result["magneticFieldArithmeticRatio"], 10.117566118294585)
        self.assertGreater(result["claimedPowerOverPrintedRoundedEvaluation"], 1e15)
        self.assertGreater(result["claimedPowerOverExactScalingEvaluation"], 1e13)
        self.assertFalse(result["claimedPowerMatchesWrittenFormula"])

    def test_duration_is_not_a_short_or_long_burst_after_same_formula_recalculation(self):
        result = rotation_engine()
        self.assertGreater(result["durationFromInertia"], 1e14)
        self.assertGreater(result["durationFromRestMass"], 1e14)
        self.assertGreater(result["durationFromInertiaUsingPrintedRoundedValues"], 1e16)
        self.assertFalse(result["shortOrLongDurationDemonstrated"])

    def test_beaming_factor_reciprocal_conventions_cannot_be_mixed(self):
        result = beaming_and_duration()
        self.assertClose(result["claimedEngineDividedBy500"], 3.6e41)
        self.assertClose(result["claimedEngineTimes500"], 9.0e46)
        self.assertFalse(result["divisionMatchesObservedMinimum"])
        self.assertFalse(result["reciprocalNotationMatchesDivisionFormula"])

    def test_lorentz_factor_does_not_support_relativistic_small_angle_jet(self):
        result = lorentz_and_variability()
        self.assertClose(result["gammaMax"], 0.434, 0.01)
        self.assertFalse(result["physicallyRelativistic"])
        self.assertGreater(result["gammaDefiniteIntegralWithInitialOne"], 1.14)
        self.assertLess(result["gammaDefiniteIntegralWithInitialOne"], 1.15)
        self.assertLess(result["gammaDefiniteIntegralWithInitialOne"], 2.0)
        self.assertClose(result["thetaAtGamma300"], math.sqrt(6.0e4 / 5.1e4) / 300)
        self.assertGreater(result["thetaAtDefiniteIntegralGamma"], 0.9)
        self.assertFalse(result["smallAnglePredictionEstablished"])

    def test_reconnection_variability_arithmetic_is_retained(self):
        result = lorentz_and_variability()
        self.assertClose(result["minimumVariabilityTime"], 51 / 299792458.0)

    def test_reconnection_rate_and_total_energy_coefficient_do_not_reproduce_claims(self):
        result = accretion_reconnection()
        self.assertClose(result["pairInflowOverC"], 8.29e-5 / math.pi)
        self.assertGreater(result["protonInflowOverC"], 3e-6)
        self.assertLess(result["protonInflowOverC"], 5e-6)
        self.assertGreater(result["normalizedEnergyEstimateJ"], 1e11)
        self.assertLess(result["normalizedEnergyEstimateJ"], 1e12)
        self.assertGreater(result["claimedEnergyOverEstimate"], 1e33)
        self.assertClose(result["energyWhenAngleHalvedRatio"], 1.0, 1e-12)

    def test_si_label_and_virial_profile_identity_fail(self):
        result = unit_and_profile_checks()
        self.assertClose(result["magneticPressureSiAtOneTesla"], 1 / (2 * 4e-7 * math.pi))
        self.assertClose(result["virialLeftAtTwoReferenceRadii"], 0.5)
        self.assertClose(result["virialRightAtTwoReferenceRadii"], 0.25)
        self.assertFalse(result["virialIdentityValidAwayFromReferenceRadius"])
        self.assertFalse(result["siUnitSystemClosed"])

    def test_supermassive_example_energy_and_luminosity_are_overestimated(self):
        result = smbh_example()
        self.assertClose(result["neutronStarBindingEnergyErgs"], 2.5e53, 0.01)
        self.assertGreater(result["rotationalEnergyErgs"], 8e56)
        self.assertLess(result["rotationalEnergyErgs"], 1e57)
        self.assertGreater(result["claimedEnergyOverRecomputed"], 20)
        self.assertGreater(result["correctedIsotropicLuminosity"], 1e59)
        self.assertLess(result["correctedIsotropicLuminosity"], 2e59)
        self.assertLess(result["correctedLowEfficiencyLuminosity"], 2e55)

    def test_agn_geometry_example_and_lifetime_mass_cancellation(self):
        result = agn_beaming_example()
        self.assertClose(result["twoPiSolidAngleRatio"], 0.252)
        self.assertGreater(result["exactOpeningAngle"], 0.70)
        self.assertLess(result["exactOpeningAngle"], 0.75)
        self.assertNotEqual(round(result["exactOpeningAngle"], 2), 0.54)
        self.assertGreater(result["dopplerFromActualRatio"], 1.99)
        self.assertLess(result["dopplerFromActualRatio"], 2.01)
        self.assertClose(result["lifetimePerInverseEddingtonRatioYears"], 5e7, 0.01)
        self.assertClose(result["lifetimeMassRatio"], 1.0, 1e-12)

    def test_jet_event_length_power_and_time_recalculations(self):
        result = jet_event_example()
        self.assertClose(result["longitudinalLengthFromInputs"], 2.7e13)
        self.assertClose(result["longitudinalLengthRatio"], 100.0)
        self.assertClose(result["powerRatioOverImpliedClaim"], 1e12, 0.001)
        self.assertGreater(result["isotropicFromWrittenFormula"] / result["claimedIsotropic"], 1e11)
        self.assertClose(result["angularVariabilityTime"], (1e14 / 3e10) * (8.29e-5)**2 / 2)
        self.assertClose(result["gammaTimesJetAngle"], 30.0)
        self.assertFalse(result["powerUnitIsWatt"])
        self.assertFalse(result["observationalFitPerformed"])


if __name__ == "__main__":
    unittest.main()
