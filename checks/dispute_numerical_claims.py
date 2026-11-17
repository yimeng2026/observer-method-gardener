#!/usr/bin/env python3
"""Independent numerical checks for post 9475919621."""
from __future__ import annotations
import json
import math

ARCSECONDS_PER_RADIAN = 180 / math.pi * 3600


def displayed_g_estimate(mu, density, reference):
    calculated = mu * density / (4 * math.pi)
    return {
        "calculated": calculated,
        "reference": reference,
        "relativeBelowReference": (reference - calculated) / reference,
    }


def starlight_remainder_scales(gm, radius, c=299792458.0):
    k = gm / (radius * c**2)
    return {
        "k": k,
        "kCubedArcseconds": k**3 * ARCSECONDS_PER_RADIAN,
        "exponential": math.exp(-k),
        "oneMinusExponential": 1 - math.exp(-k),
    }


def main() -> None:
    print(json.dumps({
        "schemaVersion": "dispute-numerical-claims/v1",
        "sourceId": "9475919621",
        "gravityExample": displayed_g_estimate(1.52e-13, 5500.0, 6.674e-11),
        "starlightExample": starlight_remainder_scales(1.32712440018e20, 6.957e8),
        "claimedStarlightErrorArcseconds": 3.4e-19,
        "numericalNearMatchRepairsDimensions": False,
        "modelOrObservationValidated": False,
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
