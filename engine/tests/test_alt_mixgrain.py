import hashlib
import json
import unittest
from pathlib import Path

from engine.alerts.mixed_grain import MixedGrainAlertProfile, classify_mixed_grain_review
from engine.calibration.evaluate_alt_mixgrain_draft_golden import evaluate
from engine.contracts.diagnosis import to_diagnosis_fragment


class MixedGrainAlertTests(unittest.TestCase):
    def test_emits_blocking_review_from_synthetic_independent_signal(self):
        finding = classify_mixed_grain_review(MixedGrainAlertProfile(independent_mixed_grain_signal_count=1))
        self.assertEqual(finding["rule_id"], "ALT-MIXGRAIN-009")
        self.assertEqual(finding["severity"], "high")
        self.assertTrue(finding["question"]["blocking"])
        self.assertNotIn("header", str(finding["evidence"]).lower())
        self.assertNotIn("column_id", finding)

    def test_blocks_without_signal_or_when_confirmation_conflict_sensitivity_or_contract_error_exists(self):
        self.assertIsNone(classify_mixed_grain_review(MixedGrainAlertProfile()))
        self.assertIsNone(classify_mixed_grain_review(MixedGrainAlertProfile(independent_mixed_grain_signal_count=1, confirmed_single_grain_count=1)))
        self.assertIsNone(classify_mixed_grain_review(MixedGrainAlertProfile(independent_mixed_grain_signal_count=1, structural_conflict_count=1)))
        self.assertIsNone(classify_mixed_grain_review(MixedGrainAlertProfile(independent_mixed_grain_signal_count=1, sensitive_signal_count=1)))
        self.assertIsNone(classify_mixed_grain_review(MixedGrainAlertProfile(independent_mixed_grain_signal_count=1, contract_error_count=1)))

    def test_contract_projection_keeps_only_aggregate_signal_count(self):
        finding = classify_mixed_grain_review(MixedGrainAlertProfile(independent_mixed_grain_signal_count=1))
        fragment = to_diagnosis_fragment([finding], sheet_id="model", column_id="model")
        projected = fragment["findings"][0]
        self.assertEqual(projected["rule_id"], "ALT-MIXGRAIN-009")
        self.assertEqual(projected["evidence"][0]["observed"], {"observed_value": 1})
        self.assertNotIn("header", str(projected["evidence"]).lower())
        self.assertNotIn("example", str(projected["evidence"]).lower())

    def test_synthetic_golden_calibration_is_deterministic(self):
        self.assertEqual(evaluate(), {"tp": 1, "fp": 0, "fn": 0})

    def test_synthetic_golden_matches_manifest_and_production_stays_blocked(self):
        root = Path(__file__).resolve().parents[2]
        golden = root / "artifacts/golden/alt-mixgrain-draft-golden-v1.json"
        manifest = json.loads((root / "artifacts/golden/alt-mixgrain-draft-golden-v1.manifest.json").read_text())
        self.assertEqual(hashlib.sha256(golden.read_bytes()).hexdigest(), manifest["sha256"])
        self.assertEqual(manifest["calibration"], {"tp": 1, "fp": 0, "fn": 0})
        self.assertFalse(manifest["production_authorized"])

