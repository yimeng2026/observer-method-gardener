#!/usr/bin/env python3
"""Numerical checks for the Mercury-precession derivation and its baselines."""
from __future__ import annotations
import json
import math

ARCSECONDS_PER_RADIAN = 180 / math.pi * 3600


def _validate(gm, a, e, c):
    if gm <= 0 or a <= 0 or c <= 0 or not 0 <= e < 1:
        raise ValueError("Require GM>0, a>0, c>0 and 0<=e<1")


def precession_arcsec_century(gm, a, e, period_days, c=299792458.0):
    _validate(gm, a, e, c)
    if period_days <= 0:
        raise ValueError("Orbital period must be positive")
    p = a * (1 - e**2)
    alpha2 = gm / (c**2 * p)
    radians = 6 * math.pi * alpha2
    orbits = 100 * 365.25 / period_days
    return {
        "alpha2": alpha2,
        "precessionRadians": radians,
        "orbitsPerCentury": orbits,
        "arcsecPerCentury": radians * orbits * ARCSECONDS_PER_RADIAN,
    }


def orbital_parameters(gm, a, e, c=299792458.0):
    _validate(gm, a, e, c)
    p = a * (1 - e**2)
    baseline = precession_arcsec_century(gm, a, e, 87.9691, c)
    return {
        "semiLatusRectum": p,
        "alpha2": baseline["alpha2"],
        "twoPiArcsecPerCentury": baseline["arcsecPerCentury"] / 3,
        "sixPiArcsecPerCentury": baseline["arcsecPerCentury"],
        "sixPiOverTwoPi": 3.0,
        "characteristicSpeed": math.sqrt(gm / p),
        "perihelionSpeed": math.sqrt(gm * (1 + e) / (a * (1 - e))),
    }


def secular_particular_coefficient(gm, c, p, e):
    if gm <= 0 or c <= 0 or p <= 0 or not 0 <= e < 1:
        raise ValueError("Require positive GM, c, p and 0<=e<1")
    k = gm / (c**2 * p)
    alpha2 = k
    return {
        "B": -e * k,
        "twiceB": -2 * e * k,
        "forcingCosineCoefficient": -2 * e * k,
        "alpha2": alpha2,
        "precessionRadians": 2 * math.pi * alpha2,
    }


def main() -> None:
    result = orbital_parameters(1.32712440018e20, 5.791e10, 0.2056)
    print(json.dumps({
        "schemaVersion": "mercury-precession-check/v1",
        "sourceId": "9524209110",
        **result,
        "displayedResonantParticular": secular_particular_coefficient(1.32712440018e20, 299792458.0, result["semiLatusRectum"], 0.2056),
        "independentSixPiDerivationEstablished": False,
        "unifiedTheoryValidated": False,
        "evidenceUpgrade": False,
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
