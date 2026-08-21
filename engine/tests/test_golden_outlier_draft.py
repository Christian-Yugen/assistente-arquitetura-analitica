import hashlib
import json
import unittest
from pathlib import Path

from engine.profiling.outliers import OutlierProfile
from engine.quality.outliers import OutlierColumnProfile, evaluate_outliers


ROOT = Path(__file__).resolve().parents[2]
GOLDEN_PATH = ROOT / "artifacts/golden/outlier-draft-golden-v1.json"
MANIFEST_PATH = ROOT / "artifacts/golden/outlier-draft-golden-v1.manifest.json"


class GoldenOutlierDraftTests(unittest.TestCase):
    def test_manifest_privacy_and_expected_findings_are_reproducible(self):
        golden_bytes = GOLDEN_PATH.read_bytes()
        golden = json.loads(golden_bytes)
        manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))

        self.assertEqual(hashlib.sha256(golden_bytes).hexdigest(), manifest["sha256"])
        self.assertEqual(golden["dataset_id"], "GD-QLT-OUTLIER-012-001")
        self.assertEqual(golden["rule_id"], "QLT-OUTLIER-012")
        self.assertTrue(all(not value for value in golden["privacy"].values()))

        for scenario in golden["scenarios"]:
            profile = OutlierColumnProfile("Coluna Interna", OutlierProfile(**scenario["column"]["outliers"]))
            observed = [
                {
                    "rule_id": finding["rule_id"],
                    "severity": finding["severity"],
                    "confidence": finding["confidence"],
                    "question": finding["question"] is not None,
                }
                for finding in evaluate_outliers(profile)
            ]
            self.assertEqual(observed, scenario["expected_findings"], scenario["scenario_id"])

        serialized = json.dumps(golden["scenarios"], ensure_ascii=False)
        for forbidden in ("raw_value", "column_name", "sheet_name", "quartile", "fence"):
            self.assertNotIn(forbidden, serialized)
