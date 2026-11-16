#!/usr/bin/env python3
"""Numerical checks for the displayed starlight-deflection correction."""
from __future__ import annotations
import json
import math

ARCSECONDS_PER_RADIAN = 180 / math.pi * 3600


def log_expansion(b):
    if b <= -1:
        raise ValueError("Require b>-1")
    return {
        "logTimesExponential": math.log1p(b) * math.exp(-b),
        "seriesThirdOrder": b - 1.5 * b**2 + 5 * b**3 / 6,
    }


def deflection_terms(gm, radius, c=299792458.0):
    if gm <= 0 or radius <= 0 or c <= 0:
        raise ValueError("Require positive GM, radius and c")
    b = gm / (radius * c**2)
    base = 4 * b
    relative = 0.5 * math.log1p(b) * math.exp(-b)
    correction = base * relative
    return {
        "b": b,
        "baseRadians": base,
        "baseArcseconds": base * ARCSECONDS_PER_RADIAN,
        "relativeCorrection": relative,
        "correctionRadians": correction,
        "correctionArcseconds": correction * ARCSECONDS_PER_RADIAN,
        "totalArcseconds": (base + correction) * ARCSECONDS_PER_RADIAN,
    }


def prefactor_exponent(gm, reference_radius, radius, c=299792458.0):
    if reference_radius <= 0 or radius <= 0 or c <= 0:
        raise ValueError("Require positive radii and c")
    return gm * (1 - reference_radius / radius) / (reference_radius * c**2)


def main() -> None:
    result = deflection_terms(1.32712440018e20, 6.957e8)
    print(json.dumps({
        "schemaVersion": "starlight-deflection-check/v1",
        "sourceId": "9475751686",
        "constants": {"GM": 1.32712440018e20, "R": 6.957e8, "c": 299792458.0},
        **result,
        "ratioToPiTimes1eMinus19Arcsec": result["correctionArcseconds"] / (math.pi * 1e-19),
        "ratioTo6.958eMinus19Arcsec": result["correctionArcseconds"] / 6.958e-19,
        "seriesAtSolarB": log_expansion(result["b"]),
        "metricOrIndependentPredictionEstablished": False,
        "evidenceUpgrade": False,
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
