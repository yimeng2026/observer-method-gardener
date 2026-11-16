#!/usr/bin/env python3
"""Arithmetic checks for the displayed temperature-to-magnetic-field formula."""
from __future__ import annotations
import json
import math


def delta_b_micro_tesla(b0, delta_t, *, k_b=1.380649e-23, m0=1.67262192369e-27, alpha=0.0072973525693, c=299792458.0):
    """Evaluate B0*sqrt(3*kB*DeltaT/(M0*c^2)/(2*alpha)), in microtesla."""
    if b0 <= 0 or delta_t <= 0:
        raise ValueError("B0 and temperature change must be positive")
    if k_b <= 0 or m0 <= 0 or alpha <= 0 or c <= 0:
        raise ValueError("Physical constants must be positive")
    return b0 * math.sqrt(3 * k_b * delta_t / (m0 * c**2) / (2 * alpha)) * 1e6


def main() -> None:
    claimed = {(1, 0.5): 25.4, (1, 2): 35.9, (3, 0.5): 76.2, (3, 2): 107.7, (5, 0.5): 127, (5, 2): 179.5}
    rows = []
    for (b0, dt), displayed in claimed.items():
        computed = delta_b_micro_tesla(b0, dt)
        rows.append({"B0T": b0, "deltaTK": dt, "computedMicroT": computed, "displayedMicroT": displayed, "displayedOverComputed": displayed / computed})
    print(json.dumps({
        "schemaVersion": "magnetic-temperature-check/v1",
        "sourceId": "9532344263",
        "rows": rows,
        "temperatureRatioComputed": delta_b_micro_tesla(1, 2) / delta_b_micro_tesla(1, 0.5),
        "temperatureRatioDisplayed": 35.9 / 25.4,
        "clinicalValidationPresent": False,
        "diagnosticUseEstablished": False,
        "evidenceUpgrade": False,
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
