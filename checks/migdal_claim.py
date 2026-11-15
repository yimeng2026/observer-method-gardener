#!/usr/bin/env python3
"""Arithmetic checks for public Migdal-related claims, not a physical replication."""
from __future__ import annotations
import json
import math


def audit_migdal_claim(ratio: float = 2.6e3, xi: float = 2.16e-4, theta_m_radians: float = math.radians(89.25)) -> dict:
    ratio = float(ratio)
    xi = float(xi)
    theta_m_radians = float(theta_m_radians)
    if not math.isfinite(ratio) or ratio <= 0:
        raise ValueError("ratio must be finite and positive")
    if not math.isfinite(xi) or xi < 0:
        raise ValueError("xi must be finite and nonnegative")
    if not math.isfinite(theta_m_radians):
        raise ValueError("theta_m_radians must be finite")
    exponent = 2 * theta_m_radians / math.pi
    factor = 1 + xi * ratio**exponent
    return {
        "schemaVersion": "migdal-claim-arithmetic/v1",
        "sourceId": "10406582785",
        "sourceLocators": ["04.jpg", "05.jpg", "06.jpg"],
        "observedEnergyEV": 37.2,
        "claimedTheoryEnergyEV": 37.19,
        "relativeEnergyDifferencePercent": abs(37.2 - 37.19) / 37.2 * 100,
        "wavelengthRatio": ratio,
        "xi": xi,
        "thetaMRadians": theta_m_radians,
        "enhancementExponent": exponent,
        "enhancementFactor": factor,
        "publishedEnhancementRange": [1e2, 1e3],
        "enhancementMatchesPublishedHundredToThousandRange": 1e2 <= factor <= 1e3,
        "scope": "Arithmetic only. No six-event dataset, likelihood, detector response, or five-dimensional model is validated.",
        "evidenceUpgrade": False,
    }


def main() -> None:
    print(json.dumps(audit_migdal_claim(), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
