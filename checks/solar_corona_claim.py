#!/usr/bin/env python3
"""Arithmetic-only checks for selected solar, gravity and timing claims."""
from __future__ import annotations
import json
import math


def planck_ratio_squared(lambda_c_m: float, planck_length_m: float) -> dict:
    displayed = (lambda_c_m / planck_length_m) ** 2
    reciprocal = (planck_length_m / lambda_c_m) ** 2
    return {
        "displayedRatioSquared": displayed,
        "reciprocalRatioSquared": reciprocal,
        "matchesDisplayedOneEMinus48": math.isclose(displayed, 1e-48, rel_tol=0.01),
    }


def corona_volumetric_heating(flux_w_m2: float, area_m2: float, height_m: float) -> float:
    return flux_w_m2 * area_m2 / (area_m2 * height_m)


def clock_unit_variants() -> dict:
    point_one_second_ns = 0.1 * 1e9
    point_one_nanosecond_ns = 0.1
    return {
        "pointOneSecondNs": point_one_second_ns,
        "pointOneNanosecondNs": point_one_nanosecond_ns,
        "secondsToNanosecondsRatio": point_one_second_ns / point_one_nanosecond_ns,
        "annualRateNsPerYear": 0.15,
        "rateAndInstantaneousOffsetDirectlyComparable": False,
    }


def audit_claims() -> dict:
    ratio = planck_ratio_squared(6.8e-12, 1.616255e-35)
    return {
        "schemaVersion": "solar-corona-claim-arithmetic/v1",
        "sourceId": "10409241814",
        "sourceLocators": ["07.jpg", "08.jpg", "09.jpg", "115.jpg", "130.jpg", "148.jpg", "149.jpg"],
        "planckRatio": ratio,
        "coronaVolumetricHeatingWPerM3": corona_volumetric_heating(2.1e7, 1e18, 1e8),
        "clockUnits": clock_unit_variants(),
        "scope": "Arithmetic and units only; no observational dataset, statistical fit or physical mechanism is validated.",
        "evidenceUpgrade": False,
    }


def main() -> None:
    print(json.dumps(audit_claims(), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
