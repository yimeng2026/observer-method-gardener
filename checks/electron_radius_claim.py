#!/usr/bin/env python3
"""Arithmetic checks for classical electron-radius and electrostatic-model claims."""
from __future__ import annotations

import json
import math

POST_INPUTS = {
    "e": 1.602e-19,
    "m_e": 9.109e-31,
    "c": 3.0e8,
    "epsilon_0": 8.854e-12,
}

CODATA_2022 = {
    "e": 1.602176634e-19,
    "m_e": 9.1093837139e-31,
    "c": 299792458.0,
    "epsilon_0": 8.8541878188e-12,
}

HBAR = 6.62607015e-34 / (2 * math.pi)


def _require_positive(**values: float) -> None:
    if any(not math.isfinite(value) or value <= 0 for value in values.values()):
        raise ValueError("all physical inputs must be finite and positive")


def classical_electron_radius(e: float, m_e: float, c: float, epsilon_0: float) -> float:
    """Return e^2/(4*pi*epsilon_0*m_e*c^2), a defined electromagnetic scale."""
    _require_positive(e=e, m_e=m_e, c=c, epsilon_0=epsilon_0)
    return e**2 / (4 * math.pi * epsilon_0 * m_e * c**2)


def shell_outside_field_energy(radius: float, coulomb_k: float, charge: float) -> float:
    """Integrate (epsilon_0 E^2/2) outside a thin spherical charged shell."""
    _require_positive(radius=radius, coulomb_k=coulomb_k, charge=charge)
    return coulomb_k * charge**2 / (2 * radius)


def uniform_solid_self_energy(radius: float, coulomb_k: float, charge: float) -> float:
    """Return the self-energy 3*k*Q^2/(5*R) of a uniform solid charged sphere."""
    _require_positive(radius=radius, coulomb_k=coulomb_k, charge=charge)
    return 3 * coulomb_k * charge**2 / (5 * radius)


def surface_speed_for_uniform_sphere_spin(radius: float, m_e: float) -> float:
    """Classical equatorial speed when I*omega=hbar/2 and I=(2/5)mR^2."""
    _require_positive(radius=radius, m_e=m_e)
    return 5 * HBAR / (4 * m_e * radius)


def main() -> None:
    post_radius = classical_electron_radius(**POST_INPUTS)
    reference_radius = classical_electron_radius(**CODATA_2022)
    spin_speed = surface_speed_for_uniform_sphere_spin(reference_radius, CODATA_2022["m_e"])
    print(json.dumps({
        "schemaVersion": "electron-radius-arithmetic/v1",
        "sourceIds": ["9434307215"],
        "postInputsRadiusM": post_radius,
        "postInputsRadiusFm": post_radius * 1e15,
        "codataInputsRadiusM": reference_radius,
        "codataReferenceRadiusM": 2.8179403205e-15,
        "displayedConversionFm": 0.2818,
        "correctConversionFm": post_radius * 1e15,
        "shellOutsideFieldEnergy": "k*Q^2/(2*R)",
        "uniformSolidSelfEnergy": "3*k*Q^2/(5*R)",
        "uniformSphereSpinSurfaceSpeedOverC": spin_speed / CODATA_2022["c"],
        "experimentalElectronRadiusMeasured": False,
        "scope": "Arithmetic and stated classical models only; no physical electron boundary is inferred.",
        "evidenceUpgrade": False,
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
