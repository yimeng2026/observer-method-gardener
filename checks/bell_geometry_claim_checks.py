#!/usr/bin/env python3
"""Independent checks for the 2025-12-04 Bell-parameter post.

The standard CHSH result is separated from later geometric ansatze.  Passing
arithmetic checks do not validate the proposed five-dimensional model.
"""
from __future__ import annotations

import json
import math

HBAR = 1.054571817e-34
C = 299792458.0
GEV_JOULES = 1.602176634e-10
LAMBDA_C = 5.99153e-13
Z = 1 / 70


def chsh_baseline() -> dict[str, float | bool]:
    return {
        "localHiddenVariableBound": 2.0,
        "singletMaximum": 2 * math.sqrt(2),
        "sameDirectionCorrelation": -1.0,
        "orthogonalCorrelation": 0.0,
        "standardQmAlwaysMaximal": False,
        "belowTwoProvesLocalRealism": False,
    }


def wilson_loop() -> dict[str, float | bool]:
    phase = math.pi / (4 * Z)
    correlation = math.cos(phase)
    s_value = 2 * abs(math.cos(phase) - math.cos(3 * phase))
    return {
        "z": Z,
        "phaseOverPi": phase / math.pi,
        "computedCorrelation": correlation,
        "computedS": s_value,
        "claimedCorrelationSupported": math.isclose(
            correlation, -math.sqrt(2) / 2, rel_tol=1e-9, abs_tol=1e-14
        ),
        "smallZTaylorExpansionValid": False,
        "correlationAtZOne": math.cos(math.pi / 4),
        "sAtZOne": 2 * abs(math.cos(math.pi / 4) - math.cos(3 * math.pi / 4)),
    }


def correction_versions() -> dict[str, float | bool]:
    original_coefficient = 1 / Z
    later_coefficient = 1 / 70
    return {
        "originalCurvatureCoefficient": original_coefficient,
        "laterCurvatureCoefficient": later_coefficient,
        "curvatureCoefficientRatio": original_coefficient / later_coefficient,
        "curvatureVersionsConsistent": math.isclose(
            original_coefficient, later_coefficient,
            rel_tol=1e-9, abs_tol=0.0,
        ),
        "topologicalCorrectionDimensionless": False,
        "torsionCorrectionDimensionDefined": False,
    }


def energy_scale() -> dict[str, float | bool]:
    energy_joules = HBAR * C / LAMBDA_C
    energy_gev = energy_joules / GEV_JOULES
    return {
        "energyJoules": energy_joules,
        "energyGeV": energy_gev,
        "claimedOverComputed": 207 / energy_gev,
        "claimedEnergySupported": math.isclose(
            energy_gev, 207, rel_tol=1e-9, abs_tol=0.0
        ),
    }


def energy_predictions() -> dict[str, float | bool]:
    tev_ratio_squared = (1000 / 207)**2
    fcc_ratio_squared = (100 / 207)**2
    cosmological_kappa = LAMBDA_C**2 * 1e-52
    return {
        "tevRatioSquaredUsingPrintedScale": tev_ratio_squared,
        "tevTenToMinusFourSupported": math.isclose(
            tev_ratio_squared, 1e-4, rel_tol=1e-9, abs_tol=0.0
        ),
        "fccRatioSquaredUsingPrintedScale": fcc_ratio_squared,
        "fccInternalArithmeticMatches": math.isclose(
            fcc_ratio_squared, 0.23, rel_tol=0.02, abs_tol=0.0
        ),
        "cosmologicalKappa": cosmological_kappa,
        "cosmologicalKappaClaimSupported": math.isclose(
            cosmological_kappa, 1e-5, rel_tol=1e-9, abs_tol=0.0
        ),
    }


def black_hole_case() -> dict[str, float | bool]:
    product = 0.01 * 0.65 * 1.0
    predicted_s = 2 * math.sqrt(2) * product
    return {
        "visibilityProduct": product,
        "predictedS": predicted_s,
        "arithmeticConsistent": math.isclose(
            predicted_s, 0.018, rel_tol=0.0, abs_tol=0.0005
        ),
        "factorsIndependentlyDerived": False,
        "localRealismRestored": False,
        "blackHoleInteriorMeasurementProvided": False,
    }


def interference_baseline() -> dict[str, float | bool]:
    ratio = LAMBDA_C / 5e-7
    return {
        "twoEqualAmplitudesAtZeroPhase": abs(1 + 1)**2,
        "visibleLambdaRatio": ratio,
        "visibleRatioOrderSupported": 1e-6 < ratio < 1e-4,
        "extraPhaseMeasured": False,
        "whichWayTopologyDerived": False,
    }


def evidence_boundaries() -> dict[str, bool]:
    return {
        "rawBellDatasetProvided": False,
        "prospectiveProtocolProvided": False,
        "independentReplicationProvided": False,
        "agnAngularCorrelationIsBellTest": False,
        "aiGeneratedAnswerIsExperimentalEvidence": False,
    }


def main() -> None:
    print(json.dumps({
        "schemaVersion": "bell-geometry-claim-checks/v1",
        "sourceIds": ["10269908045"],
        "chshBaseline": chsh_baseline(),
        "wilsonLoop": wilson_loop(),
        "correctionVersions": correction_versions(),
        "energyScale": energy_scale(),
        "energyPredictions": energy_predictions(),
        "blackHoleCase": black_hole_case(),
        "interferenceBaseline": interference_baseline(),
        "evidenceBoundaries": evidence_boundaries(),
        "evidenceUpgrade": False,
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
