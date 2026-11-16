#!/usr/bin/env python3
"""Algebraic and numerical counterchecks for the generalized-Newton post."""
from __future__ import annotations
import json
import math


def polar_acceleration(*, r: float, r_dot: float, r_ddot: float, theta_dot: float, theta_ddot: float) -> tuple[float, float]:
    """Coordinate acceleration in an inertial polar basis, not a covariant derivative."""
    return r_ddot - r * theta_dot**2, r * theta_ddot + 2 * r_dot * theta_dot


def relativistic_parallel_perpendicular_force(
    *, rest_mass: float, speed_ratio: float, parallel_acceleration: float, perpendicular_acceleration: float
) -> tuple[float, float]:
    """F = gamma^3 m0 a_parallel + gamma m0 a_perp, in units c=1."""
    gamma = 1 / math.sqrt(1 - speed_ratio**2)
    return gamma**3 * rest_mass * parallel_acceleration, gamma * rest_mass * perpendicular_acceleration


def transverse_cross_product(*, rest_mass: float, speed: float, radius: float) -> tuple[float, float, float]:
    """The displayed v cross d(v-hat)/dt at v=(v,0), d(v-hat)/dt=(0,v/r)."""
    return 0.0, 0.0, rest_mass * speed**2 / radius


def schwarzschild_radial_coefficients(*, r: float, g: float = 1.0, m: float = 1.0, c: float = 1.0) -> dict[str, float]:
    """Coefficients of (dt/dtau)^2 and (dr/dtau)^2 in d^2r/dtau^2.

    Derived directly from A=1-2GM/(c^2r), g_tt=-Ac^2 and g_rr=A^-1:
    Gamma^r_tt=GM*A/r^2 and Gamma^r_rr=-GM/(c^2*r^2*A).
    """
    a = 1 - 2 * g * m / (c**2 * r)
    if a <= 0:
        raise ValueError("Exterior Schwarzschild coordinates require A>0")
    return {"time": -g * m * a / r**2, "radius": g * m / (c**2 * r**2 * a)}


def displayed_radial_coefficients(*, r: float, g: float = 1.0, m: float = 1.0, c: float = 1.0) -> dict[str, float]:
    """The A^-1 and A^-2 coefficients displayed in images 21-22."""
    a = 1 - 2 * g * m / (c**2 * r)
    if a <= 0:
        raise ValueError("Exterior Schwarzschild coordinates require A>0")
    return {"time": -g * m / (r**2 * a), "radius": g * m / (c**2 * r**2 * a**2)}


def proper_time_factor(*, a: float, radial_speed: float, inverse_metric_denominator: bool) -> float:
    """d(tau)/dt for equatorial radial motion; c=1, theta_dot=0.

    Exact line-element form has radial_speed^2/A. The displayed formula omits A.
    """
    denominator = a if inverse_metric_denominator else 1.0
    radicand = a - radial_speed**2 / denominator
    if radicand <= 0:
        raise ValueError("The specified radial motion is not timelike")
    return math.sqrt(radicand)


def main() -> None:
    print(json.dumps({
        "schemaVersion": "generalized-newton-check/v1",
        "sourceId": "9964539659",
        "correctRadialCoefficientsAtR4": schwarzschild_radial_coefficients(r=4.0),
        "displayedRadialCoefficientsAtR4": displayed_radial_coefficients(r=4.0),
        "crossProductCounterexample": transverse_cross_product(rest_mass=1.0, speed=3.0, radius=2.0),
        "newPhysicsValidated": False,
        "evidenceUpgrade": False,
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
