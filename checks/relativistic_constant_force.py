#!/usr/bin/env python3
"""Constant-force relativistic dynamics and initial-condition counterchecks."""
from __future__ import annotations
import json
import math


def _inputs(v0, c, force, rest_mass):
    if c <= 0 or rest_mass <= 0 or force == 0:
        raise ValueError("Require c>0, rest mass>0 and nonzero force")
    if abs(v0) >= c:
        raise ValueError("Initial speed must be below c")


def constant_force_state(t, force, rest_mass, initial_speed, c=299792458.0):
    """Exact one-dimensional solution for F=dp/dt and p=gamma*m0*v."""
    _inputs(initial_speed, c, force, rest_mass)
    gamma0 = 1 / math.sqrt(1 - (initial_speed / c) ** 2)
    u = gamma0 * initial_speed + force * t / rest_mass
    gamma = math.sqrt(1 + (u / c) ** 2)
    v = u / gamma
    x = rest_mass * c**2 * (gamma - gamma0) / force
    return {
        "u": u,
        "v": v,
        "x": x,
        "gamma": gamma,
        "gamma0": gamma0,
        "momentum": rest_mass * u,
        "energy": gamma * rest_mass * c**2,
        "properTimeRate": 1 / gamma,
    }


def displayed_initial_residuals(force, rest_mass, initial_speed, c=299792458.0):
    """Evaluate the two displayed speed formulas and one position formula at t=0."""
    _inputs(initial_speed, c, force, rest_mass)
    gamma0 = 1 / math.sqrt(1 - (initial_speed / c) ** 2)
    speed_a = c**2 / force * (
        math.sqrt((gamma0 * rest_mass * initial_speed) ** 2 + (gamma0 * rest_mass * c) ** 2)
        - gamma0 * rest_mass * c
    )
    speed_b = (initial_speed / gamma0) / math.sqrt(1 + (initial_speed / (c * gamma0)) ** 2)
    position_a = rest_mass * c**2 / force * (math.sqrt(1 + (initial_speed / c) ** 2) - 1)
    return {"speedVersionA": speed_a, "speedVersionB": speed_b, "positionVersionA": position_a}


def displayed_mass_ratio(v, v0, c=299792458.0):
    """The displayed ratio equals gamma/gamma0, not gamma unless v0=0."""
    if c <= 0 or abs(v) >= c or abs(v0) >= c:
        raise ValueError("Require positive c and both speeds below c")
    return math.sqrt((1 - (v0 / c) ** 2) / (1 - (v / c) ** 2))


def main() -> None:
    state = constant_force_state(1.2, 3.0, 2.0, 2.0, 5.0)
    print(json.dumps({
        "schemaVersion": "relativistic-constant-force-check/v1",
        "sourceId": "9523710612",
        "example": state,
        "displayedInitialResiduals": displayed_initial_residuals(3.0, 2.0, 2.0, 5.0),
        "massRatioAtV08V006": displayed_mass_ratio(0.8, 0.6, 1.0),
        "workEnergyResidual": 3.0 * state["x"] - 2.0 * 5.0**2 * (state["gamma"] - state["gamma0"]),
        "independentDerivationOfSpecialRelativity": False,
        "newPhysicsValidated": False,
        "evidenceUpgrade": False,
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
