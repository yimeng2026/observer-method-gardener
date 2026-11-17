#!/usr/bin/env python3
"""Arithmetic checks for the millennium-prize and exchange-rate claims."""
from __future__ import annotations

from decimal import Decimal, localcontext
import json


def prize_fund_and_exchange() -> dict[str, Decimal | int]:
    with localcontext() as context:
        context.prec = 50
        total = Decimal(7000000)
        displayed_cny = Decimal("49289873.75")
        return {
            "problemCount": 7,
            "perProblemUsd": Decimal(1000000),
            "totalUsd": total,
            "displayedCny": displayed_cny,
            "impliedCnyPerUsd": displayed_cny / total,
        }


def main() -> None:
    result = prize_fund_and_exchange()
    print(json.dumps({
        "schemaVersion": "millennium-prize-claim-checks/v1",
        "sourceIds": ["10313076061"],
        "problemCount": result["problemCount"],
        "perProblemUsd": str(result["perProblemUsd"]),
        "totalUsd": str(result["totalUsd"]),
        "displayedCny": str(result["displayedCny"]),
        "impliedCnyPerUsd": str(result["impliedCnyPerUsd"]),
        "exchangeRateIsTimeInvariant": False,
        "evidenceUpgrade": False,
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
