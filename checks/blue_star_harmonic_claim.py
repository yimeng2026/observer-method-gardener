#!/usr/bin/env python3
"""High-precision checks for the repackaged harmonic approximation.

The polynomial integrals are checked as ordinary calculus only.  Their
numerical agreement with zeta(-1) is not treated as a derivation of zeta's
analytic continuation, and no finite value is assigned to zeta(1).
"""
from __future__ import annotations

from fractions import Fraction
import json

import mpmath as mp


def expansion_coefficients() -> dict[str, mp.mpf]:
    """Separate approximant coefficients from residuals against H_n."""
    gamma = mp.euler
    beta = 10 * ((1 - gamma) / 2 - Fraction(1, 12))
    displayed_inverse_n_squared = -mp.mpf(1) / 2 + gamma / 2 + beta / 10
    base_residual_inverse_n_squared = (
        -mp.mpf(1) / 2 + gamma / 2 + mp.mpf(1) / 12
    )
    return {
        "beta": beta,
        "inverseN": mp.mpf(1) - mp.mpf(1) / 2,
        "inverseNSquaredDisplayed": displayed_inverse_n_squared,
        "inverseNSquaredBeforeCorrection": base_residual_inverse_n_squared,
        "inverseNSquaredAfterCorrection": base_residual_inverse_n_squared + beta / 10,
        "inverseNSquaredCorrectedResidual": base_residual_inverse_n_squared + beta / 10,
        "correctedLeadingCoefficient": mp.mpf(1) / 3 - gamma**2 / 2,
        "nextCoefficient": gamma**3 / 2 - mp.mpf(31) / 120,
    }


def harmonic_residuals(n: int) -> dict[str, mp.mpf]:
    """Return approximation minus H_n without losing tiny residuals to cancellation."""
    if isinstance(n, bool) or not isinstance(n, int) or n < 1:
        raise ValueError("n must be a positive integer")
    # The corrected residual is O(n^-3), while H_n is O(log n).  Retain
    # enough guard digits for that subtraction instead of displaying a false zero.
    required_dps = 3 * len(str(n)) + 100
    with mp.workdps(required_dps):
        value = mp.mpf(n)
        exact = mp.harmonic(value)
        base = mp.log(value + 1) + mp.euler - 1 / (2 * (value + mp.euler))
        correction = expansion_coefficients()["beta"] / (10 * value**2)
        return {
            "baseResidual": base - exact,
            "correctedResidual": base + correction - exact,
        }


def arithmetic_partial_sum_integrals() -> dict[str, str]:
    """Evaluate the two polynomial integrals without invoking continuation."""
    from_minus_one_to_zero = -Fraction(1, 2) * (-Fraction(1, 3) + Fraction(1, 2))
    from_zero_to_one_shifted = Fraction(1, 2) * (Fraction(1, 3) - Fraction(1, 2))
    assert from_minus_one_to_zero == Fraction(-1, 12)
    assert from_zero_to_one_shifted == Fraction(-1, 12)
    return {
        "fromMinusOneToZero": str(from_minus_one_to_zero),
        "fromZeroToOneShifted": str(from_zero_to_one_shifted),
        "operation": "ordinary polynomial integration, not analytic continuation",
    }


def main() -> None:
    with mp.workdps(90):
        coefficients = expansion_coefficients()
        samples = []
        for exponent in (300, 800):
            residuals = harmonic_residuals(10**exponent)
            samples.append({
                "n": f"10^{exponent}",
                "baseResidual": mp.nstr(residuals["baseResidual"], 50),
                "correctedResidual": mp.nstr(residuals["correctedResidual"], 50),
            })
        print(json.dumps({
            "schemaVersion": "blue-star-harmonic-arithmetic/v1",
            "sourceIds": ["9438399015"],
            "sameApproximantAs": ["9581109556", "9581079063"],
            "beta": mp.nstr(coefficients["beta"], 80),
            "inverseNSquaredBeforeCorrection": mp.nstr(coefficients["inverseNSquaredBeforeCorrection"], 50),
            "inverseNSquaredAfterCorrection": mp.nstr(coefficients["inverseNSquaredAfterCorrection"], 10),
            "correctedLeadingCoefficient": mp.nstr(coefficients["correctedLeadingCoefficient"], 50),
            "nextCoefficient": mp.nstr(coefficients["nextCoefficient"], 50),
            "samples": samples,
            "polynomialIntegrals": arithmetic_partial_sum_integrals(),
            "zeta1HasFiniteValue": False,
            "evidenceUpgrade": False,
        }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
