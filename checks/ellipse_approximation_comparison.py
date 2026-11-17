#!/usr/bin/env python3
"""Compare exact ellipse perimeter, two Ramanujan approximations, and 4a."""
from __future__ import annotations

import json

import mpmath as mp


def _axes(a, b):
    a, b = mp.mpf(a), mp.mpf(b)
    if not a >= b > 0:
        raise ValueError("Require a>=b>0")
    return a, b


def ellipse_exact(a, b) -> mp.mpf:
    """Return 4a*E(1-b^2/a^2), using the parameter convention."""
    with mp.workdps(80):
        a, b = _axes(a, b)
        return 4 * a * mp.ellipe(1 - b**2 / a**2)


def ramanujan_first(a, b) -> mp.mpf:
    with mp.workdps(80):
        a, b = _axes(a, b)
        return mp.pi * (3 * (a + b) - mp.sqrt((3 * a + b) * (a + 3 * b)))


def ramanujan_second(a, b) -> mp.mpf:
    with mp.workdps(80):
        a, b = _axes(a, b)
        h = ((a - b) / (a + b)) ** 2
        return mp.pi * (a + b) * (1 + 3 * h / (10 + mp.sqrt(4 - 3 * h)))


def _sample(a, b) -> dict[str, str]:
    exact = ellipse_exact(a, b)
    first = ramanujan_first(a, b)
    second = ramanujan_second(a, b)
    four_a = 4 * mp.mpf(a)
    return {
        "exact": mp.nstr(exact, 65),
        "ramanujanFirst": mp.nstr(first, 65),
        "ramanujanSecond": mp.nstr(second, 65),
        "fourA": mp.nstr(four_a, 30),
        "firstMinusExact": mp.nstr(first - exact, 35),
        "secondMinusExact": mp.nstr(second - exact, 35),
        "fourAMinusExact": mp.nstr(four_a - exact, 35),
        "fourARelativeError": mp.nstr(abs(four_a - exact) / exact, 20),
    }


def main() -> None:
    near = _sample(2025, 2024)
    extreme = _sample(20251949, 1)
    near["ai12750Point04MinusExact"] = mp.nstr(mp.mpf("12750.04") - ellipse_exact(2025, 2024), 40)
    print(json.dumps({
        "schemaVersion": "ellipse-approximation-comparison/v1",
        "sourceIds": ["9432818493"],
        "nearCircle2025And2024": near,
        "extreme20251949And1": extreme,
        "orbitalPeriodDeterminedByEllipsePerimeter": False,
        "worldRankingEstablished": False,
        "evidenceUpgrade": False,
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
