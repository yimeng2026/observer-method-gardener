import copy
import json
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from prediction_registry import validate_registry

ROOT = Path(__file__).resolve().parents[1]


class PredictionRegistryTest(unittest.TestCase):
    def setUp(self):
        self.registry = json.loads((ROOT / "prediction_registry.json").read_text(encoding="utf-8"))

    def test_actual_registry_preserves_historical_mismatch(self):
        validate_registry(self.registry)
        item = next(p for p in self.registry["predictions"] if p["predictionId"] == "hme-bc2s-6910")
        self.assertEqual(item["status"], "historical_mismatch")
        self.assertTrue(item["revisionRequired"])

    def test_duplicate_prediction_ids_are_rejected(self):
        registry = copy.deepcopy(self.registry)
        registry["predictions"].append(copy.deepcopy(registry["predictions"][0]))
        with self.assertRaisesRegex(ValueError, "Duplicate"):
            validate_registry(registry)

    def test_mismatch_requires_observation_and_revision(self):
        registry = copy.deepcopy(self.registry)
        item = next(p for p in registry["predictions"] if p["status"] == "historical_mismatch")
        item["revisionRequired"] = False
        with self.assertRaisesRegex(ValueError, "revisionRequired"):
            validate_registry(registry)

    def test_identity_warning_requires_sources_and_revision(self):
        item = next(p for p in self.registry["predictions"] if p["predictionId"] == "hme-eta-b-3s-10355")
        self.assertEqual(item["status"], "identity_mismatch_warning")
        self.assertTrue(item["reviewSources"])
        item["revisionRequired"] = False
        with self.assertRaisesRegex(ValueError, "revisionRequired"):
            validate_registry(self.registry)

    def test_evidence_upgrade_is_rejected(self):
        registry = copy.deepcopy(self.registry)
        registry["evidenceUpgrade"] = True
        with self.assertRaisesRegex(ValueError, "evidenceUpgrade"):
            validate_registry(registry)


if __name__ == "__main__":
    unittest.main()
