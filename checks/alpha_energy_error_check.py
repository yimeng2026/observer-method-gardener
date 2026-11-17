#!/usr/bin/env python3
"""Separate relativistic kinetic correction from 1/137-vs-alpha rounding error."""
from __future__ import annotations

import json

import mpmath as mp

ALPHA_CODATA_2022 = "0.0072973525643"


def kinetic_relative_correction(beta) -> mp.mpf:
    """(K_relativistic-K_nonrelativistic)/K_nonrelativistic for the same mass."""
    with mp.workdps(60):
        beta = mp.mpf(beta)
        if not 0 < beta < 1:
            raise ValueError("beta must be between zero and one")
        nonrelativistic = beta**2 / 2
        relativistic = 1 / mp.sqrt(1 - beta**2) - 1
        return (relativistic - nonrelativistic) / nonrelativistic


def reciprocal_137_errors() -> dict[str, mp.mpf]:
    """Compare the rounded 1/137 value against the independent CODATA alpha."""
    with mp.workdps(60):
        reciprocal = mp.mpf(1) / 137
        alpha = mp.mpf(ALPHA_CODATA_2022)
        return {
            "speedRelativeError": (reciprocal - alpha) / alpha,
            "energyRelativeError": (reciprocal**2 - alpha**2) / alpha**2,
        }


def main() -> None:
    correction = kinetic_relative_correction(ALPHA_CODATA_2022)
    with mp.workdps(60):
        reciprocal = 1 / correction
    print(json.dumps({
        "schemaVersion": "alpha-energy-error/v1",
        "sourceIds": ["9408012137"],
        "alphaCodata2022": ALPHA_CODATA_2022,
        "relativisticKineticRelativeCorrection": mp.nstr(correction, 40),
        "reciprocalOfCorrection": mp.nstr(reciprocal, 30),
        "oneOver137Errors": {key: mp.nstr(value, 40) for key, value in reciprocal_137_errors().items()},
        "oneOver40000Validated": False,
        "evidenceUpgrade": False,
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
