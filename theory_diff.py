#!/usr/bin/env python3
"""Validate source-bounded semantic differences between named theory versions."""
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REQUIRED = {
    "schemaVersion", "recordId", "from", "to", "observedChanges",
    "parameterProvenanceStatus", "knownLimitStatus", "predictionDiffStatus",
    "scientificAdvanceStatus", "evidenceUpgrade",
}


def validate_record(record: dict) -> None:
    missing = sorted(REQUIRED - set(record))
    if missing:
        raise ValueError(f"Missing fields: {', '.join(missing)}")
    if record["schemaVersion"] != "theory-diff/v1":
        raise ValueError("Unsupported schemaVersion")
    for side in ("from", "to"):
        if not isinstance(record[side], dict) or not record[side].get("name") or not record[side].get("sourceId"):
            raise ValueError(f"{side} requires name and sourceId")
    changes = record["observedChanges"]
    if not isinstance(changes, list) or not changes:
        raise ValueError("observedChanges must contain at least one documented change")
    dimensions = []
    for change in changes:
        if not isinstance(change, dict) or any(not change.get(key) for key in ("dimension", "before", "after", "evidenceLocator")):
            raise ValueError("Each change requires dimension, before, after and evidenceLocator")
        dimensions.append(change["dimension"])
    if len(dimensions) != len(set(dimensions)):
        raise ValueError("Each change dimension must be unique")
    if record["evidenceUpgrade"] is not False:
        raise ValueError("evidenceUpgrade must remain false for a semantic ledger")
    if record["scientificAdvanceStatus"] not in {"unverified", "rebranding", "bounded_technical_change"}:
        raise ValueError("scientificAdvanceStatus requires a bounded, non-proof status")


def main() -> None:
    paths = sorted((ROOT / "records").glob("*.json"))
    for path in paths:
        validate_record(json.loads(path.read_text(encoding="utf-8")))
    print(json.dumps({"recordsValidated": len(paths), "evidenceUpgrade": False}, ensure_ascii=False))


if __name__ == "__main__":
    main()
