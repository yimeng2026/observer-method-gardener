#!/usr/bin/env python3
"""Check the public HME Bc(2S) claim against the earlier CMS observation."""
from __future__ import annotations
import json
import math


def audit_hme_bc2s_claim() -> dict:
    predicted = 6910.0
    observed = 6871.0
    experimental_uncertainty = math.sqrt(1.2**2 + 0.8**2 + 0.8**2)
    difference = abs(predicted - observed)
    return {
        "schemaVersion": "hme-bc2s-history-check/v1",
        "sourceId": "10980868953",
        "externalSource": "CMS Collaboration, arXiv:1902.00571",
        "observationYear": 2019,
        "postYear": 2026,
        "observationPredatesPost": True,
        "predictedMeV": predicted,
        "claimedUncertaintyMeV": 15.0,
        "observedMeV": observed,
        "observedUncertaintyComponentsMeV": [1.2, 0.8, 0.8],
        "observedCombinedUncertaintyMeV": experimental_uncertainty,
        "absoluteDifferenceMeV": difference,
        "outsideClaimedPlusMinus15MeV": difference > 15.0,
        "exceedsOwn30MeVRevisionThreshold": difference > 30.0,
        "scope": "Historical and arithmetic check only; not an independent experimental analysis or a verdict on every HME model.",
        "evidenceUpgrade": False,
    }


def main() -> None:
    print(json.dumps(audit_hme_bc2s_claim(), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
