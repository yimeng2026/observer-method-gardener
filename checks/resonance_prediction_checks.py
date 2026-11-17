#!/usr/bin/env python3
"""Independent arithmetic checks for the 2025-12-29 resonance-prediction post."""
from __future__ import annotations

import json
import math

C = 299792458.0
HBAR = 1.054571817e-34
HBAR_GEV_S = 6.582119569e-25
EV_J = 1.602176634e-19
KG_PER_GEV = 1.782661921e-27
LAMBDA_C = 5.99153e-13
THETA_M = 1.55769540
DELTA_THETA = 8.29e-5
Z0 = 0.0147
M_G_GEV = 4293.0
KAPPA_GEV_INV = 5.24e-4
PROTON_MASS_KG = 1.672621898e-27


def mass_and_dark_energy() -> dict[str, float]:
    base_mev = HBAR * C / LAMBDA_C / EV_J / 1e6
    predicted_mev = base_mev * Z0**(-1 / 3) * (DELTA_THETA / math.pi)**(-1 / 4)
    return {
        "baseMeV": base_mev,
        "predictedMeV": predicted_mev,
        "predictedTeV": predicted_mev / 1e6,
        "targetToPredictedMassRatio": 4293e3 / predicted_mev,
        "deltaThetaLogSensitivity": -1 / 4,
        "oneMilliEvKg": 1e-3 * EV_J / C**2,
        "displayedKgInEv": 1e-69 * C**2 / EV_J,
    }


def width_coupling_and_lifetime() -> dict[str, float]:
    return {
        "chosenKappa": KAPPA_GEV_INV,
        "widthGeV": KAPPA_GEV_INV**2 * M_G_GEV**3 / (80 * math.pi),
        "lifetimeSecondsAt87GeV": HBAR_GEV_S / 87,
        "kappaFromDisplayedFactors": (
            0.09 / (math.sqrt(2 * math.pi) * 1.22e19) * 2.91e22
        ),
    }


def mass_ratios() -> dict[str, float]:
    dark_matter_gev = 499.7 * PROTON_MASS_KG * C**2 / EV_J / 1e9
    mass_over_8p6 = M_G_GEV / 8.6
    return {
        "proton": M_G_GEV / 0.938272081,
        "electron": M_G_GEV / 0.000510998946,
        "darkMatter": M_G_GEV / dark_matter_gev,
        "massOver8p6GeV": mass_over_8p6,
        "massOver8p6RelativeDifference": abs(mass_over_8p6 - dark_matter_gev) / dark_matter_gev,
        "graviton": M_G_GEV * KG_PER_GEV / 1.1e-68,
        "planck": M_G_GEV / 1.22e19,
    }


def mixing_angle() -> dict[str, float]:
    eta = math.atan(Z0 * (DELTA_THETA / math.pi)**0.25)
    return {
        "radians": eta,
        "degrees": math.degrees(eta),
        "cosSquared": math.cos(eta)**2,
        "sinSquared": math.sin(eta)**2,
    }


def shell_geometry() -> dict[str, float | bool]:
    r5_over_lambda = 1 / (2 * math.pi)
    lower = 100.0
    return {
        "r5Meters": LAMBDA_C * r5_over_lambda,
        "r5OverLambda": r5_over_lambda,
        "shell5LowerOverLambda": lower,
        "shell5UpperOverLambda": r5_over_lambda,
        "shell5Nonempty": lower <= r5_over_lambda,
    }


def collider_yields() -> dict[str, float]:
    return {
        "run2": 1.7 * 140,
        "run3": 1.7 * 300,
        "gg300": 1.04 * 300,
        "tt300": 0.37 * 300,
        "zh300": 0.15 * 300,
        "gamma300": 0.017 * 300,
        "heConstantCrossSection": 1.7 * 15000,
        "heAdvertisedTimesFour": 1.7 * 15000 * 4,
        "fccConstantCrossSection": 1.7 * 30000,
        "fccAdvertisedTimesTwenty": 1.7 * 30000 * 20,
    }


def evidence_counts() -> dict[str, int | bool]:
    category_total = sum([47, 62, 89, 24, 156, 38])
    error_bin_total = sum([128, 241, 47])
    return {
        "categoryTotal": category_total,
        "errorBinTotal": error_bin_total,
        "newParticlePrecisionTotal": sum([18, 47, 63]),
        "newParticleTimingTotal": sum([42, 57, 29]),
        "claimedMaximumInsideErrorBins": 3.2e-3 <= 1e-3,
    }


def branching_and_spectrum() -> dict[str, float | bool]:
    actual_ratio = 13.02 / 4.293
    target_ratio = 1 + math.pi / THETA_M
    return {
        "branchingSum": sum([0.61, 0.22, 0.09, 0.04, 0.02, 0.01, 0.005, 0.005]),
        "ggCrossSection": 1.7 * 0.61,
        "ttCrossSection": 1.7 * 0.22,
        "zhCrossSection": 1.7 * 0.09,
        "gammaCrossSection": 1.7 * 0.01,
        "actualMassRatio": actual_ratio,
        "targetMassRatio": target_ratio,
        "actualWithinDisplayedTolerance": abs(actual_ratio - target_ratio) <= 0.002,
    }


def main() -> None:
    print(json.dumps({
        "schemaVersion": "resonance-prediction-checks/v1",
        "sourceIds": ["10345955013"],
        "massAndDarkEnergy": mass_and_dark_energy(),
        "widthCouplingAndLifetime": width_coupling_and_lifetime(),
        "massRatios": mass_ratios(),
        "mixingAngle": mixing_angle(),
        "shellGeometry": shell_geometry(),
        "colliderYields": collider_yields(),
        "evidenceCounts": evidence_counts(),
        "branchingAndSpectrum": branching_and_spectrum(),
        "evidenceUpgrade": False,
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
