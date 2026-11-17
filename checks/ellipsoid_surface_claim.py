#!/usr/bin/env python3
"""Cross-check the displayed triaxial-ellipsoid surface-area representation."""
from __future__ import annotations

import json

import mpmath as mp


def _axes(a, b, c, *, allow_sphere: bool):
    a, b, c = mp.mpf(a), mp.mpf(b), mp.mpf(c)
    if not (a >= b >= c > 0) or (not allow_sphere and not a > c):
        raise ValueError("Require a>=b>=c>0; elliptic formulas also require a>c")
    return a, b, c


def article_surface_area(a, b, c) -> mp.mpf:
    """Evaluate the article's atanh representation after t=sin(theta)."""
    with mp.workdps(60):
        a, b, c = _axes(a, b, c, allow_sphere=False)

        def coefficient(theta):
            sin_squared = mp.sin(theta) ** 2
            return 1 - c**2 * sin_squared / a**2 + c**2 * sin_squared / b**2 - c**2 / b**2

        def integrand(theta):
            value = coefficient(theta)
            root = mp.sqrt(value)
            return (1 - value) * mp.atanh(root) / root

        angular_integral = mp.quad(integrand, [-mp.pi / 2, 0, mp.pi / 2])
        return 2 * mp.pi * a * b + 2 * a * b * angular_integral


def standard_surface_area(a, b, c) -> mp.mpf:
    """Use the standard incomplete-elliptic-integral representation independently."""
    with mp.workdps(60):
        a, b, c = _axes(a, b, c, allow_sphere=False)
        major = mp.sqrt(a**2 - c**2)
        middle = mp.sqrt(b**2 - c**2)
        phi = mp.asin(major / a)
        parameter = (a * middle / (b * major)) ** 2
        return 2 * mp.pi * (
            c**2
            + b * c**2 / major * mp.ellipf(phi, parameter)
            + b * major * mp.ellipe(phi, parameter)
        )


def direct_surface_area(a, b, c) -> mp.mpf:
    """Integrate |r_u x r_v| over one octant, including the sphere limit."""
    with mp.workdps(50):
        a, b, c = _axes(a, b, c, allow_sphere=True)

        def integrand(u, v):
            sin_u, cos_u = mp.sin(u), mp.cos(u)
            return sin_u * mp.sqrt(
                b**2 * c**2 * sin_u**2 * mp.cos(v) ** 2
                + a**2 * c**2 * sin_u**2 * mp.sin(v) ** 2
                + a**2 * b**2 * cos_u**2
            )

        octant = mp.quad(integrand, [0, mp.pi / 2], [0, mp.pi / 2])
        return 8 * octant


def main() -> None:
    article = article_surface_area(5, 3, 2)
    standard = standard_surface_area(5, 3, 2)
    direct = direct_surface_area(5, 3, 2)
    print(json.dumps({
        "schemaVersion": "ellipsoid-surface-arithmetic/v1",
        "sourceIds": ["9433532719"],
        "axes": [5, 3, 2],
        "articleAtanhArea": mp.nstr(article, 55),
        "standardEllipticArea": mp.nstr(standard, 55),
        "directParametricArea": mp.nstr(direct, 32),
        "displayedArea": "134.775176724903634464601842410659640467",
        "verifiedPrefix": "134.775176724903634464601",
        "worldRankingEstablished": False,
        "evidenceUpgrade": False,
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
