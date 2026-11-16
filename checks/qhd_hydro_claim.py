#!/usr/bin/env python3
"""Retain both favorable and unfavorable public hydro-forecast examples."""
from __future__ import annotations
import json


def audit_qhd_hydro_claim() -> dict:
    rows = [
        {"station": "监利", "previousM": 4.08, "predictedM": 4.09, "actualM": 4.10},
        {"station": "重庆", "previousM": 14.99, "predictedM": 14.92, "actualM": 15.01},
    ]
    for row in rows:
        row["absoluteErrorM"] = abs(row["actualM"] - row["predictedM"])
        row["predictedDeltaM"] = row["predictedM"] - row["previousM"]
        row["actualDeltaM"] = row["actualM"] - row["previousM"]
        row["directionMismatch"] = row["predictedDeltaM"] * row["actualDeltaM"] < 0
    return {
        "schemaVersion": "qhd-hydro-public-examples/v1",
        "sourceId": "11153774899",
        "sourceLocators": ["34.jpg", "35.jpg", "39.jpg", "41.jpg", "42.jpg"],
        "examples": rows,
        "meanAbsoluteErrorM": sum(row["absoluteErrorM"] for row in rows) / len(rows),
        "maxAbsoluteErrorM": max(row["absoluteErrorM"] for row in rows),
        "directionMismatchExamples": [row for row in rows if row["directionMismatch"]],
        "scope": "Two selected public examples only; not a complete forecast score or hydrological validation.",
        "evidenceUpgrade": False,
    }


def main() -> None:
    print(json.dumps(audit_qhd_hydro_claim(), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
