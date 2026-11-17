#!/usr/bin/env python3
"""Local arithmetic and dimension checks for the 2025-12-14 field-equation post."""
from __future__ import annotations

import json
import math

C = 299792458.0
G = 6.67430e-11
HBAR = 1.054571817e-34
LAMBDA_C = 6e-13


def far_field_yukawa() -> dict[str, float]:
    ell = math.sqrt(3) * LAMBDA_C
    r = 2.4e-12
    amplitude = math.exp(-r / ell)
    radial_box = amplitude * (
        1 / (ell**2 * r)
        + 2 / (ell * r**2)
        + 2 / r**3
        - 2 / (ell * r**2)
        - 2 / r**3
    )
    target = amplitude / (ell**2 * r)
    residual = radial_box - target
    return {"ell": ell, "residual": residual, "relativeResidual": residual / target}


def simplified_constant_curvature() -> dict[str, float | bool]:
    xi = 0.02
    lambda_effective = -1 / (4 * xi)
    return {
        "zeroCurvatureRoot": 0.0,
        "nonzeroCurvatureRoot": -1 / xi,
        "lambdaEffective": lambda_effective,
        "curvatureFromLambda": 4 * lambda_effective,
        "negativeConstantCurvatureForPositiveXi": lambda_effective < 0,
    }


def fr_coefficient_conditions() -> dict[str, float | bool]:
    xi = 0.02
    eta = 0.03
    return {
        "fQuadraticCoefficient": xi / 2,
        "fPrimeLinearCoefficient": xi,
        "equalCoefficientsRecoverFr": 2 * (xi / 2) == xi,
        "fullEquationAutomaticallyFr": eta == xi,
    }


def metric_versions() -> dict[str, float | bool]:
    mass_factor = 2.0
    length = 3.0
    exponential_kappa = mass_factor / length**3
    rational_kappa = 1 / length**2
    return {
        "exponentialKappa": exponential_kappa,
        "rationalKappa": rational_kappa,
        "exponentialCoreR": 12 * exponential_kappa,
        "rationalCoreR": 12 * rational_kappa,
        "exponentialAAtZero": 1.0,
        "rationalAAtZero": 1.0,
        "completeFieldSolutionEstablished": False,
    }


def scale_and_shadow() -> dict[str, float | bool]:
    micro_radius = 2 * G * 1e12 / C**2
    planck_length = math.sqrt(HBAR * G / C**3)
    return {
        "sgrShadowFractionSquared": (LAMBDA_C / 1.2e10)**2,
        "microSchwarzschildRadius": micro_radius,
        "lambdaOverMicroRadius": LAMBDA_C / micro_radius,
        "microRadiusCloseToLambda": math.isclose(micro_radius, LAMBDA_C, rel_tol=0.1),
        "lambdaOverPlanckLength": LAMBDA_C / planck_length,
    }


def main() -> None:
    print(json.dumps({
        "schemaVersion": "field-equation-ansatz-checks/v1",
        "sourceIds": ["10300154155"],
        "farFieldYukawa": far_field_yukawa(),
        "simplifiedConstantCurvature": simplified_constant_curvature(),
        "frCoefficientConditions": fr_coefficient_conditions(),
        "metricVersions": metric_versions(),
        "scaleAndShadow": scale_and_shadow(),
        "completeFieldSolutionEstablished": False,
        "evidenceUpgrade": False,
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
