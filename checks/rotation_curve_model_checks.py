#!/usr/bin/env python3
"""Independent checks for the rotation-curve and empirical-claim post."""
from __future__ import annotations

import json
import math


def scale_and_dark_matter() -> dict[str, float]:
    alpha_g = 1.75e-45
    return {
        "scaleDecades": math.log10(1e26 / 1e-35),
        "darkMatterRatio": 2 * math.pi * alpha_g**(-1 / 3) / math.exp(0.57721566),
    }


def rotation_curve_limits() -> dict[str, float]:
    beta = 0.25

    def shape(x: float) -> float:
        return math.log1p(x) / x - 1 / (1 + x) + beta / x**2

    def shape_derivative(x: float) -> float:
        return (
            1 / (x * (1 + x))
            - math.log1p(x) / x**2
            + 1 / (1 + x)**2
            - 2 * beta / x**3
        )

    small_x = 1e-6
    outer_x = 1e6
    return {
        "smallXProduct": small_x * math.sqrt(shape(small_x)),
        "zeroTermCentralVelocityExponent": 0.5,
        "requiredFiniteCoreVelocityExponent": 1.0,
        "actualOuterSlope": outer_x * shape_derivative(outer_x) / (2 * shape(outer_x)),
        "displayedOuterSlope": -1 / (2 * outer_x) - beta / outer_x**2,
    }


def dark_matter_fraction() -> dict[str, float]:
    def fraction(y: float) -> float:
        return 1 - y * (1 - 0.5 * math.log(y))

    return {
        "atZero": 1.0,
        "atOne": fraction(1.0),
        "atOnePointTwo": fraction(1.2),
    }


def galaxy_fit_statistics() -> dict[str, float]:
    milky_way_obs = [90, 135, 170, 230, 225, 215, 200]
    milky_way_theory = [94, 141, 175, 232, 226, 214, 198]
    milky_way_error = [5, 5, 5, 10, 10, 15, 20]
    m31_obs = [100, 150, 200, 250, 260, 240, 225]
    m31_theory = [105, 155, 205, 247, 257, 238, 222]
    m31_error = [10, 8, 10, 15, 15, 20, 25]

    def chi2_per_point(obs, theory, error) -> float:
        return sum(((o - t) / e)**2 for o, t, e in zip(obs, theory, error)) / len(obs)

    return {
        "milkyWayChi2PerPoint": chi2_per_point(milky_way_obs, milky_way_theory, milky_way_error),
        "m31Chi2PerPoint": chi2_per_point(m31_obs, m31_theory, m31_error),
        "milkyWayOuterSlope": (milky_way_obs[-1] - milky_way_obs[-3]) / (50 - 15),
        "m31OuterSlope": (m31_obs[-1] - m31_obs[-3]) / (50 - 15),
    }


def observation_arithmetic() -> dict[str, float]:
    return {
        "w0Sigma": abs(-1.028 - (-1.03)) / 0.03,
        "heliumSigma": abs(0.2451 - 0.2449) / 0.0040,
        "milkyWaySigma": abs(211 - 230) / 10,
    }


def main() -> None:
    print(json.dumps({
        "schemaVersion": "rotation-curve-model-checks/v1",
        "sourceIds": ["10330962974"],
        "scaleAndDarkMatter": scale_and_dark_matter(),
        "rotationCurveLimits": rotation_curve_limits(),
        "darkMatterFraction": dark_matter_fraction(),
        "galaxyFitStatistics": galaxy_fit_statistics(),
        "observationArithmetic": observation_arithmetic(),
        "publicationVerification": "unverified",
        "evidenceUpgrade": False,
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
