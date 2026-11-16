#!/usr/bin/env python3
"""Version and unit checks for the four-parameter 'new official science' post."""
from __future__ import annotations
import json


def parameter_variants() -> dict:
    hbar = 1.054571817e-34
    c = 299792458.0
    lambda_c = 5.99153e-13
    ev_j = 1.602176634e-19
    later_mass_kg = 0.0147 * hbar / (lambda_c * c)
    later_mass_mev = later_mass_kg * c**2 / ev_j / 1e6
    early_mass_kg = 0.00148 * hbar / (lambda_c * c)
    import math
    return {
        "laterMassKg": later_mass_kg,
        "laterMassMeV": later_mass_mev,
        "displayedMassRatio": later_mass_mev / 0.00485,
        "earlyMassKg": early_mass_kg,
        "z0Ratio": 0.0147 / 0.00148,
        "gravitonFormulaMeV": (later_mass_mev / 0.0147) * math.sqrt(8.29e-5 / 1.55769540),
        "gravitonDisplayedKgEV": 1.236e-38 * c**2 / ev_j,
        "darkMatterDisplayedKgEV": 1.378e-36 * c**2 / ev_j,
        "parametersEndogenous": False,
        "reason": "Base mass and dark-matter values are compatible; conflicting Z0 versions and incompatible graviton values require a version and unit ledger.",
    }


def main() -> None:
    print(json.dumps({"schemaVersion": "new-official-parameters/v1", "sourceId": "10198884236", **parameter_variants(), "evidenceUpgrade": False}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
