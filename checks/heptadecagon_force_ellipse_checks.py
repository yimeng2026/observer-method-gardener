#!/usr/bin/env python3
"""High-precision checks for the 2025-12-20 mathematics and mechanics post."""
from __future__ import annotations

import json

import mpmath as mp


def heptadecagon_radicals() -> dict[str, str]:
    with mp.workdps(80):
        alpha = mp.sqrt(17)
        beta = mp.sqrt(34 - 2 * alpha)
        gamma = mp.sqrt(34 + 2 * alpha)
        delta_radicand = 17 + 3 * alpha - beta - 2 * gamma
        delta = mp.sqrt(delta_radicand)
        numerator = -1 + alpha + beta + 2 * delta
        cosine = numerator / 16
        tangent = mp.sqrt(256 - numerator**2) / numerator
        direct_cosine = mp.cos(2 * mp.pi / 17)
        direct_tangent = mp.tan(2 * mp.pi / 17)
        return {
            "deltaRadicand": mp.nstr(delta_radicand, 65),
            "radicalCosine": mp.nstr(cosine, 65),
            "radicalTangent": mp.nstr(tangent, 65),
            "directCosine": mp.nstr(direct_cosine, 65),
            "directTangent": mp.nstr(direct_tangent, 65),
            "cosineDifference": mp.nstr(cosine - direct_cosine, 25),
            "tangentDifference": mp.nstr(tangent - direct_tangent, 25),
        }


def constant_force_example() -> dict[str, str]:
    """Use gamma0=1.25 and qEL/(rest_mass*c^2)=0.5."""
    with mp.workdps(80):
        gamma0 = mp.mpf("1.25")
        final_gamma = gamma0 + mp.mpf("0.5")
        closed = mp.sqrt(final_gamma**2 - 1) - mp.sqrt(gamma0**2 - 1)
        integrated = mp.quad(
            lambda u: (gamma0 + u) / mp.sqrt((gamma0 + u)**2 - 1),
            [0, mp.mpf("0.5")],
        )
        initial_speed = mp.sqrt(1 - gamma0**-2)
        return {
            "initialGamma": mp.nstr(gamma0, 20),
            "finalGamma": mp.nstr(final_gamma, 20),
            "initialSpeedOverC": mp.nstr(initial_speed, 40),
            "closedNormalizedTime": mp.nstr(closed, 65),
            "integratedNormalizedTime": mp.nstr(integrated, 65),
            "newtonianNormalizedTime": mp.nstr(mp.sqrt(initial_speed**2 + 1) - initial_speed, 50),
        }


def ellipse_perimeter_checks() -> dict[str, str]:
    with mp.workdps(80):
        a = mp.mpf(2026)
        b = mp.mpf(1949)
        parameter = 1 - b**2 / a**2
        exact = 4 * a * mp.ellipe(parameter)
        direct = 4 * mp.quad(
            lambda t: mp.sqrt(a**2 * mp.sin(t)**2 + b**2 * mp.cos(t)**2),
            [0, mp.pi / 2],
        )
        transformed = 4 * b**2 / a * mp.quad(
            lambda t: t**2 / mp.sqrt((t**2 - 1) * (1 - b**2 * t**2 / a**2)),
            [1, a / b],
        )
        return {
            "eccentricity": mp.nstr(mp.sqrt(parameter), 50),
            "parameter": mp.nstr(parameter, 50),
            "exact": mp.nstr(exact, 65),
            "directIntegral": mp.nstr(direct, 65),
            "wolframTransformedIntegral": mp.nstr(transformed, 65),
        }


def main() -> None:
    print(json.dumps({
        "schemaVersion": "heptadecagon-force-ellipse-checks/v1",
        "sourceIds": ["10318708655"],
        "heptadecagon": heptadecagon_radicals(),
        "constantForce": constant_force_example(),
        "ellipse": ellipse_perimeter_checks(),
        "elementaryEllipseAntiderivativeEstablished": False,
        "evidenceUpgrade": False,
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
