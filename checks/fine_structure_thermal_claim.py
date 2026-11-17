#!/usr/bin/env python3
"""Algebraic checks for the displayed thermal fine-structure variation claim."""
from __future__ import annotations
import json
import math

K_B_EV_PER_K = 8.617333262145e-5
H_BINDING_EV = 13.6


def energy_alpha_relative(delta_e, e0):
    """Formal differential relation only; it does not establish that alpha varies thermally."""
    if e0 == 0:
        raise ValueError("Reference energy must be nonzero")
    return 0.5 * delta_e / e0


def thermal_alpha_coefficient(t0):
    if t0 <= 0:
        raise ValueError("Temperature must be positive")
    absolute = 3 * K_B_EV_PER_K * t0 / (4 * H_BINDING_EV)
    return {"absoluteCoefficient": absolute, "signedCoefficient": -absolute}


def energy_fluctuation_ratio(temperature, heat_capacity_ev_per_k, e0=H_BINDING_EV):
    if temperature <= 0 or heat_capacity_ev_per_k <= 0 or e0 == 0:
        raise ValueError("Require positive temperature and heat capacity and nonzero energy scale")
    sigma = math.sqrt(K_B_EV_PER_K * temperature**2 * heat_capacity_ev_per_k)
    return {"sigmaEnergyEV": sigma, "relativeFluctuation": sigma / abs(e0)}


def main() -> None:
    delta_e = 1.5 * K_B_EV_PER_K
    print(json.dumps({
        "schemaVersion": "fine-structure-thermal-check/v1",
        "sourceId": "9558649820",
        "oneKelvinFormalRelativeAlpha": energy_alpha_relative(delta_e, -H_BINDING_EV),
        "coefficientAt300K": thermal_alpha_coefficient(300.0),
        "displayedCoefficient": 1.43e-6,
        "illustrativeFluctuationAt300K": energy_fluctuation_ratio(300.0, 1.5 * K_B_EV_PER_K),
        "vacuumAlphaTemperatureDependenceEstablished": False,
        "thermalStateEnergyCanBeIdentifiedWithCouplingVariation": False,
        "evidenceUpgrade": False,
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
