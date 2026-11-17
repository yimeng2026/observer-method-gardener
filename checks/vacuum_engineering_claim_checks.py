#!/usr/bin/env python3
"""Arithmetic and evidence checks for the 2025-12-05 vacuum-theory post.

All displayed engineering and institutional claims remain claims.  These
checks reproduce arithmetic and document boundaries; they do not validate
vacuum-energy extraction, fusion performance, or any government memo.
"""
from __future__ import annotations

from datetime import date
import json
import math

HBAR = 1.054571817e-34
C = 299792458.0
MPC_METRES = 3.0856775814913673e22


def vacuum_density() -> dict[str, float | bool]:
    lambda_c = 5.99153e-13
    alpha = 1 / 137.035999084
    h0 = 67.66 * 1000 / MPC_METRES
    hubble_radius = C / h0
    gamma = 1.280
    scale = HBAR * C / lambda_c**4
    density = (
        scale * alpha**1.5 * (lambda_c / hubble_radius)**(2 / 3) * gamma
    )
    displayed_scale = 2.455e19
    displayed_density = 5.34e-10
    displayed_observation = 5.33e-10
    return {
        "hubbleRadiusMetres": hubble_radius,
        "computedScale": scale,
        "computedScaleOverDisplayed": scale / displayed_scale,
        "displayedScaleSupported": math.isclose(
            scale, displayed_scale, rel_tol=1e-9, abs_tol=0.0
        ),
        "computedDensity": density,
        "computedOverClaimedDensity": density / displayed_density,
        "printedPairRelativeDifference": abs(
            displayed_density - displayed_observation
        ) / displayed_observation,
        "zeroErrorSupported": False,
        "calibrationFactorIndependentlyDerived": False,
        "independentDatasetProvided": False,
        "friedmannExtraTermClosedIfSameGamma": False,
    }


def fusion_economics() -> dict[str, float | bool]:
    thermal_mw = 5000.0
    electric_mw = 2000.0
    capital_usd = 16e9
    annual_revenue = 2e6 * 8760 * 0.02
    fusion_share = 50e12 * 0.30
    revenue_at_shown_price = fusion_share * 0.02
    claimed_annual_value = 1.5e12
    return {
        "grossElectricMwAt45Percent": thermal_mw * 0.45,
        "printedEfficiency": electric_mw / thermal_mw,
        "efficiencyConsistent": math.isclose(
            electric_mw / thermal_mw, 0.45, rel_tol=1e-9, abs_tol=0.0
        ),
        "twoGwCapitalFromDisplayedUnitCost": 8e9 * 2,
        "unitCostAndCapitalConsistent": math.isclose(8e9 * 2, capital_usd),
        "annualRevenueUsd": annual_revenue,
        "paybackAtFullCapacity": capital_usd / annual_revenue,
        "paybackAt85Percent": capital_usd / (annual_revenue * 0.85),
        "sixYearPaybackSupported": capital_usd / annual_revenue <= 6,
        "fusionShareKwh": fusion_share,
        "annualRevenueAtShownPriceUsd": revenue_at_shown_price,
        "claimedAnnualValueUsd": claimed_annual_value,
        "shownPriceSupportsClaimedValue": math.isclose(
            revenue_at_shown_price, claimed_annual_value,
            rel_tol=1e-9, abs_tol=0.0,
        ),
        "irrCashFlowProvided": False,
    }


def performance_table() -> dict[str, float | bool]:
    return {
        "powerDensityRatio": 1e5 / 0.1,
        "fuelUtilizationRatio": 0.95 / 0.001,
        "availabilityRatio": 0.98 / 0.30,
        "gainRatio": 1500 / 10,
        "printedEffectiveGain": (1 / 1e-13) * 1e6,
        "effectiveConfinementGainDerived": False,
        "q1500Measured": False,
        "hundredYearLeadDerived": False,
    }


def document_evidence() -> dict[str, bool]:
    return {
        "simulationLabelPresent": True,
        "memoDateAfterPost": date(2025, 12, 15) > date(2025, 12, 6),
        "officialAuthenticationProvided": False,
        "classificationMarkingsAuthenticateDocument": False,
        "listedAttachmentsIncluded": False,
        "engineeringPerformanceValidated": False,
        "aiPraiseIsIndependentReview": False,
    }


def main() -> None:
    print(json.dumps({
        "schemaVersion": "vacuum-engineering-claim-checks/v1",
        "sourceIds": ["10272549965"],
        "vacuumDensity": vacuum_density(),
        "fusionEconomics": fusion_economics(),
        "performanceTable": performance_table(),
        "documentEvidence": document_evidence(),
        "evidenceUpgrade": False,
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
