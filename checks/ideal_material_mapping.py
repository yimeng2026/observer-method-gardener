#!/usr/bin/env python3
"""Arithmetic checks for material mappings in post 10501114457."""
from __future__ import annotations
import json
import math


def electron_length_conventions() -> dict:
    h = 6.62607015e-34
    hbar = h / (2 * math.pi)
    c = 299792458.0
    electron_energy_j = 510998.95 * 1.602176634e-19
    ordinary = h * c / electron_energy_j
    reduced = hbar * c / electron_energy_j
    return {
        "hTimesCOverElectronEnergyM": ordinary,
        "hbarTimesCOverElectronEnergyM": reduced,
        "conventionRatio": ordinary / reduced,
    }


def lattice_table_errors_percent() -> dict:
    pairs = {"Al": (4.05, 4.03), "Cu": (3.61, 3.59), "Fe": (2.87, 2.85)}
    return {name: abs(predicted - measured) / measured * 100 for name, (measured, predicted) in pairs.items()}


def audit_mapping() -> dict:
    lengths = electron_length_conventions()
    errors = lattice_table_errors_percent()
    return {
        "schemaVersion": "ideal-material-mapping-arithmetic/v1",
        "sourceId": "10501114457",
        "sourceLocators": ["36.jpg", "57.jpg", "58.jpg"],
        "electronLengths": lengths,
        "displayedElectronLengthMatchesReducedConvention": math.isclose(
            lengths["hbarTimesCOverElectronEnergyM"], 3.86e-13, rel_tol=0.001
        ),
        "latticeTableErrorsPercent": errors,
        "scope": "Arithmetic and notation only; table agreement does not establish independent prediction or material validation.",
        "evidenceUpgrade": False,
    }


def main() -> None:
    print(json.dumps(audit_mapping(), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
