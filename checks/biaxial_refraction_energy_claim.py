#!/usr/bin/env python3
"""Evaluate the displayed two-channel s-polarized energy coefficients."""
from __future__ import annotations
import json


def displayed_energy_coefficients(A, B, C):
    """Use A=n_i cos(theta_i), B=n_1s cos(theta_t1), C=n_2s cos(theta_t2).

    This evaluates the formulas as displayed; it does not assume they satisfy
    Maxwell boundary conditions or energy conservation.
    """
    D = A + B + C
    E = B - C
    R = ((A - B - C) / D)**2
    t1 = 2 * A * B / (D * E)
    t2 = -2 * A * C / (D * E)
    T1 = B / A * abs(t1)**2
    T2 = C / A * abs(t2)**2
    return {
        "R": R,
        "t1": t1,
        "t2": t2,
        "T1": T1,
        "T2": T2,
        "energySum": R + T1 + T2,
    }


def main() -> None:
    two_channel = displayed_energy_coefficients(1.0, 2.0, 1.0)
    single_channel = displayed_energy_coefficients(1.0, 2.0, 0.0)
    print(json.dumps({
        "schemaVersion": "biaxial-refraction-energy-check/v1",
        "sourceId": "9491341592",
        "twoChannelExample": {"A": 1.0, "B": 2.0, "C": 1.0, **two_channel},
        "singleChannelLimit": {"A": 1.0, "B": 2.0, "C": 0.0, **single_channel},
        "displayedTwoChannelFormulasConserveEnergyInGeneral": False,
        "maxwellBoundaryConditionsEstablished": False,
        "independentOpticalTheoryEstablished": False,
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
