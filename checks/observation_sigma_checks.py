#!/usr/bin/env python3
"""Recalculate the displayed theory-minus-observation standardized residuals."""
from __future__ import annotations

import json


def observation_rows() -> list[dict[str, float | str]]:
    rows = [
        ("starlight", 1.751, 1.750, 0.005, 0.2),
        ("mercury", 43.000, 42.96, 0.02, 1.9),
        ("solarRedshift", 2.11e-6, 2.12e-6, 0.01e-6, 1.0),
        ("milkyWayRotation", 232.0, 230.0, 10.0, 0.2),
        ("hubble", 67.4, 67.4, 0.5, 0.0),
        ("omegaM", 0.315, 0.315, 0.007, 0.0),
    ]
    return [
        {
            "id": key,
            "theory": theory,
            "observation": observation,
            "uncertainty": uncertainty,
            "displayedSigma": displayed,
            "recomputedSigma": abs(theory - observation) / uncertainty,
        }
        for key, theory, observation, uncertainty, displayed in rows
    ]


def unverifiable_sigma_rows() -> list[int]:
    """Rows 10 and 12 show numeric sigmas but no corresponding theory values in the eight images."""
    return [10, 12]


def main() -> None:
    print(json.dumps({
        "schemaVersion": "observation-sigma-checks/v1",
        "sourceIds": ["10343813067"],
        "rows": observation_rows(),
        "unverifiableSigmaRows": unverifiable_sigma_rows(),
        "desiAttributionRequiresModelAndDataset": True,
        "evidenceUpgrade": False,
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
