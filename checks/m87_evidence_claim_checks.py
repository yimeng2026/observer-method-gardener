#!/usr/bin/env python3
"""Independent, bounded checks for the M87 / pulsar evidence post.

All source-model values are labelled as such.  Literature baselines are
versioned and do not become independent confirmation of the proposed theory.
"""
from __future__ import annotations

import json
import math

HBAR = 1.054571817e-34
C = 299792458.0
G = 6.67430e-11
MSUN = 1.98847e30
LAMBDA_C = 5.99153e-13
THETA_M = 1.55769540


def scale_length() -> dict[str, float | bool]:
    unscreened = math.sqrt(HBAR * G / (math.pi * C**3))
    return {
        "unscreenedLengthM": unscreened,
        "requiredScreeningFactor": unscreened / LAMBDA_C,
        "lambdaOverUnscreened": LAMBDA_C / unscreened,
        "dimensionlessScreeningProven": False,
    }


def jet_power() -> dict[str, str | bool]:
    # In SI, B^2/mu0 is energy density.  The extra Rs^2/lambda_c^2
    # does not restore an area after multiplication by c.
    return {
        "quantityAfterMu0Restored": "W/m^2",
        "printedExpressionIsPower": False,
        "observedJetPowerReproduced": False,
    }


def efficiency() -> dict[str, float | bool]:
    # An illustrative mass only: this is not a new M87 mass measurement.
    mass = 6.5e9 * MSUN
    radius = 2 * G * mass / C**2
    exponent = THETA_M / math.pi * radius / LAMBDA_C
    value = 0.5 * (-math.expm1(-exponent))
    return {
        "illustrativeMassMsun": 6.5e9,
        "schwarzschildRadiusM": radius,
        "exponent": exponent,
        "value": value,
        "independentFit": False,
    }


def turbulent_viscosity() -> dict[str, float | bool]:
    denominator = math.sqrt(1 - 2 / 3 * math.sin(THETA_M)**2)
    period = 0.039
    nu_si = LAMBDA_C**2 / period / denominator
    nu_cgs = nu_si * 1e4
    return {
        "usingPeriodCm2PerSecond": nu_cgs,
        "printedOverPeriodBased": 1.2e12 / nu_cgs,
        "requiredTauSeconds": LAMBDA_C**2 / denominator / (1.2e12 * 1e-4),
        "tauDecaySupplied": False,
        "printedValueSupported": False,
    }


def parameter_counts() -> dict[str, int | bool]:
    groups = [12, 15, 11, 9, 18, 14, 5]
    return {
        "total": sum(groups),
        "allIndependentlyDerived": False,
    }


def evidence_counts() -> dict[str, int | bool]:
    domains = [287, 194, 219, 173, 236]
    strengths = [417, 392, 300]
    return {
        "domainSum": sum(domains),
        "strengthSum": sum(strengths),
        "claimedConfirmed": 973,
        "pending": 136,
        "confirmedPlusPending": 973 + 136,
        "independentEvidenceRegistryProvided": False,
    }


def pulsar_baseline() -> dict[str, float | str | bool]:
    # Saffer et al., arXiv:2412.02850, Table 1 and abstract.
    return {
        "source": "arXiv:2412.02850",
        "spinPeriodMs": 39.1226562801558,
        "transverseMagneticFieldAtPolesG": 3.11e9,
        "claimedOverPublishedB": 1e13 / 3.11e9,
        "updatedMassMsun": 1.806,
        "updatedMassUncertaintyMsun": 0.037,
        "printedMagneticFieldSupported": False,
    }


def entropy_core() -> dict[str, bool]:
    # S=A/(4 l_P^2)*theta_m/pi is dimensionless with k_B=1;
    # hbar*c/lambda_c times a dimensionless entropy has energy units.
    return {
        "dimensionlessInKbUnits": True,
        "energyUnitsClose": True,
        "informationParadoxSolved": False,
    }


def dimensional_boundaries() -> dict[str, float | bool]:
    return {
        "exponentialCorrection": math.exp(-0.5 * (THETA_M / math.pi)**2),
        "curvatureFactorDimensionless": False,
        "sigmaUpgradeDerived": False,
        "lVKBandAtOneEMinusTenHz": False,
        "closedElevenDimensionalActionProvided": False,
    }


def evidence_boundaries() -> dict[str, bool]:
    return {
        "virtualDataDisclosedInComments": True,
        "rawM87ObservationsProvided": False,
        "officialAwardsOrAppointmentsProvided": False,
        "healthOrIqTextIsMeasurement": False,
        "simulatedPoliticalDocumentsAreOfficial": False,
    }


def main() -> None:
    print(json.dumps({
        "schemaVersion": "m87-evidence-claim-checks/v1",
        "sourceIds": ["10238581618"],
        "scaleLength": scale_length(),
        "jetPower": jet_power(),
        "efficiency": efficiency(),
        "turbulentViscosity": turbulent_viscosity(),
        "parameterCounts": parameter_counts(),
        "evidenceCounts": evidence_counts(),
        "pulsarBaseline": pulsar_baseline(),
        "entropyCore": entropy_core(),
        "dimensionalBoundaries": dimensional_boundaries(),
        "evidenceBoundaries": evidence_boundaries(),
        "evidenceUpgrade": False,
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
