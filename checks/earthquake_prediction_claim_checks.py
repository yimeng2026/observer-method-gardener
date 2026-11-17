#!/usr/bin/env python3
"""Arithmetic and evidence checks for the 2025-12-07 earthquake post.

Displayed formulas are treated as claims, not observations.  The checks do
not validate an earthquake forecast or establish any physical mechanism.
"""
from __future__ import annotations

import json
import math

YEAR_SECONDS = 365.25 * 86400
LAMBDA_C = 5.99e-13
EARTH_RADIUS = 6.371e6
ALPHA = 7.2973525693e-3


def cosmic_periods() -> dict[str, float | int | bool]:
    seconds = (
        2 * math.pi / 5.01e20
        * 1.37e26 / 5.99e-13
        * math.sin(1.5577)
    )
    years = seconds / YEAR_SECONDS
    lcm_years = math.lcm(7124, 1781, 2310)
    event_time = lcm_years * LAMBDA_C / EARTH_RADIUS
    return {
        "superPeriodSeconds": seconds,
        "superPeriodYears": years,
        "claimedPeriodOverComputed": 7000 / years,
        "computedOverClaimedPeriod": years / 7000,
        "sevenThousandSupported": False,
        "lcmYears": lcm_years,
        "eventTimeYears": event_time,
        "eventDateEstablished": False,
    }


def curvature_and_gradient() -> dict[str, float | bool]:
    delta_r = 2.4e-28 * 1e22
    chi_q = (
        ALPHA / (2 * math.pi)
        * LAMBDA_C / 1.37e26
        * math.sin(1.5577)
    )
    return {
        "deltaR": delta_r,
        "chiQ": chi_q,
        "deltaRMatchesClaim": math.isclose(
            delta_r, 1e-6, rel_tol=1e-9, abs_tol=0.0
        ),
        "poissonDimensionsClosed": False,
        "verticalGradientDimensionsClosed": False,
        "precursorGradientDerived": False,
    }


def evidence_boundaries() -> dict[str, bool]:
    return {
        "paleoDatasetProvided": False,
        "machineLearningBenchmarkProvided": False,
        "prospectiveProtocolProvided": False,
        "operationalForecastValidated": False,
    }


def rupture_and_magnitude() -> dict[str, float | bool]:
    moment = 1.2e23
    modulus = 7.5e10
    return {
        "sqrtMomentOverModulus": math.sqrt(moment / modulus),
        "sqrtHasLengthUnits": False,
        "momentMagnitude": (2 / 3) * (math.log10(moment) - 9.1),
        "depthWithinTransitionZone": 410 <= 280 <= 660,
        "ruptureDurationSeconds": 350 / 4.8,
        "realRuptureObservationProvided": False,
    }


def main() -> None:
    print(json.dumps({
        "schemaVersion": "earthquake-prediction-claim-checks/v1",
        "sourceIds": ["10277023577"],
        "cosmicPeriods": cosmic_periods(),
        "curvatureAndGradient": curvature_and_gradient(),
        "evidenceBoundaries": evidence_boundaries(),
        "ruptureAndMagnitude": rupture_and_magnitude(),
        "evidenceUpgrade": False,
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
