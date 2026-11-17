#!/usr/bin/env python3
"""Minimal two-body Coulomb baseline and post-scalar magnetic scale checks."""
from __future__ import annotations

import json
import math

C = 299792458.0
E_CHARGE = 1.602176634e-19
EPSILON_0 = 8.8541878188e-12
M_E = 9.1093837139e-31
M_P = 1.67262192595e-27
R_BOHR = 5.29177210544e-11


def _positive(**values):
    if any(not math.isfinite(value) or value <= 0 for value in values.values()):
        raise ValueError("all physical inputs must be finite and positive")


def magnetic_coulomb_ratio(v1: float, v2: float, c: float = C) -> float:
    """Ratio implied by the post's scalar F_B/F_C, using mu0=1/(epsilon0*c^2)."""
    _positive(v1=v1, v2=v2, c=c)
    return v1 * v2 / c**2


def coulomb_circular_orbit(
    m_p: float = M_P,
    m_e: float = M_E,
    r: float = R_BOHR,
    e: float = E_CHARGE,
    epsilon_0: float = EPSILON_0,
    c: float = C,
) -> dict[str, float]:
    """Circular Coulomb-only baseline, not a solution of the unclosed magnetic model."""
    _positive(m_p=m_p, m_e=m_e, r=r, e=e, epsilon_0=epsilon_0, c=c)
    k = 1 / (4 * math.pi * epsilon_0)
    reduced_mass = m_p * m_e / (m_p + m_e)
    relative_speed = math.sqrt(k * e**2 / (reduced_mass * r))
    electron_speed = m_p * relative_speed / (m_p + m_e)
    proton_speed = m_e * relative_speed / (m_p + m_e)
    return {
        "reducedMass": reduced_mass,
        "relativeSpeed": relative_speed,
        "electronSpeed": electron_speed,
        "protonSpeed": proton_speed,
        "coulombForce": k * e**2 / r**2,
        "energy": -k * e**2 / (2 * r),
        "angularMomentum": reduced_mass * r * relative_speed,
        "postScalarMagneticRatio": magnetic_coulomb_ratio(electron_speed, proton_speed, c),
    }


def main() -> None:
    print(json.dumps({
        "schemaVersion": "coulomb-lorentz-model-baseline/v1",
        "sourceIds": ["9430823962"],
        "circularCoulombBaseline": coulomb_circular_orbit(),
        "scalarMagneticCoulombRatioFormula": "v1*v2/c^2",
        "closedDifferentialEquationProvided": False,
        "solutionImageProvided": False,
        "quantumRelativityOrAwardEstablished": False,
        "evidenceUpgrade": False,
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
