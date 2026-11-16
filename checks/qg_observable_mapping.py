#!/usr/bin/env python3
"""Minimal identifiability and limiting-expression checks for post 10416993115.

These functions transcribe selected public formulas for arithmetic review only.
They do not implement or validate a five-dimensional physical theory.
"""
from __future__ import annotations
import json
import math


def pressure_correction(n: float, radius: float, wavelength: float, cos_theta_y: float = 1.0) -> float:
    """Return the squared correction in the displayed pressure expression."""
    return (n * wavelength / (2 * math.pi * radius * cos_theta_y)) ** 2


def snell_lhs(index: float, theta: float, radius: float, wavelength: float) -> float:
    """Return the displayed modified-Snell left-hand side."""
    return index * math.sin(theta) * (1 + wavelength / (2 * math.pi * radius * math.cos(theta)))


def dark_matter_ratio(beta: float, galaxy_age_yr: float) -> float:
    """Transcribe the displayed scaling M_DM/M_bar = 0.1 (beta/1e-12)(t/1e10 yr)."""
    return 0.1 * (beta / 1e-12) * (galaxy_age_yr / 1e10)


def audit_mapping() -> dict:
    reference = pressure_correction(n=2.0, radius=1e-6, wavelength=5e-7)
    rescaled = pressure_correction(n=4.0, radius=2e-6, wavelength=5e-7)
    return {
        "schemaVersion": "qg-observable-mapping-arithmetic/v1",
        "sourceId": "10416993115",
        "sourceLocators": ["12.jpg", "22.jpg", "44.jpg", "45.jpg"],
        "pressureReferenceCorrection": reference,
        "pressureRescaledCorrection": rescaled,
        "pressureInvariantUnderJointNAndRadiusRescaling": reference == rescaled,
        "identifiablePressureCombination": "n/(R*cos(theta_y)) for fixed wavelength",
        "snellInfiniteRadiusLimitRecovered": math.isclose(
            snell_lhs(1.5, math.pi / 6, math.inf, 5e-7), 0.75, rel_tol=0.0, abs_tol=1e-15
        ),
        "betaRequiredForDisplayedRatioFiveAtReferenceAge": 50e-12,
        "scope": "Arithmetic and parameter identifiability only; no dynamics, data fit or physical claim is validated.",
        "evidenceUpgrade": False,
    }


def main() -> None:
    print(json.dumps(audit_mapping(), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
