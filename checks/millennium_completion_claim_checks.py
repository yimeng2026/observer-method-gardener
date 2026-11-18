#!/usr/bin/env python3
"""Evidence and arithmetic checks for the seven-Millennium-problems post.

Matching printed zero ordinates to known values is retained as a table check;
it is not a derivation or a proof of the Riemann hypothesis.
"""
from __future__ import annotations

from functools import lru_cache
import json

import mpmath as mp


@lru_cache(maxsize=1)
def zero_table() -> dict[str, object]:
    mp.mp.dps = 70
    printed = [
        "14.134725141734693",
        "21.022039638771554",
        "25.010857580145688",
        "30.424876125859513",
        "32.935061587739189",
    ]
    actual = [mp.im(mp.zetazero(i)) for i in range(1, 6)]
    errors = [abs(value - mp.mpf(text)) for value, text in zip(actual, printed)]
    return {
        "printedOrdinates": [float(mp.mpf(text)) for text in printed],
        "independentOrdinates": [float(value) for value in actual],
        "absoluteErrors": [float(error) for error in errors],
        "maximumAbsoluteError": float(max(errors)),
        "allPrintedErrorsBelowOneEMinus15": all(
            error < mp.mpf("1e-15") for error in errors
        ),
        "parametersGenerateValues": False,
        "finiteCheckProvesAllZeros": False,
        "conjugatePairsProveCriticalLine": False,
    }


def proof_logic() -> dict[str, int | bool]:
    return {
        "spectralIdentityDemonstrated": False,
        "chiralityProvesCriticalLine": False,
        "hermiticityProvesCriticalLine": False,
        "conjugateSymmetryProvesCriticalLine": False,
        "closedOddDimensionalEulerCharacteristic": 0,
        "closedFiveManifoldCanHaveEulerTwo": False,
        "boundaryOrOtherSettingMustBeSpecified": True,
    }


def problem_registry() -> dict[str, int | bool]:
    return {
        "completeProofDocumentsProvided": 0,
        "allSevenCompleted": False,
        "poincarePreviouslySolved": True,
        "satTspPrototypesProvePEqualsNp": False,
        "zConstantProvesNsRegularity": False,
        "knownEllipticCurvesProveBsd": False,
        "massNumberProvesYangMills": False,
        "independentPeerReviewProvided": False,
        "prizeRecognitionProvided": False,
        "publicProofAvailable": False,
    }


def payment_terms() -> dict[str, int | bool]:
    first = 0.1 * 10000
    later = 5000
    return {
        "firstDemandWanYuan": int(first),
        "laterDemandWanYuan": int(later),
        "laterOverFirst": int(later / first),
        "paymentSubstitutesForPublicProof": False,
    }


def main() -> None:
    print(json.dumps({
        "schemaVersion": "millennium-completion-claim-checks/v1",
        "sourceIds": ["10263493648"],
        "zeroTable": zero_table(),
        "proofLogic": proof_logic(),
        "problemRegistry": problem_registry(),
        "paymentTerms": payment_terms(),
        "evidenceUpgrade": False,
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
