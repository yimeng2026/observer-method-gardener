#!/usr/bin/env python3
"""Cross-check prime-counting estimates without presenting them as exact counts.

Requires mpmath for Li, Ei and Riemann R; small Legendre checks use stdlib only.
"""
from __future__ import annotations
from fractions import Fraction
import json
import math
import mpmath as mp


def _primes(limit: int) -> list[int]:
    if limit < 2:
        return []
    sieve = bytearray([1]) * (limit + 1)
    sieve[0:2] = b"\x00\x00"
    for p in range(2, math.isqrt(limit) + 1):
        if sieve[p]:
            sieve[p * p:limit + 1:p] = b"\x00" * (((limit - p * p) // p) + 1)
    return [p for p in range(2, limit + 1) if sieve[p]]


def evaluate_estimates(x: str) -> dict:
    """Evaluate distinct smooth approximations at the same positive real x>1."""
    with mp.workdps(70):
        value = mp.mpf(x)
        if value <= 1:
            raise ValueError("x must exceed 1")
        logarithm = mp.log(value)
        return {
            "xOverLog": mp.nstr(value / logarithm, 40),
            "li": mp.nstr(mp.li(value), 40),
            "scaledEi": mp.nstr(mp.exp(-1) * mp.ei(1 + logarithm), 40),
            "riemannR": mp.nstr(mp.riemannr(value), 40),
            "exactPi": None,
            "status": "smooth_estimates_not_exact_counts",
        }


def sieve_product(x: int) -> Fraction:
    """The naive product x*product_{p<=sqrt(x)}(1-1/p), not pi(x)."""
    if isinstance(x, bool) or not isinstance(x, int) or x < 1:
        raise ValueError("x must be a positive integer")
    result = Fraction(x)
    for prime in _primes(math.isqrt(x)):
        result *= 1 - Fraction(1, prime)
    return result


def legendre_pi(x: int) -> int:
    """Exact Legendre inclusion-exclusion for bounded small inputs."""
    if isinstance(x, bool) or not isinstance(x, int) or not 1 <= x <= 10000:
        raise ValueError("This bounded check accepts integer inputs from 1 to 10000")
    primes = _primes(math.isqrt(x))
    survivors = x

    def extend(start: int, product: int, sign: int) -> None:
        nonlocal survivors
        for index in range(start, len(primes)):
            combined = product * primes[index]
            if combined > x:
                break
            survivors += sign * (x // combined)
            extend(index + 1, combined, -sign)

    extend(0, 1, -1)
    return survivors + len(primes) - 1


def mertens_prefactor() -> float:
    """The asymptotic ratio of x*product to x/log(x), namely 2 exp(-gamma)."""
    with mp.workdps(50):
        return float(2 * mp.exp(-mp.euler))


def main() -> None:
    large = {str(exponent): evaluate_estimates(f"1e{exponent}")["riemannR"] for exponent in [30, 50, 100, 1000]}
    print(json.dumps({
        "schemaVersion": "prime-counting-estimates/v1",
        "sourceId": "9500700895",
        "x8e25": evaluate_estimates("8e25"),
        "referencePi1e25": 176846309399143769411680,
        "smallCounterexample": {
            "x": 25,
            "exactLegendrePi": legendre_pi(25),
            "naiveProductExact": str(sieve_product(25)),
            "naiveProductFloat": float(sieve_product(25)),
        },
        "mertensPrefactor": mertens_prefactor(),
        "largeRiemannApproximations": large,
        "largeApproximationsAreExactPi": False,
        "evidenceUpgrade": False,
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
