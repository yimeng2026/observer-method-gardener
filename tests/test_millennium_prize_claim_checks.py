from pathlib import Path
from decimal import Decimal
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
try:
    from checks.millennium_prize_claim_checks import prize_fund_and_exchange
except ModuleNotFoundError:
    prize_fund_and_exchange = None


class MillenniumPrizeClaimChecksTest(unittest.TestCase):
    def setUp(self):
        self.assertTrue(prize_fund_and_exchange, "prize checker function must exist")

    def test_seven_problems_have_one_million_dollars_each(self):
        result = prize_fund_and_exchange()
        self.assertEqual(result["problemCount"], 7)
        self.assertEqual(result["perProblemUsd"], Decimal("1000000"))
        self.assertEqual(result["totalUsd"], Decimal("7000000"))

    def test_displayed_rmb_amount_only_implies_an_exchange_rate(self):
        result = prize_fund_and_exchange()
        self.assertEqual(result["impliedCnyPerUsd"], Decimal("7.0414105357142857142857142857142857142857142857143"))
        self.assertNotEqual(result["impliedCnyPerUsd"], Decimal("7"))


if __name__ == "__main__":
    unittest.main()
