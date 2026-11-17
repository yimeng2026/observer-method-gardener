#!/usr/bin/env python3
"""Distinguish turn radius, bank angle, chord geometry and load factor."""
from __future__ import annotations
import json
import math


def turn_radius(speed, acceleration):
    return speed**2 / acceleration


def coordinated_turn_bank(load_factor):
    """Level coordinated turn: N/mg=sec(bank)."""
    if load_factor < 1:
        raise ValueError("Load factor must be at least one")
    return math.degrees(math.acos(1 / load_factor))


def chord_geometry_angle(radius, aircraft_length):
    """Angle satisfying r*sin(theta)=L/2, in degrees; not an angle of attack."""
    return math.degrees(math.asin(aircraft_length / (2 * radius)))


def load_factor_from_net_acceleration(centripetal_g):
    """Support-force magnitude when gravity is perpendicular to centripetal acceleration."""
    return math.sqrt(centripetal_g**2 + 1)


def main() -> None:
    print(json.dumps({
        "schemaVersion": "turn-performance-check/v1",
        "sourceId": "9457167593",
        "radiusAt1020And49gUsing9.8": turn_radius(1020, 49 * 9.8),
        "radiusAt1029And9gUsing9.81": turn_radius(1029, 9 * 9.81),
        "coordinatedBankAt9gDegrees": coordinated_turn_bank(9),
        "coordinatedBankAt50gDegrees": coordinated_turn_bank(50),
        "supportLoadFrom49gCentripetal": load_factor_from_net_acceleration(49),
        "chordAngleIsAngleOfAttack": False,
        "machNumberAloneProvesPilotFatality": False,
        "highManeuverEnvelopeUnrestricted": False,
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
