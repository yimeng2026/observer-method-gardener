#!/usr/bin/env python3
"""Arithmetic checks for engineering claims embedded in post 10377346752."""
from __future__ import annotations
import json
import math


def fusion_gain(input_powers_mw: list[float], fusion_output_mw: float) -> float:
    return fusion_output_mw / sum(input_powers_mw)


def casimir_energy_density_magnitude(distance_m: float) -> float:
    """Evaluate the displayed positive prefactor pi^2*hbar*c/(480*d^4)."""
    hbar = 1.054571817e-34
    c = 299792458.0
    return math.pi**2 * hbar * c / (480 * distance_m**4)


def audit_engineering() -> dict:
    gain = fusion_gain([10.0, 5.0, 5.0], 1200.0)
    casimir = casimir_energy_density_magnitude(1e-9)
    return {
        "schemaVersion": "six-force-engineering-arithmetic/v1",
        "sourceId": "10377346752",
        "sourceLocators": ["comment-floor-20", "111.jpg"],
        "fusionInputMW": 20.0,
        "fusionOutputMW": 1200.0,
        "fusionGainFromDisplayedNumbers": gain,
        "matchesDisplayedApproximateGain100": math.isclose(gain, 100.0),
        "casimirDistanceM": 1e-9,
        "casimirEnergyDensityMagnitudeJPerM3": casimir,
        "matchesDisplayedOneKJPerM3": math.isclose(casimir, 1000.0, rel_tol=0.01),
        "scope": "Arithmetic only; no fusion, vacuum-energy, superconductivity or engineering feasibility is validated.",
        "evidenceUpgrade": False,
    }


def main() -> None:
    print(json.dumps(audit_engineering(), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
