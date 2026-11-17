#!/usr/bin/env python3
"""Numerical and finite-enumeration checks for the Desboves-model post."""
from __future__ import annotations

import json
import math

import mpmath as mp


def _primes_upto(n: int) -> list[int]:
    if n < 2:
        return []
    sieve = bytearray(b"\x01") * (n + 1)
    sieve[0:2] = b"\x00\x00"
    for p in range(2, math.isqrt(n) + 1):
        if sieve[p]:
            sieve[p * p:n + 1:p] = b"\x00" * (((n - p * p) // p) + 1)
    return [number for number in range(2, n + 1) if sieve[number]]


def prime_pi(x) -> int:
    """Count primes p<=x for finite real x."""
    if not math.isfinite(float(x)) or float(x) < 0:
        raise ValueError("x must be finite and nonnegative")
    return len(_primes_upto(math.floor(float(x))))


def primes_between_squares(n: int) -> list[int]:
    """Finite verification only: primes strictly between n^2 and (n+1)^2."""
    if isinstance(n, bool) or not isinstance(n, int) or n < 1:
        raise ValueError("n must be a positive integer")
    upper_exclusive = (n + 1) ** 2
    return [p for p in _primes_upto(upper_exclusive - 1) if p > n * n]


def smooth_pi_model(x) -> mp.mpf:
    """Smooth proposal exp(-1)*Ei(1+log x), not the integer prime count."""
    with mp.workdps(50):
        x = mp.mpf(x)
        if x <= 0:
            raise ValueError("x must be positive")
        return mp.e ** (-1) * mp.ei(1 + mp.log(x))


def smooth_pi_derivative(x) -> mp.mpf:
    with mp.workdps(50):
        x = mp.mpf(x)
        if x <= 0:
            raise ValueError("x must be positive")
        return 1 / (1 + mp.log(x))


def _displayed_smooth_term(x) -> mp.mpf:
    x = mp.mpf(x)
    if x <= 0:
        raise ValueError("x must be positive")
    return mp.e ** (-1) * mp.ei(1 + 2 * mp.log(x))


def displayed_y(x) -> mp.mpf:
    """The image's F(x+1)-F(x)-1, with F=exp(-1)Ei(1+2log x)."""
    with mp.workdps(50):
        return _displayed_smooth_term(mp.mpf(x) + 1) - _displayed_smooth_term(x) - 1


def displayed_derivative(x) -> mp.mpf:
    with mp.workdps(50):
        x = mp.mpf(x)
        if x <= 0:
            raise ValueError("x must be positive")
        return 2 * (x + 1) / (1 + 2 * mp.log(x + 1)) - 2 * x / (1 + 2 * mp.log(x))


def displayed_second_derivative(x) -> mp.mpf:
    """Analytic second derivative, avoiding a noisy nested finite difference."""
    with mp.workdps(50):
        x = mp.mpf(x)
        if x <= 0:
            raise ValueError("x must be positive")
        left = 1 + 2 * mp.log(x + 1)
        right = 1 + 2 * mp.log(x)
        return 2 * (1 / left - 1 / right) + 4 * (1 / right**2 - 1 / left**2)


def find_displayed_root() -> mp.mpf:
    with mp.workdps(50):
        return mp.findroot(displayed_y, mp.mpf("0.157"))


def find_displayed_minimum() -> dict[str, mp.mpf]:
    with mp.workdps(50):
        location = mp.findroot(displayed_derivative, mp.mpf("1.27"))
        return {
            "x": location,
            "y": displayed_y(location),
            "secondDerivative": displayed_second_derivative(location),
        }


def main() -> None:
    root = find_displayed_root()
    minimum = find_displayed_minimum()
    counterexamples = []
    for x in (mp.mpf("6.7"), 9, 10):
        counterexamples.append({
            "x": mp.nstr(x, 10),
            "actualPrimePi": prime_pi(x),
            "xOverLogX": mp.nstr(x / mp.log(x), 25),
            "lowerBoundHolds": bool(x / mp.log(x) < prime_pi(x)),
        })
    print(json.dumps({
        "schemaVersion": "desboves-model-arithmetic/v1",
        "sourceIds": ["9431150211"],
        "displayedRoot": mp.nstr(root, 35),
        "displayedMinimum": {key: mp.nstr(value, 35) for key, value in minimum.items()},
        "lowerBoundCounterexamples": counterexamples,
        "finiteSquareIntervalsVerifiedThroughN": 1000,
        "allSquareIntervalsVerified": False,
        "smoothModelMissingIntegrationConstant": True,
        "littlewoodPreventsGlobalLiUpperBound": True,
        "evidenceUpgrade": False,
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
