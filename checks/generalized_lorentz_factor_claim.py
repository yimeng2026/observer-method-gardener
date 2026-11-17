#!/usr/bin/env python3
"""Algebra checks for the displayed generalized Lorentz-factor claims."""
from __future__ import annotations
import json
import math


def work_energy_state(work, rest_mass, c):
    """From-rest relativistic energy state under external work."""
    gamma = 1 + work / (rest_mass * c**2)
    if gamma < 1:
        raise ValueError("A from-rest massive particle cannot have gamma<1")
    speed = c * math.sqrt(1 - 1 / gamma**2)
    return {
        "gamma": gamma,
        "speed": speed,
        "kineticEnergy": (gamma - 1) * rest_mass * c**2,
    }


def coulomb_mass_ratios(k_e2, rest_mass, c, reference_radius, radius):
    """Compare direct integration of c^2 dm=-k_e2/r^2 dr with the claimed exponential."""
    exponent = k_e2 / (rest_mass * c**2) * (1 / radius - 1 / reference_radius)
    return {
        "directIntegratedRatio": 1 + exponent,
        "claimedExponentialRatio": math.exp(exponent),
    }


def gravitational_potential_terms(gm, rest_mass, c, reference_radius, radius):
    """Evaluate the exponential model and its correctly retained first-order potential."""
    alpha = gm / c**2
    exponent = alpha * (1 / radius - 1 / reference_radius)
    exact = -gm * rest_mass * math.exp(exponent) / radius
    first_order = -gm * rest_mass * (1 + exponent) / radius
    missing_radius_form = -gm * rest_mass * (1 + alpha / radius)
    return {
        "exactPotential": exact,
        "firstOrderPotential": first_order,
        "missingRadiusDisplayedForm": missing_radius_form,
    }


def main() -> None:
    print(json.dumps({
        "schemaVersion": "generalized-lorentz-factor-check/v1",
        "sourceId": "9487081127",
        "workExample": work_energy_state(4.5, 2.0, 3.0),
        "coulombExample": coulomb_mass_ratios(1.0, 1.0, 1.0, 2.0, 4.0),
        "potentialExample": gravitational_potential_terms(1.0, 1.0, 1.0, 2.0, 4.0),
        "independentRelativityUnificationEstablished": False,
        "mercuryPrecessionDerived": False,
        "evidenceUpgrade": False,
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
