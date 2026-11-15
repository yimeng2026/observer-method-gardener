#!/usr/bin/env python3
"""Arithmetic checks for two public DSF cosmology claims."""
from __future__ import annotations
import json
import math


def audit_dsf_claim() -> dict:
    relative_range = [1e-3, 1e-2]
    percent_range = [value * 100 for value in relative_range]
    exponential = math.exp(-1.4e-14)
    return {
        "schemaVersion": "dsf-claim-arithmetic/v1",
        "sourceId": "10987516879",
        "sourceLocators": ["25.jpg", "26.jpg", "27.jpg", "28.jpg"],
        "hubbleRelativeRange": relative_range,
        "hubbleRelativePercentRange": percent_range,
        "publishedApproximateTensionPercent": 10.0,
        "hubbleRangeMatchesTenPercentClaim": percent_range[0] <= 10.0 <= percent_range[1],
        "cmbExponent": -1.4e-14,
        "cmbExponentialFactor": exponential,
        "scope": "Arithmetic only; no DSF model, cosmological likelihood or physical amplification mechanism is validated.",
        "evidenceUpgrade": False,
    }


def main() -> None:
    print(json.dumps(audit_dsf_claim(), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
