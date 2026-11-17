#!/usr/bin/env python3
"""Reproduce finite prime-constellation checks from post 9494567904."""
from __future__ import annotations
import json
import math


def residue_coverage(offsets, prime):
    """Return the residue classes occupied by an offset pattern modulo prime."""
    return sorted({offset % prime for offset in offsets})


def consecutive_prime_tuples(limit, k, allowed_gaps):
    """Enumerate k consecutive primes with every gap in allowed_gaps."""
    sieve = bytearray(b"\x01") * (limit + 1)
    if limit >= 0:
        sieve[0] = 0
    if limit >= 1:
        sieve[1] = 0
    for candidate in range(2, math.isqrt(limit) + 1):
        if sieve[candidate]:
            start = candidate * candidate
            sieve[start:limit + 1:candidate] = b"\x00" * (((limit - start) // candidate) + 1)
    primes = [number for number in range(2, limit + 1) if sieve[number]]
    allowed = set(allowed_gaps)
    return [
        tuple(primes[start:start + k])
        for start in range(len(primes) - k + 1)
        if all(
            primes[index + 1] - primes[index] in allowed
            for index in range(start, start + k - 1)
        )
    ]


def displayed_count_estimate(x, constant):
    """Evaluate the image's displayed C*x/log(x)^8 expression."""
    return constant * x / math.log(x)**8


def main() -> None:
    unique = consecutive_prime_tuples(100000, 8, (2, 4))
    dense = consecutive_prime_tuples(100, 8, (2, 4, 6))
    ai_offsets = (0, 2, 6, 8, 12, 14, 18, 20)
    estimate = displayed_count_estimate(10**12, 0.00037)
    print(json.dumps({
        "schemaVersion": "dense-prime-constellation-check/v1",
        "sourceId": "9494567904",
        "twoFourEightTuplesBelow100000": unique,
        "twoFourSixEightTuplesBelow100": dense,
        "aiOffsets": ai_offsets,
        "aiResiduesModulo3": residue_coverage(ai_offsets, 3),
        "aiResiduesModulo5": residue_coverage(ai_offsets, 5),
        "aiPatternAdmissible": False,
        "displayedC": 0.00037,
        "displayedX": 10**12,
        "displayedFormulaValue": estimate,
        "displayedClaimedValue": 1.06,
        "claimedOverComputedRatio": 1.06 / estimate,
        "finiteExamplesDoNotProveInfinity": True,
        "kTupleConjectureEstablishedByPost": False,
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
