#!/usr/bin/env python3
"""Independent checks for the DeepSeek research-example number theory claims."""
from __future__ import annotations
import json
import math
import mpmath as mp

try:
    from checks.prime_quadruplet_claim import primes_up_to
except ModuleNotFoundError:  # Direct execution from the checks directory.
    from prime_quadruplet_claim import primes_up_to


def derivative_comparison(x):
    logx = math.log(x)
    return {
        "exactDerivative": (logx - 1) / logx**2,
        "claimedDerivative": 1 / (1 + logx),
    }


def integral_derivatives(x):
    t = 1 + math.log(x)
    unscaled = mp.exp(t) / (t * x)
    return {
        "unscaledEiDerivative": float(unscaled),
        "displayedScaledDerivative": float(unscaled / math.e),
        "targetDerivative": 1 / t,
    }


def symmetry_counterexample(a):
    polynomial = lambda s: (s - a) * (s - (1 - a))
    return {
        "roots": [a, 1 - a],
        "valueAt0.1": polynomial(0.1),
        "valueAt0.9": polynomial(0.9),
    }


def prime_gap_scan(limit):
    primes = primes_up_to(limit)
    rows = []
    for index in range(len(primes) - 1):
        prime = primes[index]
        if prime < 3:
            continue
        gap = primes[index + 1] - prime
        rows.append((prime, gap, gap / math.log(prime)))
    maximum = max(rows, key=lambda row: row[2])
    return {
        "pairs": len(rows),
        "maxRatioPrime": maximum[0],
        "maxRatioGap": maximum[1],
        "maxGapOverLog": maximum[2],
        "allGapsAtLeast2": all(gap >= 2 for _, gap, _ in rows),
        "allGapsBelow36Log": all(gap <= 36 * math.log(prime) for prime, gap, _ in rows),
        "allGapsBelowOnePlus36Log": all(gap <= 1 + 36 * math.log(prime) for prime, gap, _ in rows),
    }


def main() -> None:
    print(json.dumps({
        "schemaVersion": "research-example-number-theory/v1",
        "sourceId": "9462214167",
        "derivativeAtESquared": derivative_comparison(math.e**2),
        "integralAtESquared": integral_derivatives(math.e**2),
        "symmetryCounterexample": symmetry_counterexample(0.2),
        "primeGapScanTo1000000": prime_gap_scan(1000000),
        "finiteScanProvesGlobalUpperBound": False,
        "riemannHypothesisProvenByDisplayedSymmetry": False,
        "evidenceUpgrade": False,
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
