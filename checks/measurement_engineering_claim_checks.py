#!/usr/bin/env python3
"""Independent checks for the 2025-12-21 measurement, CT and radar post."""
from __future__ import annotations

import json
import math

C = 299792458.0
H = 6.62607015e-34
HBAR = 1.054571817e-34
LAMBDA_C = 5.9915e-13


def standard_quantum_baseline() -> dict[str, float]:
    differences = [b - a for a, b in zip([1, 2, 4], [2, 4, 7])]
    return {
        "positionMomentumBound": HBAR / 2,
        "squeezedProduct": (0.5 * math.exp(-1.5)) * (0.5 * math.exp(1.5)),
        "chshMaximum": 2 * math.sqrt(2),
        "allanExample": sum(value**2 for value in differences) / (2 * (4 - 1)),
    }


def characteristic_constants() -> dict[str, float]:
    frequency = C / LAMBDA_C
    angular_frequency = 2 * math.pi * frequency
    energy = H * frequency
    return {
        "periodSeconds": LAMBDA_C / C,
        "ordinaryFrequencyHz": frequency,
        "angularFrequencyRadPerSecond": angular_frequency,
        "photonEnergyJ": energy,
        "energyFromHbarTimesOmegaJ": HBAR * angular_frequency,
        "displayedEnergyRatio": 3.30e-7 / energy,
    }


def engineering_dimensions() -> dict[str, dict[str, float]]:
    # Only dimensions are checked; no proposed model is thereby validated.
    return {
        "spacetimeLeft": {"L": 1, "T": 1},
        "spacetimeRight": {"L": 0, "T": 1},
        "afmDisplacement": {"L": 1, "T": 0.25},
        "ligoStrain": {"L": 0.5, "T": -0.5},
    }


def ct_business_arithmetic() -> dict[str, float | int | bool]:
    traditional = sum([80000, 120000, 100000, 60000, 40000])
    quantum = sum([150000, 200000, 120000, 80000, 100000])
    annual_saving = 365 * 100 * (2.5 + 0.8 + 1.2)
    return {
        "traditionalTotal": traditional,
        "quantumTotal": quantum,
        "totalPremiumFraction": (quantum - traditional) / traditional,
        "electricitySaving": (3.5 - 1.2) / 3.5,
        "annualSaving": annual_saving,
        "nominalPaybackYears": (1800000 - 1200000) / (300000 + annual_saving),
        # The prices use dollar signs while annual savings and income use yuan.
        "currencyAwarePayback": False,
    }


def ct_dose_and_performance() -> dict[str, float]:
    r = 1.5
    return {
        "snrGain": math.exp(r),
        "doseFactor95": math.exp(-2 * r),
        "performanceFactor": math.exp(r) * 2 * 10 * math.exp(2 * r) * 0.615,
        "heartDoseFromFactor": 15 * math.exp(-2 * r),
        "heartDoseDisplayedReduction": (15 - 3) / 15,
        "breastPCTVReduction": (2 - 0.8) / 2,
        "lungPCTVReduction": (1.5 - 0.6) / 1.5,
        "resolutionRatio": 0.35 / 0.15,
        "contrastRatio": 0.3 / 0.08,
    }


def dichroism_and_dose_cancellation() -> dict[str, float | int]:
    # I_pm = I_0 exp[-integral(mu_0 pm Delta_mu) dl].
    r = 1.5
    classical_over_quantum_resolution = math.exp(r)
    return {
        "logRatioOpticalDepthFactor": 2,
        "doseFactorUsingOwnResolution": (
            math.exp(-2 * r) * classical_over_quantum_resolution**2
        ),
    }


def radar_examples() -> dict[str, float]:
    ka_without_angle = C / (1.2 * 35e9 * math.sqrt(1e6)) * math.exp(-1.5)
    return {
        "kaVelocityWithoutAngle": ka_without_angle,
        "kaVelocityWithAngle": ka_without_angle / math.cos(math.radians(30)),
        # Frequency resolution required by the separate optical-velocity formula,
        # for n=1, cos(theta)=1 and a target resolution of 1 micrometre/second.
        "opticalRequiredFrequencyResolution": 2 * 1e14 * 1e-6 / C,
    }


def mtf_and_availability() -> dict[str, float | bool]:
    frequency = 40 * math.sqrt(-math.log(0.5))
    return {
        "mtfFrequencyLpPerMm": frequency,
        "linePairPitchMm": 1 / frequency,
        "singleLineWidthMm": 1 / (2 * frequency),
        "availabilityBound": 10000 / (10000 + 2),
        "measuredAvailability": False,
    }


def main() -> None:
    print(json.dumps({
        "schemaVersion": "measurement-engineering-claim-checks/v1",
        "sourceIds": ["10320926799"],
        "standardQuantumBaseline": standard_quantum_baseline(),
        "characteristicConstants": characteristic_constants(),
        "engineeringDimensions": engineering_dimensions(),
        "ctBusinessArithmetic": ct_business_arithmetic(),
        "ctDoseAndPerformance": ct_dose_and_performance(),
        "dichroismAndDoseCancellation": dichroism_and_dose_cancellation(),
        "radarExamples": radar_examples(),
        "mtfAndAvailability": mtf_and_availability(),
        "clinicalValidation": False,
        "evidenceUpgrade": False,
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
