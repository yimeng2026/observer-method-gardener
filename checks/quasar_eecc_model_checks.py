#!/usr/bin/env python3
"""Local arithmetic and convention checks for the 2025-12-13 quasar post.

These checks compare mutually inconsistent printed versions.  A passing test
only certifies the independent arithmetic, never the physical EECC model.
"""
from __future__ import annotations

import json
import math

C = 299792458.0


def kernel_and_units() -> dict[str, float | bool]:
    theta = 1.5577

    def kernel(z_parameter: float) -> float:
        return (
            (2 / math.pi) * theta * math.exp(-1 / z_parameter)
            * (1 + 0.5 * math.log1p(1 / z_parameter))
        )

    return {
        "kernelAt003": kernel(0.03),
        "kernelAt00123": kernel(0.0123),
        "kernelAt0005": kernel(0.005),
        "pointNineKernelCompatible": False,
        "printedMomentumOverMass": C,
    }


def jet_and_orbit_baseline() -> dict[str, float | bool]:
    opening = math.sqrt(10) / 30
    return {
        "openingBaselineRadians": opening,
        "openingBaselineDegrees": math.degrees(opening),
        "openingRatioToPointOneDegree": opening / math.radians(0.1),
        "pointOneDegreeBaselineReproduced": math.isclose(opening, math.radians(0.1)),
        "evpaPrinted": math.atan(1.0),
        "evpaStandard": 0.5 * math.atan(1.0),
        "nodalPrintedCoefficient": 12 * math.pi,
        "nodalStandardCoefficient": 3 * math.pi,
        "nodalPrintedOverStandard": (12 * math.pi) / (3 * math.pi),
    }


def redshift_and_period() -> dict[str, float]:
    alpha = 0.28
    gamma = 1.55
    redshift_factor = (1.158 / 1.004)**-0.65
    earlier = 11 * (5.5e9 / 7.77e8) * redshift_factor
    later = 11 * (6.5e9 / 7.77e8) * redshift_factor
    return {
        "alphaMinusGamma": alpha - gamma,
        "gammaMinusTwoAlpha": gamma - 2 * alpha,
        "printedExponent": -0.65,
        "observedExponentAfterTimeDilation": -0.65 + 1,
        "periodEarlierCalibration": earlier,
        "periodLaterCalibration": later,
        "periodEarlierOverTarget": earlier / 1.86,
        "periodLaterOverTarget": later / 1.86,
        "opticalMassExponentAfterSubstitution": -0.5 + 0.5 * (-1),
        "opticalRedshiftExponentAfterSubstitution": 0.4 + 0.5 * (-0.65),
    }


def energy_and_stability() -> dict[str, float | bool]:
    zeta = 1e-6
    geometric_factor = zeta**-0.5 * (1 + math.log(1 / zeta))
    early_erg_per_second = 3e45
    si_watts = 3.2e45
    return {
        "geometricFactor": geometric_factor,
        "extractionEfficiency": 0.1 * geometric_factor,
        "earlyNormalizationErgsPerSecond": early_erg_per_second,
        "siNormalizationWatts": si_watts,
        "siNormalizationErgsPerSecond": si_watts * 1e7,
        "powerUnitJumpRatio": si_watts * 1e7 / early_erg_per_second,
        "powerFractionOmitsGeometry": True,
        "stiffnessMatrixProvided": False,
        "equilibriumSpinDemonstrated": False,
        "observationalFitPerformed": False,
    }


def blr_quadrupole() -> dict[str, float]:
    quadrupole = -1e-3
    radius_ratio = 1e12 / 1e16
    printed_arithmetic = abs(-0.75 * quadrupole * radius_ratio**2)
    return {
        "omegaSquaredQuadrupoleCoefficient": 1.5,
        "printedQuadrupoleCoefficient": -1.5,
        "correctSignedRelativeShift": 0.75 * quadrupole * radius_ratio**2,
        "printedSignedRelativeShift": -0.75 * quadrupole * radius_ratio**2,
        "printedArithmeticMagnitude": printed_arithmetic,
        "claimedInstantOverPrintedArithmetic": 0.025 / printed_arithmetic,
        "finalFormulaValue": 0.25 * abs(quadrupole) * radius_ratio**-1.5,
        "claimedFinalAmplitude": 0.28,
    }


def sgr_a_comment() -> dict[str, float | bool]:
    schwarzschild_radius = 1.27e10
    lambda_c = 5.99e-13
    theta = 1.5577
    z_parameter = 0.03
    semi_major = (0.5 / 0.08) * schwarzschild_radius * 0.95
    zeta = (
        (lambda_c / schwarzschild_radius)
        * (theta / math.pi)**-0.5
        * z_parameter**(1 / 3)
    )
    eta = 1 - 8.29e-5 * math.sqrt(schwarzschild_radius / lambda_c) * math.tanh(1 / z_parameter)
    ratio = semi_major / schwarzschild_radius
    return {
        "zetaFromCommentFormula": zeta,
        "claimedZetaOverComputed": 4.07e-6 / zeta,
        "semiMajor": semi_major,
        "semiMajorOverSchwarzschild": ratio,
        "polarRadiusFromComputedZeta": zeta * semi_major,
        "claimedPolarRadius": 3.07e5,
        "etaFromCommentFormula": eta,
        "nearCircleAndThinDiskConsistent": 0.7 <= eta <= 1 and 0.01 <= ratio <= 0.1,
    }


def main() -> None:
    print(json.dumps({
        "schemaVersion": "quasar-eecc-model-checks/v1",
        "sourceIds": ["10296919247"],
        "kernelAndUnits": kernel_and_units(),
        "jetAndOrbitBaseline": jet_and_orbit_baseline(),
        "redshiftAndPeriod": redshift_and_period(),
        "energyAndStability": energy_and_stability(),
        "blrQuadrupole": blr_quadrupole(),
        "sgrAComment": sgr_a_comment(),
        "observationalFitPerformed": False,
        "evidenceUpgrade": False,
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
