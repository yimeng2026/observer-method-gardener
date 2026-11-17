#!/usr/bin/env python3
"""Check prime-quadruplet correction factors and counting conventions."""
from __future__ import annotations
from fractions import Fraction
import json
import math

OFFSETS = (0, 2, 6, 8)


def primes_up_to(limit):
    sieve = bytearray(b"\x01") * (limit + 1)
    sieve[0:min(2, limit + 1)] = b"\x00" * min(2, limit + 1)
    for candidate in range(2, math.isqrt(limit) + 1):
        if sieve[candidate]:
            start = candidate * candidate
            sieve[start:limit + 1:candidate] = b"\x00" * (((limit - start) // candidate) + 1)
    return [number for number in range(2, limit + 1) if sieve[number]]


def small_prime_factors():
    """Compute local Hardy-Littlewood factors from the actual residues."""
    result = {}
    for prime in (2, 3, 5, 7):
        occupied = len({offset % prime for offset in OFFSETS})
        result[prime] = (1 - Fraction(occupied, prime)) / (1 - Fraction(1, prime))**4
    return result


def quadruplet_constant(prime_limit):
    """Truncate the displayed convergent Euler product at prime_limit."""
    constant = 27 / 2
    for prime in primes_up_to(prime_limit):
        if prime >= 5:
            constant *= prime**3 * (prime - 4) / (prime - 1)**4
    return constant


def prime_quadruplets(start_limit):
    """Enumerate starts n<=start_limit for which all four offsets are prime."""
    primes = primes_up_to(start_limit + max(OFFSETS))
    prime_set = set(primes)
    return [
        tuple(start + offset for offset in OFFSETS)
        for start in primes
        if start <= start_limit and all(start + offset in prime_set for offset in OFFSETS)
    ]


def count_heuristics(x, constant):
    """Distinguish local start density from the expected cumulative count."""
    local_density = constant / math.log(x)**4
    return {
        "localDensity": local_density,
        "cumulativeCount": x * local_density,
    }


def main() -> None:
    heuristics = count_heuristics(10**6, 4.15118)
    print(json.dumps({
        "schemaVersion": "prime-quadruplet-check/v1",
        "sourceId": "9494507686",
        "offsets": OFFSETS,
        "smallPrimeFactors": {str(prime): str(factor) for prime, factor in small_prime_factors().items()},
        "smallPrimePrefactor": str(small_prime_factors()[2] * small_prime_factors()[3]),
        "constantPrimeLimit": 1000000,
        "truncatedConstant": quadruplet_constant(1000000),
        "displayedConstant": 4.15118,
        "quadrupletStartsThrough200": prime_quadruplets(200),
        "xForCountingExample": 10**6,
        **heuristics,
        "wholeIntervalProbabilityEqualsLocalDensity": False,
        "finiteExamplesProveInfinitude": False,
        "hardyLittlewoodConjectureProvenByPost": False,
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
