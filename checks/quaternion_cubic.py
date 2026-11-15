#!/usr/bin/env python3
"""Executable checks for x^3+1=0 over Hamilton quaternions."""
from __future__ import annotations
import json
import math

Quaternion = tuple[float, float, float, float]


def multiply(a: Quaternion, b: Quaternion) -> Quaternion:
    aw, ax, ay, az = a
    bw, bx, by, bz = b
    return (
        aw * bw - ax * bx - ay * by - az * bz,
        aw * bx + ax * bw + ay * bz - az * by,
        aw * by - ax * bz + ay * bw + az * bx,
        aw * bz + ax * by - ay * bx + az * bw,
    )


def cubic_residual(x: Quaternion) -> Quaternion:
    cube = multiply(multiply(x, x), x)
    return (cube[0] + 1.0, cube[1], cube[2], cube[3])


def quaternion_norm(x: Quaternion) -> float:
    return math.sqrt(sum(value * value for value in x))


def quadratic_root_from_unit_pure(unit: tuple[float, float, float]) -> Quaternion:
    if len(unit) != 3 or any(not math.isfinite(float(value)) for value in unit):
        raise ValueError("A finite three-component pure direction is required")
    norm = math.sqrt(sum(float(value) ** 2 for value in unit))
    if abs(norm - 1.0) > 1e-9:
        raise ValueError("The pure direction must have unit norm")
    scale = math.sqrt(3.0) / 2.0
    return (0.5, *(scale * float(value) for value in unit))


def main() -> None:
    directions = [(1, 0, 0), (0, 1, 0), (0, 0, 1), tuple(value / math.sqrt(14) for value in (1, 2, 3))]
    result = {
        "schemaVersion": "quaternion-cubic-check/v1",
        "sourceId": "11079846507",
        "counterexample": {"x": [0, 1, 0, 0], "xCubedPlusOne": cubic_residual((0, 1, 0, 0))},
        "minusOneResidualNorm": quaternion_norm(cubic_residual((-1, 0, 0, 0))),
        "familyResidualNorms": [quaternion_norm(cubic_residual(quadratic_root_from_unit_pure(direction))) for direction in directions],
        "completeSolutionSet": "x=-1 or x=1/2+(sqrt(3)/2)u, where u is pure imaginary and |u|=1",
        "scope": "Hamilton quaternion algebra only; no physical interpretation or evidence upgrade",
        "evidenceUpgrade": False,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
