#!/usr/bin/env python3
"""Independent arithmetic for the displayed consecutive-twin-pair gap formulas."""
from __future__ import annotations
from fractions import Fraction
import json
import math


def twin_pairs(limit: int) -> list[int]:
    """Return first members p such that p and p+2 are prime, within the finite limit."""
    if limit < 3:
        return []
    sieve = bytearray([1]) * (limit + 1)
    sieve[0:2] = b"\x00\x00"
    for p in range(2, math.isqrt(limit) + 1):
        if sieve[p]:
            sieve[p * p:limit + 1:p] = b"\x00" * (((limit - p * p) // p) + 1)
    return [p for p in range(3, limit - 1, 2) if sieve[p] and sieve[p + 2]]


def product_c2(p: int) -> Fraction:
    """The post's p-dependent product over odd primes 3<=q<=sqrt(p)."""
    if p < 1:
        raise ValueError("p must be positive")
    result = Fraction(1)
    for q in range(3, math.isqrt(p) + 1, 2):
        if all(q % divisor for divisor in range(2, math.isqrt(q) + 1)):
            result *= 1 - Fraction(1, (q - 1) ** 2)
    return result


def displayed_gap_bounds(p: int) -> dict:
    """Evaluate the displayed heuristic, without treating it as a proved bound."""
    c2 = float(product_c2(p))
    log_squared = math.log(p) ** 2
    return {
        "c2": c2,
        "mean": 6 * (1 + log_squared / (12 * c2)),
        "upper": 6 * (1 + log_squared / (6 * c2)),
        "asymptoticMeanMainTerm": log_squared / (2 * c2),
        "status": "displayed_heuristic_not_universal_proof",
    }


def main() -> None:
    pairs = twin_pairs(110)
    result = displayed_gap_bounds(71)
    print(json.dumps({
        "schemaVersion": "twin-prime-gap-check/v1",
        "sourceId": "9542406218",
        "p71ProductExact": str(product_c2(71)),
        "p71DisplayedHeuristic": result,
        "p71ActualNextPairFirstMember": pairs[pairs.index(71) + 1],
        "p71ActualGap": pairs[pairs.index(71) + 1] - 71,
        "correctedUpperRounded": round(result["upper"]),
        "rigorousTwinPrimeConjectureProof": False,
        "evidenceUpgrade": False,
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
