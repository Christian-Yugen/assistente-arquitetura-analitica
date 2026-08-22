from __future__ import annotations

import hashlib
import json
import unittest
from pathlib import Path

from engine.calibration.evaluate_rel_onemany_draft_golden import evaluate


class GoldenRelOneManyTests(unittest.TestCase):
    def test_calibration_has_no_false_positives_or_false_negatives(self):
        self.assertEqual(evaluate(), {"tp": 3, "fp": 0, "fn": 0})

    def test_dataset_is_synthetic_and_matches_its_manifest_hash(self):
        root = Path(__file__).resolve().parents[2]
        dataset_path = root / "artifacts/golden/rel-onemany-draft-golden-v1.json"
        manifest_path = root / "artifacts/golden/rel-onemany-draft-golden-v1.manifest.json"
        dataset = json.loads(dataset_path.read_text(encoding="utf-8"))
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))

        self.assertTrue(dataset["synthetic_only"])
        self.assertTrue(manifest["synthetic_only"])
        self.assertEqual(
            hashlib.sha256(dataset_path.read_bytes()).hexdigest(),
            manifest["sha256"],
        )
