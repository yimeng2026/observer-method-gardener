import copy
import json
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from theory_diff import validate_record

ROOT = Path(__file__).resolve().parents[1]


class TheoryDiffTest(unittest.TestCase):
    def setUp(self):
        self.record = json.loads((ROOT / "records" / "feq_to_gtft.json").read_text(encoding="utf-8"))

    def test_real_record_preserves_unverified_semantic_boundary(self):
        validate_record(self.record)
        self.assertEqual(self.record["scientificAdvanceStatus"], "unverified")
        self.assertFalse(self.record["evidenceUpgrade"])

    def test_rename_without_observed_changes_cannot_claim_advance(self):
        record = copy.deepcopy(self.record)
        record["observedChanges"] = []
        with self.assertRaisesRegex(ValueError, "observedChanges"):
            validate_record(record)

    def test_evidence_upgrade_is_rejected(self):
        record = copy.deepcopy(self.record)
        record["evidenceUpgrade"] = True
        with self.assertRaisesRegex(ValueError, "evidenceUpgrade"):
            validate_record(record)

    def test_duplicate_change_dimensions_are_rejected(self):
        record = copy.deepcopy(self.record)
        record["observedChanges"].append(copy.deepcopy(record["observedChanges"][0]))
        with self.assertRaisesRegex(ValueError, "dimension"):
            validate_record(record)


if __name__ == "__main__":
    unittest.main()
