#!/usr/bin/env python3
"""Reference arithmetic for the D-T example in post 10226818220."""
from __future__ import annotations
import json
import math

C = 299792458.0
U_KG = 1.66053906892e-27
EV_J = 1.602176634e-19


def dt_reference() -> dict:
    deuterium = 2.0141017778
    tritium = 3.01604928199
    helium4 = 4.00260325413
    neutron = 1.00866491588
    defect_u = deuterium + tritium - helium4 - neutron
    defect_kg = defect_u * U_KG
    energy_j = defect_kg * C**2
    return {
        "massDefectU": defect_u,
        "massDefectKg": defect_kg,
        "energyJ": energy_j,
        "energyMeV": energy_j / EV_J / 1e6,
    }


def evaluate_displayed_claim() -> dict:
    reference = dt_reference()
    displayed_mass = 8.35e-30
    displayed_energy = 7.51e-13
    return {
        "displayedMassOverReference": displayed_mass / reference["massDefectKg"],
        "displayedEnergyOverReference": displayed_energy / reference["energyJ"],
        "matchesReference": math.isclose(displayed_energy, reference["energyJ"], rel_tol=0.02),
        "displayedMassEnergyInternallyConsistent": math.isclose(displayed_mass * C**2, displayed_energy, rel_tol=0.002),
    }


def audit_claim() -> dict:
    return {
        "schemaVersion": "dt-fusion-claim-arithmetic/v1",
        "sourceId": "10226818220",
        "sourceLocators": ["06.jpg", "07.jpg", "08.jpg"],
        "reference": dt_reference(),
        "displayed": evaluate_displayed_claim(),
        "scope": "Atomic-mass and unit arithmetic only; no new microscopic mechanism is validated or ruled out by this check alone.",
        "evidenceUpgrade": False,
    }


def main() -> None:
    print(json.dumps(audit_claim(), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
