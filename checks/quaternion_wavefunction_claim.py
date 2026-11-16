#!/usr/bin/env python3
"""Hamilton-product and series checks for the displayed quaternion exponential."""
from __future__ import annotations
import json
import math


def qmul(a, b):
    """Hamilton product in (1,i,j,k) coordinates."""
    a0, a1, a2, a3 = a
    b0, b1, b2, b3 = b
    return (
        a0*b0 - a1*b1 - a2*b2 - a3*b3,
        a0*b1 + a1*b0 + a2*b3 - a3*b2,
        a0*b2 - a1*b3 + a2*b0 + a3*b1,
        a0*b3 + a1*b2 - a2*b1 + a3*b0,
    )


def qexp_closed(alpha, beta, gamma):
    """exp(alpha+i*beta+j*gamma), evaluated from (i beta+j gamma)^2=-r^2."""
    radius = math.hypot(beta, gamma)
    scale = math.exp(alpha)
    if radius == 0:
        return scale, 0.0, 0.0, 0.0
    sine = math.sin(radius) / radius
    return scale * math.cos(radius), scale * beta * sine, scale * gamma * sine, 0.0


def qexp_series(alpha, beta, gamma, terms=40):
    """Independent truncated power series; no product-factorization assumption."""
    q = alpha, beta, gamma, 0.0
    term = 1.0, 0.0, 0.0, 0.0
    result = term
    for n in range(1, terms + 1):
        product = qmul(term, q)
        term = tuple(value / n for value in product)
        result = tuple(a + b for a, b in zip(result, term))
    return result


def displayed_product(beta, gamma):
    """The actual product (cos(beta)+i sin(beta))(cos(gamma)+j sin(gamma))."""
    return qmul((math.cos(beta), math.sin(beta), 0.0, 0.0), (math.cos(gamma), 0.0, math.sin(gamma), 0.0))


def main() -> None:
    beta = gamma = math.pi / 4
    direct = qexp_closed(0.0, beta, gamma)
    series = qexp_series(0.0, beta, gamma)
    product = displayed_product(beta, gamma)
    print(json.dumps({
        "schemaVersion": "quaternion-exponential-check/v1",
        "sourceId": "9388728245",
        "betaGamma": [beta, gamma],
        "directExponential": direct,
        "independentSeries": series,
        "seriesMaxComponentResidual": max(abs(a - b) for a, b in zip(direct, series)),
        "displayedProduct": product,
        "correctJComponent": math.cos(beta) * math.sin(gamma),
        "postJComponent": math.sin(beta) * math.sin(gamma),
        "noncommutativeFactorizationValidInGeneral": False,
        "wavefunctionEstablished": False,
        "schrodingerSignErrorEstablished": False,
        "specialRelativityRefuted": False,
        "evidenceUpgrade": False,
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
