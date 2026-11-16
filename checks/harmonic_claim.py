#!/usr/bin/env python3
"""Exact-sum checks for the public harmonic approximation and zeta(1) claim."""
from __future__ import annotations
import json
import math

EULER_GAMMA = 0.5772156649015329


def exact_harmonic(n: int) -> float:
    return sum(1.0 / k for k in range(1, n + 1))


def proposed_harmonic(n: int) -> float:
    coefficient = (1 - EULER_GAMMA) / 2 - 1 / 12
    return EULER_GAMMA + math.log(n + 1) - 1 / (2 * n + 2 * EULER_GAMMA) + coefficient / n**2


def expansion_coefficients() -> dict:
    gamma = EULER_GAMMA
    return {
        "inverseN": 1.0 - 0.5,
        "inverseNSquared": -0.5 + gamma / 2 + (1 - gamma) / 2 - 1 / 12,
        "inverseNCubedFromDisplayedTerms": 1 / 3 - gamma**2 / 2,
        "standardInverseNCubed": 0.0,
    }


def harmonic_errors(inputs: list[int]) -> list[dict]:
    return [{
        "n": n,
        "exact": exact_harmonic(n),
        "proposed": proposed_harmonic(n),
        "absoluteError": abs(proposed_harmonic(n) - exact_harmonic(n)),
        "zeta1HasFiniteValue": False,
    } for n in inputs]


def main() -> None:
    print(json.dumps({
        "schemaVersion": "harmonic-claim-arithmetic/v1",
        "sourceIds": ["9581109556", "9581079063"],
        "expansionCoefficients": expansion_coefficients(),
        "samples": harmonic_errors([1, 10, 100, 1000, 10000]),
        "scope": "Exact finite-sum and expansion arithmetic only; no novelty claim or finite zeta(1) value is validated.",
        "evidenceUpgrade": False,
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
