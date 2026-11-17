#!/usr/bin/env python3
"""Standard thermal baseline and a classical Coulomb Gibbs divergence certificate."""
from __future__ import annotations
import json
import math


def maxwell_velocity_pdf(v, mass, thermal_energy):
    """One-dimensional Maxwell velocity pdf; thermal_energy=k_B*T."""
    return math.sqrt(mass / (2 * math.pi * thermal_energy)) * math.exp(-mass * v**2 / (2 * thermal_energy))


def coulomb_small_radius_lower_bound(a, cutoff, upper):
    """Lower bound for the divergent radial Gibbs integral.

    For a=beta*k_e*e^2>0 and 0<r<upper, exp(a/r)>=a^4/(24*r^4).
    Thus r^2*exp(a/r)>=a^4/(24*r^2), whose integral from cutoff to
    upper is a^4/24*(1/cutoff-1/upper).  It diverges as cutoff->0.
    """
    if a <= 0 or not 0 < cutoff < upper:
        raise ValueError("Require a>0 and 0<cutoff<upper")
    return a**4 / 24 * (1 / cutoff - 1 / upper)


def total_momentum(m1, v1, m2, v2):
    return m1 * v1 + m2 * v2


def main() -> None:
    print(json.dumps({
        "schemaVersion": "classical-coulomb-gibbs-check/v1",
        "sourceId": "9477069063",
        "maxwellExample": {"mass": 2.0, "thermalEnergy": 3.0, "variance": 1.5},
        "coulombSmallRadiusLowerBoundAt0.1": coulomb_small_radius_lower_bound(1.0, 0.1, 1.0),
        "coulombSmallRadiusLowerBoundAt0.01": coulomb_small_radius_lower_bound(1.0, 0.01, 1.0),
        "classicalInfiniteSpaceCoulombGibbsNormalizable": False,
        "oppositeVelocityTotalMomentumExample": total_momentum(1.0, 1.0, 2.0, -1.0),
        "quantumHydrogenGroundStateDerivedFromClassicalNoise": False,
        "darkMatterOrDarkEnergyModelEstablished": False,
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
