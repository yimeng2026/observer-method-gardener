#!/usr/bin/env python3
"""Standard Dirac hydrogen baseline and normalization countercheck."""
from __future__ import annotations
import json
import math
import mpmath as mp


def dirac_total_energy(n, k, alpha, rest_energy=1.0):
    """Standard Coulomb-Dirac total energy, including the rest energy."""
    if not isinstance(n, int) or not isinstance(k, int) or n < 1 or k == 0 or abs(k) > n:
        raise ValueError("Require n>=1, nonzero integer |k|<=n")
    if alpha <= 0 or rest_energy <= 0 or k*k <= alpha*alpha:
        raise ValueError("Require positive constants and real Coulomb-Dirac branch")
    with mp.workdps(60):
        a = mp.mpf(alpha)
        denominator = n - abs(k) + mp.sqrt(k*k - a*a)
        return float(rest_energy / mp.sqrt(1 + (a / denominator)**2))


def dirac_binding_expansion(n, j, alpha, rest_energy=1.0):
    if n < 1 or j <= 0 or alpha <= 0 or rest_energy <= 0:
        raise ValueError("Require positive n, j, alpha and rest energy")
    with mp.workdps(60):
        a = mp.mpf(alpha)
        result = -rest_energy * a*a / (2*n*n) - rest_energy * a**4 / (2*n**3) * (1 / (j + mp.mpf('0.5')) - 3 / (4*n))
        return float(result)


def perturbative_wavefunction_norm(kappa, r0_over_a0):
    """Norm of the displayed dimensionless correction for a0=1 and R0=r0_over_a0."""
    if kappa < 0 or r0_over_a0 <= 0:
        raise ValueError("Require kappa>=0 and positive R0/a0")
    with mp.workdps(50):
        k = mp.mpf(kappa)
        r0 = mp.mpf(r0_over_a0)
        factor = lambda r: 1 - k * (r - r0) / 2
        norm = mp.quad(lambda r: 4*r*r*mp.exp(-2*r)*factor(r)**2, [0, r0, 1, 5, mp.inf])
        return float(norm)


def main() -> None:
    alpha = 0.0072973525693
    exact = dirac_total_energy(2, -1, alpha)
    print(json.dumps({
        "schemaVersion": "dirac-energy-baseline/v1",
        "sourceId": "9564889398",
        "exactTotalEnergyOverRest": exact,
        "exactBindingOverRest": exact - 1,
        "displayedBindingExpansionOverRest": dirac_binding_expansion(2, 0.5, alpha),
        "illustrativeCorrectedWavefunctionNorm": perturbative_wavefunction_norm(0.01, 0.1),
        "newMediumOrProtonRadiusModelValidated": False,
        "curvedSpacetimeDiracEquationDerived": False,
        "evidenceUpgrade": False,
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
