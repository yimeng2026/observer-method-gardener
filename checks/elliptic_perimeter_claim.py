#!/usr/bin/env python3
"""Check the displayed improper elliptic-perimeter integral."""
from __future__ import annotations
import json
import mpmath as mp


def ellipse_perimeter(a, b):
    """Numerically integrate the displayed formula without evaluating its endpoints."""
    if not a > b > 0:
        raise ValueError("The displayed real-valued family requires a>b>0")
    with mp.workdps(50):
        a = mp.mpf(a)
        b = mp.mpf(b)
        upper = a / b
        epsilon = min(mp.mpf("1e-10"), (upper - 1) / 100)
        integrand = lambda t: t**2 / mp.sqrt((t**2 - 1) * (1 - b**2 * t**2 / a**2))
        points = [1 + epsilon, 1 + (upper - 1) / 4, 1 + (upper - 1) / 2, 1 + 3 * (upper - 1) / 4, upper - epsilon]
        integral = mp.quad(integrand, points)
        perimeter = 4 * b**2 / a * integral
        standard = 4 * a * mp.ellipe(1 - b**2 / a**2)
        return {
            "integralFromOpenEndpoints": float(integral),
            "displayedPerimeter": float(perimeter),
            "standardPerimeter": float(standard),
            "relativeDiscrepancy": float(abs(perimeter - standard) / standard),
        }


def endpoint_models(a, b):
    """Leading inverse-square-root models at t=1 and t=a/b."""
    if not a > b > 0:
        raise ValueError("The displayed real-valued family requires a>b>0")
    eccentricity_squared = 1 - b**2 / a**2
    upper = a / b
    return {
        "leftExponent": 0.5,
        "rightExponent": 0.5,
        "leftCoefficient": 1 / (2 * eccentricity_squared)**0.5,
        "rightCoefficient": upper**2 / (2 * a * eccentricity_squared / b)**0.5,
    }


def main() -> None:
    result = ellipse_perimeter(2.0, 1.0)
    print(json.dumps({
        "schemaVersion": "elliptic-perimeter-check/v1",
        "sourceId": "9531357756",
        "a": 2.0,
        "b": 1.0,
        **result,
        "endpointModels": endpoint_models(2.0, 1.0),
        "improperIntegralDivergesMerelyBecauseDenominatorVanishes": False,
        "zeroErrorOrIndependentPhysicalTheoryEstablished": False,
        "evidenceUpgrade": False,
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
