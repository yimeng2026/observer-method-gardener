#!/usr/bin/env python3
"""Independent numerical and dimensional checks for the 2025-12-31 QG poster."""
from __future__ import annotations

import json
import math

C = 299792458.0
HBAR = 1.054571817e-34
EV_J = 1.602176634e-19
LAMBDA_C = 5.991529734e-13
THETA_M = 1.557695400
DELTA_THETA = 8.290000e-5
KAPPA = 7.254e-27
MPC_M = 3.0856775814913673e22
SECONDS_PER_YEAR = 365.25 * 86400
PROTON_MASS_DISPLAY = 1.672621898e-27


def qg_energy_scale() -> dict[str, float]:
    energy_j = HBAR * C / LAMBDA_C
    return {
        "J": energy_j,
        "MeV": energy_j / EV_J / 1e6,
        "TeV": energy_j / EV_J / 1e12,
    }


def gravitational_wave_suppression() -> float:
    return LAMBDA_C**2 * 100**2 / (2 * C**2) * (THETA_M / math.pi) ** 2


def proton_log10_lifetime_years() -> float:
    return (
        math.log10(LAMBDA_C / C)
        + math.pi / (2 * DELTA_THETA * math.log(10))
        - math.log10(SECONDS_PER_YEAR)
    )


def hubble_and_integral_factor() -> dict[str, float]:
    h0_si = C * KAPPA
    return {
        "h0SI": h0_si,
        "h0KmSPerMpc": h0_si * MPC_M / 1000,
        "integralFactor": 2 * math.pi**2 / math.sin(2 * THETA_M),
    }


def cosmological_constant_rate() -> float:
    h0_per_year = C * KAPPA * SECONDS_PER_YEAR
    return -3 * h0_per_year / (2 * math.pi) * math.sin(2 * THETA_M)


def dark_matter_mass() -> dict[str, float]:
    mass_kg = 499.7 * PROTON_MASS_DISPLAY
    return {
        "kg": mass_kg,
        "GeV": mass_kg * C**2 / EV_J / 1e9,
    }


def dimensional_findings() -> dict[str, object]:
    return {
        "kappaBaseDimension": "M^2 L^-4 T",
        "requiredIntegralFactorDimension": "M^-2 L^3 T^-1",
        "annihilationPrefactorDimension": "L^2",
        "annihilationRateDimensionallyClosed": False,
    }


def main() -> None:
    print(json.dumps({
        "schemaVersion": "year-end-qg-claim-checks/v1",
        "sourceIds": ["10353816276"],
        "energyScale": qg_energy_scale(),
        "gravitationalWaveSuppression": gravitational_wave_suppression(),
        "protonLog10LifetimeYears": proton_log10_lifetime_years(),
        "hubble": hubble_and_integral_factor(),
        "cosmologicalConstantRatePerYear": cosmological_constant_rate(),
        "darkMatterMass": dark_matter_mass(),
        "dimensions": dimensional_findings(),
        "evidenceUpgrade": False,
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
