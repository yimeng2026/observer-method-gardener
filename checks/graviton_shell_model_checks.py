#!/usr/bin/env python3
"""Independent SI checks for the 2025-12-23 graviton-shell post."""
from __future__ import annotations

import json
import math

C = 299792458.0
G = 6.67430e-11
H = 6.62607015e-34
HBAR = 1.054571817e-34
K_B = 1.380649e-23
EV_J = 1.602176634e-19
DISPLAYED_E1_J = 2.1e-46


def energy_and_thermal_scale() -> dict[str, float]:
    lambda_c = 1e-19
    alpha_g = 5.9e-39
    lambda_mass = HBAR / (lambda_c * C)
    return {
        "lambdaMassKg": lambda_mass,
        "bindingEnergyJ": lambda_mass * C**2 * alpha_g**2 / 2,
        "displayedTemperatureK": DISPLAYED_E1_J / K_B,
        "displayedLengthM": HBAR * C / DISPLAYED_E1_J,
    }


def energy_density_ratio() -> dict[str, float]:
    # This checks only the ratio printed in images 35-36, not its derivation.
    coefficient = 15 * 1e-19 * K_B / (4 * math.pi * HBAR * C)
    return {
        "coefficientPerK": coefficient,
        "at27K": coefficient * 2.7,
        "at1e15K": coefficient * 1e15,
    }


def geometry_and_cutoffs() -> dict[str, float]:
    return {
        "bohrRadiusM": 1e-19 / 1.75e-45,
        "planckCutoff": 1e-19 / 1.6e-35,
        "alpha45Cutoff": 1 / 1.75e-45,
        "alpha39Cutoff": 1 / 5.9e-39,
    }


def decay_channel_differences() -> dict[str, float]:
    levels_ev = {
        "1S0": -1.32e-27,
        "2S0": -3.30e-28,
        "2P1": -3.29e-28,
        "2P2": -3.28e-28,
        "2P3": -3.27e-28,
        "3S0": -1.47e-28,
        "3P1": -1.46e-28,
        "3D1": -1.45e-28,
    }
    channels = [
        ("2S0", "1S0"),
        ("2P1", "1S0"),
        ("2P2", "1S0"),
        ("2P3", "1S0"),
        ("3S0", "2P1"),
        ("3P1", "2S0"),
        ("3D1", "2P1"),
    ]
    return {
        f"{upper}->{lower}": levels_ev[upper] - levels_ev[lower]
        for upper, lower in channels
    }


def frequency_conversions() -> dict[str, float]:
    return {
        "normalized2To1Hz": DISPLAYED_E1_J * 0.7501 / H,
        "displayedE0TransitionHz": 1e-27 * EV_J * 0.75 / H,
        "milliEv23Hz": 2.3e-3 * EV_J / H,
        "halfMillimetreHz": C / 0.0005,
    }


def spectral_sequence() -> dict[str, float]:
    f0 = 2.41e-8

    def frequency(upper: int, lower: int) -> float:
        return f0 * abs(upper**-2 - lower**-2)

    high_shell_frequency = frequency(9, 8)
    return {
        "2->1Hz": frequency(2, 1),
        "3->2Hz": frequency(3, 2),
        "4->3Hz": frequency(4, 3),
        "5->4Hz": frequency(5, 4),
        "9->8Hz": high_shell_frequency,
        "9->8WavelengthM": C / high_shell_frequency,
    }


def microphysical_frequency_version() -> dict[str, float]:
    mass = 1.1e-68
    alpha = G * mass**2 / (HBAR * C)
    return {
        "alphaFromMass": alpha,
        "comptonWavelengthM": HBAR / (mass * C),
        "baseFrequencyHz": alpha**2 * mass * C**2 / (2 * H),
    }


def action_dimensions(c_power: int, spacetime_dimension: int = 5) -> dict[str, int]:
    """Dimensions of c**p/G_D * R * d**D x, with all coordinates in metres."""
    if spacetime_dimension < 2:
        raise ValueError("spacetime_dimension must be at least two")
    dimensions = {"M": 0, "L": 0, "T": 0}

    def add(mass: int, length: int, time: int) -> None:
        dimensions["M"] += mass
        dimensions["L"] += length
        dimensions["T"] += time

    add(0, c_power, -c_power)  # c**p
    add(1, -(spacetime_dimension - 1), 2)  # 1/G_D
    add(0, -2, 0)  # scalar curvature
    add(0, spacetime_dimension, 0)  # integration measure
    return dimensions


def finite_shell_count_and_cutoff() -> dict[str, float | int | bool]:
    radial_root = math.sqrt(1e26 / 1.2e26)
    strict_floor = math.floor(radial_root)
    return {
        "displayedStateTotal": sum([5, 5, 15, 5, 15, 5, 15, 5, 15]),
        "radialRoot": radial_root,
        "strictFloor": strict_floor,
        "nearestInteger": round(radial_root),
        "supportsNineShells": strict_floor == 9,
    }


def mercury_baseline() -> dict[str, float | int | bool]:
    solar_mass = 1.9885e30
    semi_major_axis = 5.7909e10
    eccentricity = 0.2056
    compactness = G * solar_mass / (C**2 * semi_major_axis)
    radians = 6 * math.pi * compactness / (1 - eccentricity**2)
    orbits_per_century = 365.256 / 87.969 * 100
    alpha_squared_over_r_squared_length_exponent = 2 * 0 - 2
    return {
        "compactness": compactness,
        "radiansPerOrbit": radians,
        "arcsecondsPerCentury": math.degrees(radians) * 3600 * orbits_per_century,
        "alphaSquaredOverRSquaredLengthExponent": alpha_squared_over_r_squared_length_exponent,
        "metricCorrectionIsDimensionless": alpha_squared_over_r_squared_length_exponent == 0,
    }


def main() -> None:
    print(json.dumps({
        "schemaVersion": "graviton-shell-model-checks/v1",
        "sourceIds": ["10327019478"],
        "energyAndThermalScale": energy_and_thermal_scale(),
        "energyDensityRatio": energy_density_ratio(),
        "geometryAndCutoffs": geometry_and_cutoffs(),
        "decayChannelDifferences": decay_channel_differences(),
        "frequencyConversions": frequency_conversions(),
        "spectralSequence": spectral_sequence(),
        "microphysicalFrequencyVersion": microphysical_frequency_version(),
        "c4ActionDimensions": action_dimensions(4),
        "c3ActionDimensions": action_dimensions(3),
        "finiteShellCountAndCutoff": finite_shell_count_and_cutoff(),
        "mercuryBaseline": mercury_baseline(),
        "evidenceUpgrade": False,
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
