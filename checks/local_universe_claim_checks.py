#!/usr/bin/env python3
"""Independent checks for the 2025-12-01 local-achievement post.

Table rounding consistency is not experimental validation.  All new-physics
claims remain separated from standard-model arithmetic and source artwork.
"""
from __future__ import annotations

import json
import math

HBAR = 1.054571817e-34
C = 299792458.0
G = 6.67430e-11
KB = 1.380649e-23
EV_JOULES = 1.602176634e-19
GEV_JOULES = 1.602176634e-10
ELECTRON_MASS = 9.1093837015e-31
PROTON_MASS = 1.67262192369e-27
LAMBDA_C = 5.99153e-13
THETA_M = 1.55769540


def dark_matter_mass() -> dict[str, float | bool]:
    mass = (
        HBAR / (C * LAMBDA_C) * 2 * math.pi**2
        / math.sqrt(1 + 3 * math.cos(THETA_M)**2)
    )
    ratio = mass / PROTON_MASS
    return {
        "massKg": mass,
        "claimedOverComputed": 8.35e-25 / mass,
        "computedOverClaimed": mass / 8.35e-25,
        "massOverProton": ratio,
        "claimedMassSupported": math.isclose(
            mass, 8.35e-25, rel_tol=1e-6, abs_tol=0.0
        ),
        "ratio500Supported": math.isclose(
            ratio, 500, rel_tol=1e-6, abs_tol=0.0
        ),
    }


def superconductor() -> dict[str, float | bool]:
    gap = (
        HBAR**2 / (2 * ELECTRON_MASS * LAMBDA_C**2)
        * (1 - math.cos(4 * THETA_M)) / math.sin(2 * THETA_M)
    )
    return {
        "gapJ": gap,
        "gapEv": gap / EV_JOULES,
        "gapMev": gap / EV_JOULES * 1000,
        "tcDirectK": gap / KB,
        "tcBcsK": gap / (1.76 * KB),
        "roomTemperatureSupported": False,
    }


def dark_energy() -> dict[str, float | bool]:
    w = -0.999999999969
    mass_bound_kg = 1e-33 * EV_JOULES / C**2
    return {
        "wOutsideBy": w - (-1),
        "wWithinPrintedInterval": -1.06 <= w <= -1.0,
        "massBoundSatisfied": 7.46e-73 < mass_bound_kg,
        "rhoRelativePercent": abs(5.96 - 6.0) / 6.0 * 100,
    }


def top_quark() -> dict[str, float | bool]:
    y33 = math.cos(THETA_M / 2) / 2
    return {
        "y33": y33,
        "computedMtGev": y33 * 246.2 / math.sqrt(2),
        "mtUsingPrintedCoefficient": 0.995 * 246.2 / math.sqrt(2),
        "printedCoefficientSupported": math.isclose(
            y33, 0.995, rel_tol=1e-6, abs_tol=0.0
        ),
    }


def electroweak() -> dict[str, float | bool]:
    mw = 0.5 * 0.652 * 246.2
    mz = 0.5 * math.sqrt(0.357**2 + 0.652**2) * 246.2
    return {
        "mwGev": mw,
        "mzGev": mz,
        "standardArithmeticBroadlyMatches": (
            abs(mw - 80.379) / 80.379 < 0.01
            and abs(mz - 91.1876) / 91.1876 < 0.005
        ),
    }


def gravitational_wave() -> dict[str, float | bool]:
    dispersion = THETA_M**2 / (4 * math.pi**2) * (100 * LAMBDA_C / C)**2
    return {
        "relativeDispersionAt100Hz": dispersion,
        "printedDispersionSupported": math.isclose(
            dispersion, 1e-21, rel_tol=1e-9, abs_tol=0.0
        ),
        "peakFrequencyDerived": False,
        "actualSignalAnalyzed": False,
    }


def energy_balance() -> dict[str, float | bool]:
    mass = 1e53
    radius = 4.41e26
    gravitational = -0.6 * G * mass**2 / radius
    rest = mass * C**2
    ratio = abs(gravitational) / rest
    return {
        "gravitationalEnergyJ": gravitational,
        "restEnergyJ": rest,
        "absoluteGravityOverRest": ratio,
        "orderUnityBalanceSupported": math.isclose(
            ratio, 1, rel_tol=0.1, abs_tol=0.0
        ),
        "radiusVersionFrozen": False,
    }


def error_table() -> dict[str, list[dict[str, float | str]] | bool]:
    definitions = [
        ("ns", 0.965, 0.9649, 0.01, 0.005),
        ("H0", 67.36, 67.4, 0.06, 0.005),
        ("age", 13.76, 13.787, 0.2, 0.05),
        ("Omega", 0.685, 0.6847, 0.04, 0.005),
        ("abund", 0.119, 0.1200, 0.8, 0.05),
        ("mg", 499.97, 500, 0.006, 0.0005),
        ("rho", 5.96, 6.0, 0.7, 0.05),
        ("electron", 0.5110, 0.510999, 0.0002, 0.00005),
        ("top", 173.2, 172.76, 0.25, 0.005),
        ("higgs", 125.1, 125.25, 0.12, 0.005),
    ]
    rows = [
        {
            "name": name,
            "computedPercent": abs(theory - observed) / observed * 100,
            "printedPercent": printed,
            "roundingTolerance": tolerance,
        }
        for name, theory, observed, printed, tolerance in definitions
    ]
    return {
        "rows": rows,
        "roundingConsistent": all(
            abs(row["computedPercent"] - row["printedPercent"])
            <= row["roundingTolerance"]
            for row in rows
        ),
        "independentPredictionProven": False,
    }


def casimir() -> dict[str, float | bool]:
    coefficient = -math.pi**2 / 720 + THETA_M**2 / (4 * math.pi**2)
    return {
        "coefficient": coefficient,
        "energyExtractionValidated": False,
    }


def evidence_boundaries() -> dict[str, bool]:
    return {
        "rawDatasetsProvided": False,
        "onlyTwoParameters": False,
        "independentPeerReviewProvided": False,
        "awardsOrOfficialAppointmentsProvided": False,
        "bookCoverIsScientificEvidence": False,
        "simulatedInstitutionalReportsAreOfficial": False,
    }


def main() -> None:
    print(json.dumps({
        "schemaVersion": "local-universe-claim-checks/v1",
        "sourceIds": ["10260231053"],
        "darkMatterMass": dark_matter_mass(),
        "superconductor": superconductor(),
        "darkEnergy": dark_energy(),
        "topQuark": top_quark(),
        "electroweak": electroweak(),
        "gravitationalWave": gravitational_wave(),
        "energyBalance": energy_balance(),
        "errorTable": error_table(),
        "casimir": casimir(),
        "evidenceBoundaries": evidence_boundaries(),
        "evidenceUpgrade": False,
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
