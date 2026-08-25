import hashlib
import json
import unittest
from pathlib import Path

from engine.calibration.evaluate_rel_ambig_draft_golden import evaluate


class AmbiguousRelationshipPathGoldenDatasetTests(unittest.TestCase):
    def test_dataset_is_synthetic_and_calibrates_without_known_errors(self):
        path = Path(__file__).resolve().parents[2] / "artifacts/golden/rel-ambig-draft-golden-v1.json"
        dataset = json.loads(path.read_text(encoding="utf-8"))

        self.assertEqual(dataset["rule_id"], "REL-AMBIG-007")
        self.assertTrue(dataset["synthetic_only"])
        self.assertEqual(evaluate(), {"tp": 3, "fp": 0, "fn": 0})

    def test_manifest_hash_matches_the_synthetic_dataset(self):
        root = Path(__file__).resolve().parents[2]
        dataset_path = root / "artifacts/golden/rel-ambig-draft-golden-v1.json"
        manifest_path = root / "artifacts/golden/rel-ambig-draft-golden-v1.manifest.json"
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))

        self.assertEqual(hashlib.sha256(dataset_path.read_bytes()).hexdigest(), manifest["sha256"])
