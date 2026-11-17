#!/usr/bin/env python3
"""Arithmetic and evidence checks for the 2025-12-12 observation-plan post."""
from __future__ import annotations

import json
import math

AU = 1.495978707e11


def period_and_scaling() -> dict[str, float | bool]:
    def period(mass: float, factor: float) -> float:
        return 1.20 * (1.8e10 / mass) * factor

    sgr_period = period(4.297e6, 0.18)
    return {
        "m87Period": period(5.5e9, 0.73),
        "m87PeriodWithSixPointFive": period(6.5e9, 0.73),
        "sgrPeriod": sgr_period,
        "sgrClaimedOverComputed": 5020 / sgr_period,
        "sgrPeriodIfFactorOne": period(4.297e6, 1.0),
        "cadenceAtTwoYears": 6 / 2.0,
        "cadenceAt292Years": 6 / 2.92,
        "phaseThresholdDegrees": 0.05 * 360,
        "grsPeriodOverHubbleTime": 1.7e9 / 13.8e9,
        "grsExceedsHubbleTime": False,
    }


def pa_amplitude() -> dict[str, float | bool]:
    delta = 2e-5 / math.sin(math.radians(17))
    return {
        "deltaPaRadians": delta,
        "deltaPaDegrees": math.degrees(delta),
        "printedOverComputedRatio": 4e-6 / delta,
        "degreeScaleDerived": False,
    }


def lense_thirring_baseline() -> dict[str, float | bool]:
    semimajor = 970 * AU
    gravitational_radius = 6.35e9
    spin = 0.5
    eccentricity = 0.880
    per_orbit = (
        4 * math.pi * spin
        * (gravitational_radius / semimajor)**1.5
        / (1 - eccentricity**2)**1.5
    )
    return {
        "printedFormulaHasAngularDimensions": False,
        "properPerOrbitRadians": per_orbit,
        "properPerOrbitDegrees": math.degrees(per_orbit),
        "modulationPercentageDerived": False,
    }


def observation_evidence() -> dict[str, float | bool]:
    rate = 360 / 5000
    return {
        "fullTurnRateDegrees": rate,
        "yearsToTenDegreeAccuracy": 10 / rate,
        "yearsToFiveDegreeAccuracy": 5 / rate,
        "multiEpochMeasurementPerformed": False,
        "absenceOfEvidenceSupportsTheoryUnconditionally": False,
    }


def main() -> None:
    print(json.dumps({
        "schemaVersion": "black-hole-observation-plan-checks/v1",
        "sourceIds": ["10293576133"],
        "periodAndScaling": period_and_scaling(),
        "paAmplitude": pa_amplitude(),
        "lenseThirringBaseline": lense_thirring_baseline(),
        "observationEvidence": observation_evidence(),
        "evidenceUpgrade": False,
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
