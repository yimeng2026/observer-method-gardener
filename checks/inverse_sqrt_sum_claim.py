#!/usr/bin/env python3
"""Certified convexity bounds for sum_{k=1}^N 1/sqrt(k)."""
from __future__ import annotations
from decimal import Decimal, localcontext
import json


def inverse_sqrt_sum_certificate(n: int) -> dict:
    """Return decimal-string bounds proved by trapezoid and midpoint integrals.

    For convex f(x)=1/sqrt(x), the trapezoid rule overestimates each integral
    and the midpoint rule underestimates it. Consequently,
      L = 2 sqrt(N+1) - 3/2 - 1/(2 sqrt(N+1)) <= S_N,
      U = 1 + 2 sqrt(N+1/2) - 2 sqrt(3/2) >= S_N.
    A 1e-40 outward margin covers Decimal rounding at 60-digit precision.
    """
    if isinstance(n, bool) or not isinstance(n, int) or n < 1:
        raise ValueError("N must be a positive integer")
    with localcontext() as context:
        context.prec = 60
        value = Decimal(n)
        next_root = (value + 1).sqrt()
        lower = 2 * next_root - Decimal("1.5") - 1 / (2 * next_root)
        upper = 1 + 2 * (value + Decimal("0.5")).sqrt() - 2 * Decimal("1.5").sqrt()
        margin = Decimal("1e-40")
        return {
            "lower": format(lower - margin, "f"),
            "upper": format(upper + margin, "f"),
            "boundType": "convex_trapezoid_and_midpoint",
            "numericalMargin": "1e-40",
        }


def displayed_s100_bounds() -> dict:
    """Evaluate the purported sharp bounds in the two new content images."""
    import math
    lower = 2 * math.sqrt(101) - 1.5 + 1 / (2 * math.sqrt(101)) + 1 / 24 - 1 / (24 * 101**1.5)
    upper = 2 * math.sqrt(100) - 1.5 + 1 / (2 * math.sqrt(100)) + 1 / 24 - 1 / (24 * 100**1.5)
    actual = sum(1 / math.sqrt(k) for k in range(1, 101))
    return {"lower": lower, "upper": upper, "actual": actual, "lowerIsInvalid": lower > actual}


def main() -> None:
    result = inverse_sqrt_sum_certificate(400002025)
    lower = Decimal(result["lower"])
    upper = Decimal(result["upper"])
    print(json.dumps({
        "schemaVersion": "inverse-sqrt-sum-check/v1",
        "sourceId": "9451317463",
        "n": 400002025,
        **result,
        "integerPart": int(lower) if int(lower) == int(upper) else None,
        "displayedS100Bounds": displayed_s100_bounds(),
        "historicalOriginVerified": False,
        "evidenceUpgrade": False,
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
