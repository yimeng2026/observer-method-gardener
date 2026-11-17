#!/usr/bin/env python3
"""Round-trip times in the simplest classical stationary-ether model."""
from __future__ import annotations
import json
import math


def ether_arm_round_trips(length, speed_ratio, c=1.0):
    """Equal rest-length arms; speed_ratio=v/c and 0<=speed_ratio<1."""
    if length <= 0 or c <= 0 or not 0 <= speed_ratio < 1:
        raise ValueError("Require length>0, c>0 and 0<=v/c<1")
    beta2 = speed_ratio**2
    baseline = 2 * length / c
    longitudinal = baseline / (1 - beta2)
    transverse = baseline / math.sqrt(1 - beta2)
    return {
        "longitudinal": longitudinal,
        "transverse": transverse,
        "timeDifference": longitudinal - transverse,
        "leadingDifference": length / c * beta2,
    }


def main() -> None:
    print(json.dumps({
        "schemaVersion": "classical-ether-arm-times/v1",
        "sourceId": "9487081127",
        "length": 1.0,
        "speedRatio": 0.5,
        "c": 1.0,
        **ether_arm_round_trips(1.0, 0.5, 1.0),
        "simplestEtherModelPredictsZeroDifference": False,
        "michelsonMorleyAloneProvesAllOfSpecialRelativity": False,
        "alternativeEtherModelsRequireSeparateTests": True,
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
