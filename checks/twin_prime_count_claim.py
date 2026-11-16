#!/usr/bin/env python3
"""Independent checks for twin-prime counting and gap heuristics."""
from __future__ import annotations
import json
import math
import mpmath as mp

if __package__:
    from .twin_prime_gap_claim import product_c2, twin_pairs
else:
    from twin_prime_gap_claim import product_c2, twin_pairs


def twin_count(limit: int) -> int:
    if isinstance(limit, bool) or not isinstance(limit, int) or limit < 2:
        raise ValueError("limit must be an integer of at least 2")
    return len(twin_pairs(limit))


def hardy_littlewood_estimate(x: int) -> dict:
    """Evaluate the conjectural smooth model with a proper lower limit of 2."""
    if isinstance(x, bool) or not isinstance(x, int) or x <= 2:
        raise ValueError("x must be an integer greater than 2")
    with mp.workdps(50):
        integral = mp.quad(lambda t: 1 / mp.log(t) ** 2, [2, x])
    c2 = float(product_c2(x))
    return {
        "integralFrom2": float(integral),
        "truncatedC2": c2,
        "truncatedEstimate": 2 * c2 * float(integral),
        "status": "hardy_littlewood_conjecture_not_proof",
    }


def clement_condition(p: int) -> bool:
    """Clement's finite criterion: 4[(p-1)!+1]+p == 0 mod p(p+2)."""
    if isinstance(p, bool) or not isinstance(p, int) or p < 3:
        raise ValueError("p must be an integer of at least 3")
    return (4 * (math.factorial(p - 1) + 1) + p) % (p * (p + 2)) == 0


def mean_gap_heuristic(p: int) -> float:
    """The smooth density-based gap estimate, not a derivative of the step count."""
    if isinstance(p, bool) or not isinstance(p, int) or p <= 2:
        raise ValueError("p must be an integer greater than 2")
    return math.log(p) ** 2 / (2 * float(product_c2(p)))


def main() -> None:
    actual = twin_count(100000)
    estimate = hardy_littlewood_estimate(100000)
    print(json.dumps({
        "schemaVersion": "twin-prime-count-check/v1",
        "sourceId": "9499499139",
        "countsByPowerOfTen": {str(10**e): twin_count(10**e) for e in range(2, 9)},
        "x100000HardyLittlewood": estimate,
        "actualPi2At100000": actual,
        "imageEstimate": 1620,
        "imageMinusActualRatio": (1620 - actual) / actual,
        "imageMinusActualPercent": 100 * (1620 - actual) / actual,
        "claimedPercent": 0.3235294118,
        "meanGapHeuristicAt1000000": mean_gap_heuristic(1000000),
        "clementExamples": {str(p): clement_condition(p) for p in [3, 5, 7, 11, 13]},
        "meanValueDerivativeOfIntegerCountIsValid": False,
        "provedGlobalInfinitude": False,
        "evidenceUpgrade": False,
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
