#!/usr/bin/env python3
"""Independent checks for the 2025-12-13 EEBH parameter-table post.

All displayed values are treated as claims, not observations.  Physical
constants are used only for independent arithmetic and standard baselines.
"""
from __future__ import annotations

import json
import math

C = 299792458.0
G = 6.67430e-11
M_SOLAR = 1.98847e30
YEAR_SECONDS = 365.25 * 86400
AU = 1.495978707e11


def m87_table() -> dict[str, float]:
    mass = 6.5e9 * M_SOLAR
    ellipsoid_mass = 0.05 * mass
    rs = 1.92e13
    a, b, c = 8.73e11, 7.16e11, 1.84e6
    volume = 4 * math.pi * a * b * c / 3
    angular_momentum = 0.9 * G * mass**2 / C
    inertia = 0.5 * ellipsoid_mass * a**2
    amplification = (a / b)**2 * math.sqrt(a / c) * 5.0**2
    return {
        "aOverGravitationalRadius": a / (rs / 2),
        "volume": volume,
        "displayedVolume": 2.29e36,
        "density": ellipsoid_mass / volume,
        "displayedDensity": 2.82e7,
        "densityFromDisplayedVolume": ellipsoid_mass / 2.29e36,
        "gammaFromSpeed": 1 / math.sqrt(1 - 0.98**2),
        "rotationPeriodHours": 2 * math.pi / (0.98 * C / a) / 3600,
        "angularMomentum": angular_momentum,
        "displayedJ": 8.43e69,
        "coreAngularMomentum": 0.05**2 * angular_momentum,
        "inertia": inertia,
        "displayedInertia": 2.47e65,
        "amplification": amplification,
        "torque": 1.07e47 * 2.57e4,
        "torqueOverDisplayedJ": 2.75e51 / 8.43e69,
        "periodFromDisplayedOmegaYears": 2 * math.pi / 2.19e-8 / YEAR_SECONDS,
        "betaFromFormula": 2.75e51 * (2.89 * YEAR_SECONDS) / (4 * math.pi**2 * 2.47e65),
    }


def sgr_a_table() -> dict[str, float]:
    mass = 4.30e6 * M_SOLAR
    ellipsoid_mass = 0.05 * mass
    rs = 1.27e10
    a, b, c = 5.67e8, 4.65e8, 1.43e3
    volume = 4 * math.pi * a * b * c / 3
    angular_momentum = 0.5 * G * mass**2 / C
    amplification = (a / b)**2 * math.sqrt(a / c) * 1.4**2
    return {
        "aOverGravitationalRadius": a / (rs / 2),
        "volume": volume,
        "displayedVolume": 6.29e26,
        "density": ellipsoid_mass / volume,
        "displayedDensity": 1.14e12,
        "densityFromDisplayedVolume": ellipsoid_mass / 6.29e26,
        "gammaFromSpeed": 1 / math.sqrt(1 - 0.70**2),
        "rotationPeriodHours": 2 * math.pi / (0.70 * C / a) / 3600,
        "angularMomentum": angular_momentum,
        "displayedJ": 4.01e58,
        "displayedJOverPhysical": 4.01e58 / angular_momentum,
        "amplification": amplification,
        "torque": 4.35e31 * 3.84e2,
        "torqueOverDisplayedJ": 1.67e34 / 4.01e58,
        "periodFromDisplayedOmegaYears": 2 * math.pi / 2.62e-11 / YEAR_SECONDS,
    }


def quadrupole_and_shadow() -> dict[str, float]:
    m87_ratio = 8.73e11 / 1.92e13
    m87_zeta = 1.84e6 / 8.73e11
    sgr_ratio = 5.67e8 / 1.27e10
    sgr_zeta = 1.43e3 / 5.67e8
    return {
        "m87J2FromEarlierFormula": (m87_zeta**2 - m87_ratio**2) / 5,
        "sgrJ2FromEarlierFormula": (sgr_zeta**2 - sgr_ratio**2) / 5,
        "sgrJ2FromLaterFormula": -(3 / 5) * sgr_ratio**2 * (1 - sgr_zeta**2),
        "displayedM87J2": -1.00,
        "displayedSgrJ2": -0.785,
        "sgrShadowFormulaValue": 1 - 0.75 * (1 - (-0.785)),
        "sgrEpsilonFromCOverA": 1 + 0.5 * (1 - sgr_zeta),
    }


def s02_orbit() -> dict[str, float | bool]:
    semimajor = 970 * AU
    eccentricity = 0.880
    rs = 1.27e10
    quadrupole = -0.785
    gr_radians = 3 * math.pi * rs / (semimajor * (1 - eccentricity**2))
    correction_ratio = quadrupole * rs / (semimajor * (1 - eccentricity**2))
    return {
        "grRadians": gr_radians,
        "grDegrees": math.degrees(gr_radians),
        "displayedGrDegrees": 0.2818,
        "j2CorrectionRatio": correction_ratio,
        "totalFromPrintedFormulas": math.degrees(gr_radians * (1 + correction_ratio)),
        "thirtySixPercentSupported": math.isclose(abs(correction_ratio), 0.36, rel_tol=0.01),
        "observedPrecessionDegrees": 0.176,
        "observedUncertaintyDegrees": 0.015,
        "displayedTotalDegrees": 0.1804,
    }


def model_statistics() -> dict[str, float | bool]:
    return {
        "kerrNewtonLogRatio": -48.3 - (-90.1),
        "eebhNewtonLogRatio": -30.1 - (-90.1),
        "kerrNewtonExpectedRatio": math.exp(41.8),
        "eebhNewtonExpectedRatio": math.exp(60.0),
        "kerrNewtonDisplayedRatio": 2.3e18,
        "eebhNewtonDisplayedRatio": 6.7e25,
        "parameterCountsAndLikelihoodProvided": False,
    }


def gw_phase() -> dict[str, float | bool]:
    m1, m2 = 36 * M_SOLAR, 29 * M_SOLAR
    total_mass = m1 + m2
    symmetric_mass_ratio = m2 / total_mass
    lambda_c = 5.99e-13
    frequency = 150.0
    x = G * total_mass * math.pi * frequency / C**3

    def schwarzschild_radius(mass: float) -> float:
        return 2 * G * mass / C**2

    weighted_terms = 0.05 * (
        (lambda_c / schwarzschild_radius(m1))**2
        + (lambda_c / schwarzschild_radius(m2))**2
    )
    phase = 3 / (128 * symmetric_mass_ratio) * x**-1 * weighted_terms
    return {
        "frequencyExponentAfterCancellation": -5 / 3 + 2 / 3,
        "phase": phase,
        "claimedPhaseOverComputed": 12 / phase,
        "snrMismatchProduct": 24 * 0.2,
        "mismatchDerivedFromWaveform": False,
    }


def field_equation_boundary() -> dict[str, bool]:
    return {
        "bianchiClosureShown": False,
        "exactSolutionProvided": False,
        "observationalFitPerformed": False,
        "evidenceUpgrade": False,
    }


def main() -> None:
    print(json.dumps({
        "schemaVersion": "eebh-parameter-table-checks/v1",
        "sourceIds": ["10296425024"],
        "m87Table": m87_table(),
        "sgrATable": sgr_a_table(),
        "quadrupoleAndShadow": quadrupole_and_shadow(),
        "s02Orbit": s02_orbit(),
        "modelStatistics": model_statistics(),
        "gwPhase": gw_phase(),
        "fieldEquationBoundary": field_equation_boundary(),
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
