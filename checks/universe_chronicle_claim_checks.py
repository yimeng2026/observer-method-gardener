#!/usr/bin/env python3
"""Checks for the 2025-12-02 universe chronicle post.

Correct local arithmetic is retained without validating the larger theory.
Masses are converted to GeV/c^2 using E=mc^2 throughout.
"""
from __future__ import annotations

import json
import math

HBAR = 1.054571817e-34
C = 299792458.0
G = 6.67430e-11
KB = 1.380649e-23
SOLAR_MASS = 1.98847e30
YEAR_SECONDS = 365.25 * 86400
GEV_JOULES = 1.602176634e-10
MPC_METRES = 3.0856775814913673e22
LAMBDA_C = 5.99153e-13
THETA_M = 1.55769540


def cosmology() -> dict[str, float | bool]:
    h0 = 67.36 * 1000 / MPC_METRES
    h_infinity = h0 * math.sqrt(0.685)
    return {
        "printedAgeYears": 13.76 * 1e8,
        "correctedAgeYears": 137.6 * 1e8,
        "correctionFactor": 10.0,
        "printedAgeSupported": False,
        "hInfinity": h_infinity,
        "hInfinityArithmeticMatches": math.isclose(
            h_infinity, 1.80e-18, rel_tol=0.004, abs_tol=0.0
        ),
        "torusDeSitterSignCompatible": False,
    }


def black_hole() -> dict[str, float | bool]:
    mass = 1e9 * SOLAR_MASS
    temperature = HBAR * C**3 / (8 * math.pi * G * mass * KB)
    seconds = 5120 * math.pi * G**2 * mass**3 / (HBAR * C**4)
    years = seconds / YEAR_SECONDS
    return {
        "temperatureK": temperature,
        "evaporationYears": years,
        "claimedTemperatureSupported": math.isclose(
            temperature, 1e-14, rel_tol=1e-9, abs_tol=0.0
        ),
        "claimedEvaporationSupported": math.isclose(
            years, 1e87, rel_tol=1e-9, abs_tol=0.0
        ),
    }


def yang_mills_gap() -> dict[str, float | bool]:
    base_gev = HBAR * C / LAMBDA_C / GEV_JOULES
    factor = min(
        math.sin(THETA_M),
        math.sqrt(1 - math.cos(2 * THETA_M)**2),
    )
    delta_gev = base_gev * factor
    return {
        "baseGev": base_gev,
        "factor": factor,
        "deltaGev": delta_gev,
        "deltaKev": delta_gev * 1e6,
        "claimedGapOverComputed": 80 / delta_gev,
        "claimed80GevSupported": math.isclose(
            delta_gev, 80, rel_tol=1e-9, abs_tol=0.0
        ),
        "nonperturbativeMassGapProof": False,
    }


def w_boson_formula() -> dict[str, float | bool]:
    coupling = math.sqrt(0.426)
    angular_factor = math.sqrt(
        math.sin(2 * THETA_M)**2 / (math.pi * math.cos(THETA_M))
    )
    mass_kg = coupling * HBAR / (2 * LAMBDA_C) * angular_factor
    mass_gev = mass_kg * C**2 / GEV_JOULES
    return {
        "massKg": mass_kg,
        "massGev": mass_gev,
        "computedOverClaimed": mass_gev / 80.379,
        "claimedMassSupported": math.isclose(
            mass_gev, 80.379, rel_tol=1e-9, abs_tol=0.0
        ),
        "onlyTwoParameters": False,
    }


def navier_stokes() -> dict[str, float | bool]:
    omega = C / LAMBDA_C / 70
    gradient_percent = 0.000005 / (1 / 70) * 100
    ck_percent = (2 / 3) * gradient_percent
    return {
        "omegaMax": omega,
        "omegaArithmeticMatches": math.isclose(
            omega, 7.15e18, rel_tol=0.001, abs_tol=0.0
        ),
        "dimensionless75MappingDerived": False,
        "gradientRelativePercent": gradient_percent,
        "ckRelativePercent": ck_percent,
        "uncertaintyPropagationMatches": (
            math.isclose(gradient_percent, 0.035, rel_tol=1e-9)
            and math.isclose(ck_percent, 7 / 300, rel_tol=1e-9)
        ),
        "classicalGlobalRegularityProven": False,
        "rawSimulationDataProvided": False,
    }


def cramer_claim() -> dict[str, float | bool]:
    sin_squared = math.sin(2 * THETA_M)**2
    cos_squared = math.cos(2 * THETA_M)**2
    c_sin = 4 / (math.pi * sin_squared)
    c_cos = 4 / (math.pi * cos_squared)
    return {
        "sinSquared": sin_squared,
        "cosSquared": cos_squared,
        "cUsingPrintedSin": c_sin,
        "cUsingCos": c_cos,
        "printedSinSupported": math.isclose(
            sin_squared, 0.9993, rel_tol=1e-3, abs_tol=0.0
        ),
        "claimedCUsingPrintedFormulaSupported": math.isclose(
            c_sin, 1.274, rel_tol=0.01, abs_tol=0.0
        ),
        "conjectureProven": False,
    }


def skewes_formula() -> dict[str, float | bool]:
    exponent = 2 * math.pi / (math.sin(THETA_M) * LAMBDA_C)
    proposed_log10 = exponent / math.log(10)
    published_log10 = 727.95133 / math.log(10)
    coefficient = 10**(published_log10 - 316)
    return {
        "proposedExponent": exponent,
        "proposedLog10": proposed_log10,
        "publishedLog10": published_log10,
        "publishedCoefficient": coefficient,
        "publishedConversionMatches": math.isclose(
            coefficient, 1.397, rel_tol=0.001, abs_tol=0.0
        ),
        "dimensionallyClosed": False,
        "proposedBoundMatchesPublished": math.isclose(
            proposed_log10, published_log10, rel_tol=0.01, abs_tol=0.0
        ),
    }


def evidence_boundaries() -> dict[str, bool]:
    return {
        "selfCorrectionRecorded": True,
        "completedBookProvided": False,
        "rawDatasetsProvided": False,
        "axiomaticYangMillsConstruction": False,
        "classicalNavierStokesProof": False,
        "onlyTwoParameters": False,
        "prizeRecognitionProvided": False,
    }


def main() -> None:
    print(json.dumps({
        "schemaVersion": "universe-chronicle-claim-checks/v1",
        "sourceIds": ["10262962220"],
        "cosmology": cosmology(),
        "blackHole": black_hole(),
        "yangMillsGap": yang_mills_gap(),
        "wBosonFormula": w_boson_formula(),
        "navierStokes": navier_stokes(),
        "cramerClaim": cramer_claim(),
        "skewesFormula": skewes_formula(),
        "evidenceBoundaries": evidence_boundaries(),
        "evidenceUpgrade": False,
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
