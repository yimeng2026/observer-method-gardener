#!/usr/bin/env python3
"""Independent enumeration and heuristic evaluation for two Goldbach posts."""
from __future__ import annotations
import json
import math

TWIN_PRIME_2C = 1.32032363169373914


def primes_through(n: int) -> list[int]:
    if n < 2:
        return []
    sieve = bytearray(b"\x01") * (n + 1)
    sieve[:2] = b"\x00\x00"
    for p in range(2, math.isqrt(n) + 1):
        if sieve[p]:
            sieve[p * p:n + 1:p] = b"\x00" * (((n - p * p) // p) + 1)
    return [p for p in range(n + 1) if sieve[p]]


def goldbach_partitions(n: int) -> int:
    if n <= 2 or n % 2:
        raise ValueError("n must be an even integer greater than two")
    primes = set(primes_through(n))
    return sum(1 for p in primes if p <= n - p and n - p in primes)


def singular_series(n: int) -> float:
    result = 1.0
    remainder = n
    for p in primes_through(n):
        if p > 2 and remainder % p == 0:
            result *= (p - 1) / (p - 2)
            while remainder % p == 0:
                remainder //= p
    return result


def log_integral_from_two(n: int) -> float:
    if n <= 2:
        raise ValueError("integration upper bound must exceed two")
    intervals = max(20000, 2 * (n // 2))
    step = (n - 2) / intervals
    total = 0.0
    for index in range(intervals + 1):
        x = 2 + index * step
        weight = 1 if index in (0, intervals) else 4 if index % 2 else 2
        total += weight / math.log(x)
    return total * step / 3


def evaluate_formula(n: int) -> dict:
    hardy = TWIN_PRIME_2C * n / math.log(n)**2 * singular_series(n)
    integral = log_integral_from_two(n)
    li_two = 1.04516378011749
    single = 0.849600 * (integral + li_two - n / math.log(n))
    literal = 0.849600 * (integral - n / math.log(n))
    actual = goldbach_partitions(n)
    return {
        "n": n,
        "actualUnorderedPartitions": actual,
        "hardyLittlewood": hardy,
        "singleTermEstimate": single,
        "literalIntegralEstimate": literal,
        "hardyLittlewoodRelativeError": abs(hardy - actual) / actual,
        "singleTermRelativeError": abs(single - actual) / actual,
        "proofOfGoldbach": False,
    }


def main() -> None:
    samples = [evaluate_formula(n) for n in (100, 1000, 2000, 5000, 10000, 100000)]
    print(json.dumps({
        "schemaVersion": "goldbach-estimate-arithmetic/v1",
        "sourceIds": ["9966466979", "9966450809"],
        "samples": samples,
        "scope": "Finite enumeration and numerical heuristics only; no proof or asymptotic error bound is supplied.",
        "evidenceUpgrade": False,
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
