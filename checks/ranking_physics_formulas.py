#!/usr/bin/env python3
"""Algebra checks for formulas displayed in post 9458257253."""
from __future__ import annotations
import json
import math

ARCSECONDS_PER_RADIAN = 180 / math.pi * 3600


def exponential_rebaseline(k):
    return {
        "leftK2Over3": k**2 / 3,
        "rightExponential": math.exp(k * (1 - k / 2 + k**2 / 3)),
        "onePlusK": 1 + k,
    }


def correction_integral_coefficients():
    """Integrate r^-7, r^-8, r^-9 from R to infinity."""
    return {
        "firstDenominator": 6,
        "secondDenominator": 7,
        "thirdDenominator": 8,
    }


def negative_exponential_deflection_correction(gm, radius, c=299792458.0):
    k = gm / (radius * c**2)
    return 4 * k * (math.exp(-k) - 1) * ARCSECONDS_PER_RADIAN


def main() -> None:
    print(json.dumps({
        "schemaVersion": "ranking-physics-formulas/v1",
        "sourceId": "9458257253",
        "rebaselineAtK0.1": exponential_rebaseline(0.1),
        "integralCoefficients": correction_integral_coefficients(),
        "negativeExponentialCorrectionArcseconds": negative_exponential_deflection_correction(1.32712440018e20, 6.957e8),
        "claimedPrecisionArcseconds": 1e-19,
        "independentPhysicalModelEstablished": False,
        "worldRankingEstablished": False,
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
