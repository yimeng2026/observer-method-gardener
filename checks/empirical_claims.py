#!/usr/bin/env python3
"""Recompute a public seven-row galaxy-rotation table; no validation of FEQ is implied."""
from __future__ import annotations
import json
import math


def summarize_percentage_errors(observed, predicted) -> dict:
    observed = [float(value) for value in observed]
    predicted = [float(value) for value in predicted]
    if not observed or len(observed) != len(predicted):
        raise ValueError("Nonempty, equally sized observations and predictions are required")
    if any(not math.isfinite(value) or value <= 0 for value in observed):
        raise ValueError("Observed values must be finite and positive")
    if any(not math.isfinite(value) for value in predicted):
        raise ValueError("Predicted values must be finite")
    signed = [(prediction - observation) / observation * 100 for observation, prediction in zip(observed, predicted)]
    return {
        "signedPercentErrors": signed,
        "rmsAbsolutePercent": math.sqrt(sum(value * value for value in signed) / len(signed)),
        "maxAbsolutePercent": max(abs(value) for value in signed),
    }


def main() -> None:
    observed = [210, 220, 230, 235, 232, 215, 190]
    predicted = [213, 219, 228, 236, 234, 218, 195]
    result = {
        "schemaVersion": "empirical-claim-check/v1",
        "sourceId": "10925099933",
        "sourceLocators": ["09.jpg", "10.jpg", "11.jpg"],
        "observedKmPerS": observed,
        "predictedKmPerS": predicted,
        **summarize_percentage_errors(observed, predicted),
        "publishedSummary": {"weightedRmsPercent": 2.7, "maxAbsolutePercent": 3.1},
        "scope": "Arithmetic audit of the displayed seven-row table only; weighted summary requires disclosed weights and formula.",
        "evidenceUpgrade": False,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
