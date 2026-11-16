#!/usr/bin/env python3
"""Checks for the displayed hydrogen boundary and Lyman-limit claims."""
from __future__ import annotations
import json

R_INFINITY = 10973731.568160


def boundary_check(epsilon, displayed_meters, a0=5.29177210903e-11):
    if not 0 <= epsilon < 1 or displayed_meters <= 0 or a0 <= 0:
        raise ValueError("Require 0<=epsilon<1 and positive displayed length and a0")
    direct = (1 - epsilon) * a0
    return {
        "directMeters": direct,
        "displayedOverDirect": displayed_meters / direct,
        "displayedOverA0": displayed_meters / a0,
    }


def lyman_limit(reduced_mass=True, electron_mass=9.1093837139e-31, proton_mass=1.67262192369e-27):
    if electron_mass <= 0 or proton_mass <= 0:
        raise ValueError("Particle masses must be positive")
    rydberg = R_INFINITY / (1 + electron_mass / proton_mass) if reduced_mass else R_INFINITY
    return {"rydbergPerMeter": rydberg, "lambdaNm": 1e9 / rydberg}


def main() -> None:
    print(json.dumps({
        "schemaVersion": "hydrogen-boundary-check/v1",
        "sourceId": "9565652215",
        "boundary": boundary_check(0.0014253345, 1.98607647e-6),
        "infiniteMassLymanLimit": lyman_limit(False),
        "reducedMassLymanLimit": lyman_limit(True),
        "claimedLambdaNm": 91.02,
        "hardElectronicConfinementEstablished": False,
        "newSpectralPredictionValidated": False,
        "evidenceUpgrade": False,
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
