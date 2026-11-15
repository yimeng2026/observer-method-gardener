#!/usr/bin/env python3
"""Unit and arithmetic checks for fermion-mass and superconductivity claims."""
from __future__ import annotations
import json
import math

ELEMENTARY_CHARGE_C = 1.602176634e-19
BOLTZMANN_J_PER_K = 1.380649e-23
KB_EV_PER_K = BOLTZMANN_J_PER_K / ELEMENTARY_CHARGE_C


def audit_parameter_superconductor(energy_ev: float = 0.0200, theta: float = 0.11, length_ratio: float = 1000.0) -> dict:
    energy_ev = float(energy_ev)
    theta = float(theta)
    length_ratio = float(length_ratio)
    if not math.isfinite(energy_ev) or energy_ev <= 0:
        raise ValueError("energy_ev must be finite and positive")
    if not math.isfinite(theta) or theta < 0:
        raise ValueError("theta must be finite and nonnegative")
    if not math.isfinite(length_ratio) or length_ratio <= 1:
        raise ValueError("length_ratio must be finite and greater than one")
    theory_gev = [8.6e-9, 1.27e-8, 5.0e-5]
    theory_ev = [value * 1e9 for value in theory_gev]
    common_ev_scale = [0.0086, 0.0127, 0.05]
    # The square-root factor in the public expression cannot exceed one for a real T0/Tc ratio.
    upper_k = energy_ev * theta**2 / (2 * math.pi) / (1 + math.log(length_ratio)) / KB_EV_PER_K
    return {
        "schemaVersion": "parameter-superconductor-arithmetic/v1",
        "sourceIds": ["10688719651", "10751880300"],
        "sourceLocators": ["10688719651/01.jpg", "10751880300/04.jpg"],
        "neutrinoTheoryGeV": theory_gev,
        "neutrinoTheoryEV": theory_ev,
        "commonEVScale": common_ev_scale,
        "factorAboveCommonMillielectronvoltScale": [value / reference for value, reference in zip(theory_ev, common_ev_scale)],
        "superconductorInputs": {"energyEV": energy_ev, "theta": theta, "lengthRatio": length_ratio, "maximumRootFactor": 1.0},
        "superconductorUpperK": upper_k,
        "publishedTemperatureK": 90.0,
        "publishedUpperK": 91.0,
        "superconductorUpperBelowClaimed90K": upper_k < 90.0,
        "scope": "Unit conversion and an upper bound of the displayed formula only; no particle or superconductivity model is validated.",
        "evidenceUpgrade": False,
    }


def main() -> None:
    print(json.dumps(audit_parameter_superconductor(), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
