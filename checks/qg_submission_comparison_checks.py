#!/usr/bin/env python3
"""Recalculate only the numbers printed in the proposed QG submission table."""
from __future__ import annotations

import json
from decimal import Decimal


def comparison_table() -> list[dict[str, float | str]]:
    rows = [
        ("H0", "67.14", "67.4", 0.0039),
        ("omegaM", "0.3089", "0.308", 0.0029),
        ("omegaB", "0.0489", "0.0486", 0.0062),
        ("omegaLambda", "0.6911", "0.692", 0.0013),
        ("electronMass", "9.10938356e-31", "9.1093837015e-31", 1.5e-8),
        ("protonMass", "1.672621898e-27", "1.67262192369e-27", 1.5e-8),
        ("alphaInverse", "137.035999", "137.035999084", 6e-11),
    ]
    result = []
    for key, theory_text, observation_text, displayed in rows:
        theory = Decimal(theory_text)
        observation = Decimal(observation_text)
        result.append({
            "id": key,
            "theoryDisplay": float(theory),
            "observationDisplay": float(observation),
            "displayedRelativeError": displayed,
            "recomputedRelativeError": float(abs(theory - observation) / abs(observation)),
        })
    return result


def main() -> None:
    print(json.dumps({
        "schemaVersion": "qg-submission-comparison-checks/v1",
        "sourceIds": ["10352425546"],
        "comparisonTable": comparison_table(),
        "submissionReceiptShown": False,
        "tableEqualityAloneProvesFirstPrinciplesDerivation": False,
        "evidenceUpgrade": False,
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
