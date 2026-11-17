#!/usr/bin/env python3
"""Independent arithmetic checks for the 2025-12-14 EECC/GRB post.

Several functions intentionally evaluate the formulas exactly as printed.  That
exposes substitution and convention conflicts; it does not make those formulas
dimensionally or physically valid.  No observational fit is performed here.
"""
from __future__ import annotations

import json
import math

C = 299792458.0
M_SOLAR = 1.98847e30
M_ELECTRON = 9.1093837015e-31
M_PROTON = 1.67262192369e-27


def rotation_engine() -> dict[str, float | bool]:
    mass = 6.0e30
    ellipsoid_mass = 0.15 * mass
    semi_major = 5.1e4
    omega = 5.0e3
    zeta = 1e-6
    inertia = (2 / 5) * ellipsoid_mass * semi_major**2
    energy_inertia = 0.5 * inertia * omega**2
    energy_rest_mass = 0.1 * 0.15 * mass * C**2
    magnetic_field = 1e8 * (1e6 / semi_major)**2
    area = math.pi * semi_major**2 * zeta
    engine_power = 0.1 * magnetic_field**2 * C * area / (8 * math.pi)
    printed_rounded_power = 0.1 * (3.8e9)**2 * 3.0e8 * 8.2e3 / (8 * math.pi)
    claimed_power = 1.8e44
    return {
        "momentOfInertia": inertia,
        "rotationalEnergyFromInertia": energy_inertia,
        "rotationalEnergyFromRestMass": energy_rest_mass,
        "rotationalEnergyVersionRatio": energy_inertia / energy_rest_mass,
        "surfaceMagneticField": magnetic_field,
        "printedSurfaceMagneticField": 3.8e9,
        "magneticFieldArithmeticRatio": magnetic_field / 3.8e9,
        "reconnectionArea": area,
        "enginePowerFromWrittenFormula": engine_power,
        "enginePowerFromPrintedRoundedValues": printed_rounded_power,
        "claimedPowerOverExactScalingEvaluation": claimed_power / engine_power,
        "claimedPowerOverPrintedRoundedEvaluation": claimed_power / printed_rounded_power,
        "claimedPowerMatchesWrittenFormula": False,
        "durationFromInertia": energy_inertia / engine_power,
        "durationFromRestMass": energy_rest_mass / engine_power,
        "durationFromInertiaUsingPrintedRoundedValues": energy_inertia / printed_rounded_power,
        "shortOrLongDurationDemonstrated": False,
    }


def beaming_and_duration() -> dict[str, float | bool]:
    claimed_engine = 1.8e44
    divided = claimed_engine / 500
    multiplied = claimed_engine * 500
    return {
        "claimedEngineDividedBy500": divided,
        "claimedEngineTimes500": multiplied,
        "observedMinimum": 1e44,
        "divisionMatchesObservedMinimum": divided >= 1e44,
        "reciprocalNotationMatchesDivisionFormula": False,
        "beamingFactorAsPrinted": 900.0,
    }


def lorentz_and_variability() -> dict[str, float | bool]:
    semi_major = 5.1e4
    omega = 5.0e3
    light_cylinder = 6.0e4
    gamma_max = (2 / 5) * (omega**2 * semi_major**2 / C**2) * (light_cylinder / semi_major)**(5 / 2)
    lower_limit_term = (2 / 5) * omega**2 * semi_major**2 / C**2
    gamma_definite_integral = 1 + gamma_max - lower_limit_term
    theta_at_300 = math.sqrt(light_cylinder / semi_major) / 300
    theta_at_computed_gamma = math.sqrt(light_cylinder / semi_major) / gamma_max
    theta_at_definite_integral = math.sqrt(light_cylinder / semi_major) / gamma_definite_integral
    return {
        "gammaMax": gamma_max,
        "gammaLowerLimitTerm": lower_limit_term,
        "gammaDefiniteIntegralWithInitialOne": gamma_definite_integral,
        "physicallyRelativistic": gamma_max >= 1,
        "thetaAtGamma300": theta_at_300,
        "thetaAtComputedGamma": theta_at_computed_gamma,
        "thetaAtDefiniteIntegralGamma": theta_at_definite_integral,
        "smallAnglePredictionEstablished": gamma_definite_integral >= 100 and theta_at_definite_integral < 0.1,
        "minimumVariabilityTime": math.sqrt(1e-6) * semi_major / C,
    }


def accretion_reconnection() -> dict[str, float | bool]:
    delta_angle = 8.29e-5
    pair_inflow_over_c = delta_angle / math.pi
    proton_inflow_over_c = pair_inflow_over_c * (M_ELECTRON / M_PROTON)**0.25

    def normalized_energy(angle: float) -> float:
        efficiency = 0.5
        magnetic_field = 1e8
        stellar_radius = 1e4
        trigger_radius = 1e6
        central_mass = 10 * M_SOLAR
        flux = magnetic_field * math.pi * stellar_radius**2
        inflow = C * angle / math.pi * (M_ELECTRON / M_PROTON)**0.25
        sheet_thickness = trigger_radius * angle
        crossing_time = trigger_radius**1.5 / math.sqrt(2 * 6.67430e-11 * central_mass)
        return (
            efficiency * flux**2 * inflow
            / (16 * math.pi**2 * sheet_thickness * trigger_radius**3)
            * crossing_time
        )

    energy = normalized_energy(delta_angle)
    return {
        "pairInflowOverC": pair_inflow_over_c,
        "protonInflowOverC": proton_inflow_over_c,
        "printedPairApproximationOverC": 2.5e-6,
        "normalizedEnergyEstimateJ": energy,
        "claimedEnergyOverEstimate": 1.2e46 / energy,
        "energyWhenAngleHalvedRatio": normalized_energy(delta_angle / 2) / energy,
        "note": "Mechanical substitution into the printed Gaussian-style formula with SI numbers; not a validated SI energy.",
    }


def unit_and_profile_checks() -> dict[str, float | bool]:
    mu_zero = 4e-7 * math.pi
    virial_left = 0.5
    virial_right = 0.25
    return {
        "magneticPressureSiAtOneTesla": 1 / (2 * mu_zero),
        "magneticPressurePrintedAtOne": 1 / (8 * math.pi),
        "virialLeftAtTwoReferenceRadii": virial_left,
        "virialRightAtTwoReferenceRadii": virial_right,
        "virialIdentityValidAwayFromReferenceRadius": math.isclose(virial_left, virial_right),
        "strongShockDensityJump": 4.0,
        "strongShockTemperatureCoefficient": 3 / 16,
        "siUnitSystemClosed": False,
    }


def smbh_example() -> dict[str, float | bool]:
    mass = 1e7 * M_SOLAR
    neutron_star_binding = 0.1 * 1.4 * M_SOLAR * C**2 * 1e7
    rotational_energy = 0.1 * (0.05 * mass) * C**2 * 0.01 * 1e7
    jet_angle = math.radians(3)
    solid_angle = math.pi * jet_angle**2
    corrected_luminosity = rotational_energy / 10 * (4 * math.pi / solid_angle)
    return {
        "neutronStarBindingEnergyErgs": neutron_star_binding,
        "rotationalEnergyErgs": rotational_energy,
        "claimedEnergyOverRecomputed": 2.2e58 / rotational_energy,
        "solidAngleAtThreeDegrees": solid_angle,
        "correctedIsotropicLuminosity": corrected_luminosity,
        "correctedLowEfficiencyLuminosity": corrected_luminosity * 1e-4,
        "energyExtractionEfficiencyDerived": False,
    }


def agn_beaming_example() -> dict[str, float | bool]:
    total_luminosity = 1.26e47
    isotropic_luminosity = 1e48
    two_pi_ratio = 2 * total_luminosity / isotropic_luminosity
    opening_angle = math.acos(1 - two_pi_ratio)
    doppler = (isotropic_luminosity / total_luminosity)**(1 / 3)
    year_seconds = 365.25 * 86400
    solar_energy_ergs = M_SOLAR * C**2 * 1e7

    def lifetime(mass_in_solar_masses: float, eddington_ratio: float) -> float:
        mass_energy = mass_in_solar_masses * solar_energy_ergs
        eddington_luminosity = mass_in_solar_masses * 1.26e38
        return (0.1 / 0.9) * mass_energy / (eddington_ratio * eddington_luminosity) / year_seconds

    low_mass_lifetime = lifetime(1e6, 1.0)
    high_mass_lifetime = lifetime(1e10, 1.0)
    return {
        "twoPiSolidAngleRatio": two_pi_ratio,
        "exactOpeningAngle": opening_angle,
        "printedOpeningAngle": 0.54,
        "dopplerFromActualRatio": doppler,
        "lifetimePerInverseEddingtonRatioYears": low_mass_lifetime,
        "lifetimeMassRatio": high_mass_lifetime / low_mass_lifetime,
        "massAloneDeterminesLifetime": False,
    }


def jet_event_example() -> dict[str, float | bool]:
    c_cgs = 3e10
    gamma = 300.0
    variability = 0.01
    jet_angle = 0.1
    longitudinal_length = c_cgs * variability * gamma**2
    printed_length = 2.7e11
    printed_volume = 2.7e36
    power_from_written_formula = 0.1 * c_cgs / (4 * math.pi) * (1e8)**2 * printed_volume
    claimed_isotropic = 5.8e51
    implied_power = claimed_isotropic / 900
    return {
        "longitudinalLengthFromInputs": longitudinal_length,
        "printedLongitudinalLength": printed_length,
        "longitudinalLengthRatio": longitudinal_length / printed_length,
        "powerFromWrittenFormula": power_from_written_formula,
        "impliedPowerFromClaim": implied_power,
        "powerRatioOverImpliedClaim": power_from_written_formula / implied_power,
        "isotropicFromWrittenFormula": 900 * power_from_written_formula,
        "claimedIsotropic": claimed_isotropic,
        "angularVariabilityTime": (1e14 / c_cgs) * (8.29e-5)**2 / 2,
        "gammaTimesJetAngle": gamma * jet_angle,
        "powerUnitIsWatt": False,
        "observationalFitPerformed": False,
    }


def main() -> None:
    print(json.dumps({
        "schemaVersion": "eecc-grb-engine-checks/v1",
        "sourceIds": ["10298846404"],
        "rotationEngine": rotation_engine(),
        "beamingAndDuration": beaming_and_duration(),
        "lorentzAndVariability": lorentz_and_variability(),
        "accretionReconnection": accretion_reconnection(),
        "unitAndProfileChecks": unit_and_profile_checks(),
        "smbhExample": smbh_example(),
        "agnBeamingExample": agn_beaming_example(),
        "jetEventExample": jet_event_example(),
        "observationalFitPerformed": False,
        "evidenceUpgrade": False,
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
