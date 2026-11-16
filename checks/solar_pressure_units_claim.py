#!/usr/bin/env python3
"""SI/Gaussian checks for the displayed solar pressure correction."""
from __future__ import annotations
import json
import math

K_B = 1.380649e-23
M_H = 1.6735575e-27
SIGMA = 5.670374419e-8
C = 299792458.0
RADIATION_A = 4 * SIGMA / C
MU0 = 4 * math.pi * 1e-7


def pressure_components(rho, temperature, mean_mu, magnetic_tesla):
    """Illustrative SI scalar-pressure sum; not a validated solar-atmosphere model."""
    if rho <= 0 or temperature <= 0 or mean_mu <= 0:
        raise ValueError("Density, temperature and mean particle mass factor must be positive")
    gas = rho * K_B * temperature / (mean_mu * M_H)
    radiation = RADIATION_A * temperature**4 / 3
    magnetic = magnetic_tesla**2 / (2 * MU0)
    return {
        "gasPa": gas,
        "radiationPa": radiation,
        "magneticPa": magnetic,
        "totalSI": gas + radiation + magnetic,
        "radiationConstantSI": RADIATION_A,
    }


def magnetic_gaussian_pa(magnetic_gauss):
    """B_G^2/(8 pi) in Ba, converted to Pa with 1 Ba=0.1 Pa."""
    return magnetic_gauss**2 / (8 * math.pi) * 0.1


def naive_gaussian_with_tesla(magnetic_tesla):
    """Numerically expose the invalid insertion of tesla into the Gaussian formula."""
    return magnetic_tesla**2 / (8 * math.pi)


def main() -> None:
    result = pressure_components(1e-7, 5778.0, 0.6, 0.01)
    print(json.dumps({
        "schemaVersion": "solar-pressure-units-check/v1",
        "sourceId": "9567979465",
        "illustrativeInputs": {"rhoKgM3": 1e-7, "temperatureK": 5778.0, "meanMu": 0.6, "magneticTesla": 0.01},
        **result,
        "magneticFrom100GaussPa": magnetic_gaussian_pa(100.0),
        "naiveTeslaInGaussianFormula": naive_gaussian_with_tesla(0.01),
        "displayedFormulaHasDeclaredConsistentUnits": False,
        "solarAtmosphereModelValidated": False,
        "evidenceUpgrade": False,
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
