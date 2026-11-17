#!/usr/bin/env python3
"""Checks for the 2025-12-02 prime-distribution/cosmology post.

The Euler-totient identity is a standard mathematical positive result.  It is
kept separate from unproved spectral and cosmological interpretations.
"""
from __future__ import annotations

from functools import lru_cache
import json
import math

import mpmath as mp

HBAR = 1.054571817e-34
C = 299792458.0
LAMBDA_C = 5.99153e-13
THETA_M = 1.55769540
ALPHA_INVERSE = 137.035999084
ALPHA = 1 / ALPHA_INVERSE
EULER_GAMMA = 0.5772156649015329
G_MEASURED = 6.67430e-11


def prime_gap_formula() -> dict[str, float | bool]:
    half_cotangent = 0.5 / math.tan(2 * THETA_M)
    gamma_over_pi = EULER_GAMMA / math.pi
    correction = half_cotangent + gamma_over_pi
    gap_at_p2 = math.log(2) + correction
    return {
        "halfCotangent": half_cotangent,
        "gammaOverPi": gamma_over_pi,
        "constantCorrection": correction,
        "claimedOneSupported": math.isclose(
            correction, 1, rel_tol=1e-9, abs_tol=0.0
        ),
        "gapAtP2": gap_at_p2,
        "negativeAtP2": gap_at_p2 < 0,
        "logPrimeLeadingTermRetained": True,
    }


def zeta_zero_spacing() -> dict[str, float | bool]:
    first_zero = 14.134725141734693790
    denominator = math.log(first_zero / (2 * math.pi))
    displayed = math.pi / denominator
    standard = 2 * math.pi / denominator
    return {
        "firstZeroOrdinate": first_zero,
        "displayedCmbSpacing": displayed,
        "standardMeanSpacing": standard,
        "displayedOverStandard": displayed / standard,
        "cmbMappingDerived": False,
        "primeErrorGueEstablished": False,
    }


@lru_cache(maxsize=None)
def _phi(n: int) -> int:
    return sum(math.gcd(k, n) == 1 for k in range(1, n + 1))


@lru_cache(maxsize=1)
def euler_phi_identity() -> dict[str, float | int | bool]:
    convolution_holds = all(
        sum(_phi(d) for d in range(1, n + 1) if n % d == 0) == n
        for n in range(1, 101)
    )
    partial = math.fsum(_phi(n) / n**4 for n in range(1, 5001))
    closed = float(mp.zeta(3) / mp.zeta(4))
    return {
        "divisorConvolutionHolds": convolution_holds,
        "convolutionCheckedThrough": 100,
        "partialAtFour": partial,
        "closedAtFour": closed,
        "absoluteDifference": abs(closed - partial),
        "identityProvesFiveDimensionalOperator": False,
    }


def constant_formulas() -> dict[str, float | bool]:
    cos_squared = math.cos(2 * THETA_M)**2
    alpha_rhs = (
        (1 / 137) * float(mp.zeta(3))
        / (math.pi**3 * math.sin(THETA_M)**2)
    )
    original_g = (
        C**3 * LAMBDA_C**2 / HBAR
        * cos_squared / (192 * math.pi**4)
    )
    cosmological_constant = (
        3 / LAMBDA_C**2 * float(mp.zeta(5)) / math.pi**5 * cos_squared
    )
    return {
        "alphaRhs": alpha_rhs,
        "alphaOverActual": alpha_rhs / ALPHA,
        "alphaFormulaMatches": math.isclose(
            alpha_rhs, ALPHA, rel_tol=1e-9, abs_tol=0.0
        ),
        "originalG": original_g,
        "originalGMatches": math.isclose(
            original_g, G_MEASURED, rel_tol=1e-9, abs_tol=0.0
        ),
        "cosmologicalConstant": cosmological_constant,
        "cosmologicalConstantMatches": math.isclose(
            cosmological_constant, 1.1e-52, rel_tol=1e-9, abs_tol=0.0
        ),
    }


def updated_gravity() -> dict[str, float | bool]:
    cos_squared = math.cos(2 * THETA_M)**2
    cos_theta_sp = cos_squared / math.sqrt(
        cos_squared**2 + (2 * math.pi * ALPHA)**2
    )
    theta_sp = math.acos(cos_theta_sp)
    base = constant_formulas()["originalG"]
    updated_g = base * 2**(-ALPHA_INVERSE) * math.exp(cos_theta_sp)
    g_point468 = base * 2**(-ALPHA_INVERSE) * math.exp(math.cos(0.468))
    return {
        "cosThetaSp": cos_theta_sp,
        "thetaSp": theta_sp,
        "point468Supported": math.isclose(
            theta_sp, 0.468, rel_tol=0.01, abs_tol=0.0
        ),
        "updatedG": updated_g,
        "updatedGOverMeasured": updated_g / G_MEASURED,
        "updatedGMatches": math.isclose(
            updated_g, G_MEASURED, rel_tol=1e-4, abs_tol=0.0
        ),
        "gUsingPoint468": g_point468,
        "point468RelativeError": abs(g_point468 - G_MEASURED) / G_MEASURED,
        "point468MatchesCentralValue": math.isclose(
            g_point468, G_MEASURED, rel_tol=1e-4, abs_tol=0.0
        ),
    }


def evidence_boundaries() -> dict[str, bool]:
    return {
        "spectralZetaEquivalenceProven": False,
        "rawPrimeDatasetProvided": False,
        "cmbDatasetProvided": False,
        "preregisteredCrossDomainStatisticProvided": False,
        "futureReferenceIsPublishedEvidence": False,
        "prlCitationVerified": False,
        "sharedParameterNamesProvePhysicalIdentity": False,
    }


def main() -> None:
    print(json.dumps({
        "schemaVersion": "prime-cosmology-claim-checks/v1",
        "sourceIds": ["10264331953"],
        "primeGapFormula": prime_gap_formula(),
        "zetaZeroSpacing": zeta_zero_spacing(),
        "eulerPhiIdentity": euler_phi_identity(),
        "constantFormulas": constant_formulas(),
        "updatedGravity": updated_gravity(),
        "evidenceBoundaries": evidence_boundaries(),
        "evidenceUpgrade": False,
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
