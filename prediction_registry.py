#!/usr/bin/env python3
"""Validate a source-bounded registry of public quantitative predictions."""
from __future__ import annotations
from collections import Counter
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parent
STATUSES = {"unchecked", "pending_observation", "historical_mismatch", "supported", "contradicted_current_data", "identity_mismatch_warning"}


def validate_registry(registry: dict) -> None:
    if registry.get("schemaVersion") != "prediction-registry/v1":
        raise ValueError("Unsupported schemaVersion")
    if registry.get("evidenceUpgrade") is not False:
        raise ValueError("evidenceUpgrade must remain false")
    predictions = registry.get("predictions")
    if not isinstance(predictions, list) or not predictions:
        raise ValueError("predictions must be nonempty")
    identifiers = set()
    for item in predictions:
        for field in ("predictionId", "sourceId", "target", "claim", "proposedExperiment", "status", "revisionRequired", "evidenceUpgrade"):
            if field not in item:
                raise ValueError(f"Missing {field}")
        if item["predictionId"] in identifiers:
            raise ValueError(f"Duplicate predictionId: {item['predictionId']}")
        identifiers.add(item["predictionId"])
        if item["status"] not in STATUSES:
            raise ValueError("Unknown prediction status")
        if item["evidenceUpgrade"] is not False:
            raise ValueError("evidenceUpgrade must remain false per prediction")
        claim = item["claim"]
        if not isinstance(claim.get("value"), (int, float)) or not math.isfinite(claim["value"]) or not claim.get("unit"):
            raise ValueError("claim requires a finite value and unit")
        if "uncertainty" in claim and (not isinstance(claim["uncertainty"], (int, float)) or claim["uncertainty"] < 0):
            raise ValueError("claim uncertainty must be nonnegative")
        if item["status"] == "historical_mismatch":
            observation = item.get("observation")
            if not observation or not all(observation.get(key) is not None for key in ("year", "value", "unit", "source")):
                raise ValueError("historical_mismatch requires a sourced observation")
            if item["revisionRequired"] is not True:
                raise ValueError("historical_mismatch requires revisionRequired=true")
        if item["status"] == "identity_mismatch_warning":
            if item.get("reviewFlag") != "possible_target_identity_confusion" or not item.get("reviewSources"):
                raise ValueError("identity_mismatch_warning requires reviewFlag and reviewSources")
            if item["revisionRequired"] is not True:
                raise ValueError("identity_mismatch_warning requires revisionRequired=true")


def main() -> None:
    registry = json.loads((ROOT / "prediction_registry.json").read_text(encoding="utf-8"))
    validate_registry(registry)
    counts = Counter(item["status"] for item in registry["predictions"])
    print(json.dumps({"predictions": len(registry["predictions"]), "statusCounts": counts, "evidenceUpgrade": False}, ensure_ascii=False))


if __name__ == "__main__":
    main()
