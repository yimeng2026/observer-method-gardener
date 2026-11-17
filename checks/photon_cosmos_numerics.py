#!/usr/bin/env python3
"""Reproduce the exact numerical variants visible in post 9491341592."""
from __future__ import annotations
import json
import math

ARCSECONDS_PER_RADIAN = 180 / math.pi * 3600


def fragment_deflection_terms(gm, radius, c=299792458.0):
    """Evaluate 4*k*(1+0.5*log(1+k*exp(-k))) and the page-leading k term."""
    if gm <= 0 or radius <= 0 or c <= 0:
        raise ValueError("Require positive GM, radius and c")
    k = gm / (radius * c**2)
    base = 4 * k
    relative = 0.5 * math.log1p(k * math.exp(-k))
    correction = base * relative
    return {
        "k": k,
        "baseArcseconds": base * ARCSECONDS_PER_RADIAN,
        "pageLeadingArcseconds": k * ARCSECONDS_PER_RADIAN,
        "relativeCorrection": relative,
        "correctionArcseconds": correction * ARCSECONDS_PER_RADIAN,
        "totalArcseconds": (base + correction) * ARCSECONDS_PER_RADIAN,
    }


def fragment_redshift_terms(exponent):
    return {
        "frequencyRatio": math.exp(-exponent),
        "redshift": math.exp(exponent) - 1,
    }


def main() -> None:
    deflection = fragment_deflection_terms(1.32712440018e20, 6.957e8)
    redshift = fragment_redshift_terms(3.19431099780734)
    print(json.dumps({
        "schemaVersion": "photon-cosmos-fragment-numerics/v1",
        "sourceId": "9491341592",
        "constants": {"GM": 1.32712440018e20, "R": 6.957e8, "c": 299792458.0},
        "deflection": deflection,
        "ratioToPiTimes1eMinus19Arcsec": deflection["correctionArcseconds"] / (math.pi * 1e-19),
        "redshiftArithmetic": redshift,
        "geodesicOrRedshiftModelValidated": False,
        "cosmologicalRedshiftComparisonEstablished": False,
        "evidenceUpgrade": False,
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
