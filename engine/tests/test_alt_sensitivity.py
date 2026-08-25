import hashlib
import json
import unittest
from pathlib import Path

from engine.alerts.sensitivity import SensitiveDataRestrictionProfile, classify_sensitive_data_processing_restriction
from engine.calibration.evaluate_alt_sens_draft_golden import evaluate
from engine.contracts.diagnosis import to_diagnosis_fragment


class SensitiveDataRestrictionTests(unittest.TestCase):
    def test_emits_aggregated_restriction_with_blocking_human_question(self):
        finding = classify_sensitive_data_processing_restriction(
            SensitiveDataRestrictionProfile(sensitivity_signal_candidate_count=1)
        )
        self.assertEqual(finding["rule_id"], "ALT-SENS-001")
        self.assertEqual(finding["severity"], "high")
        self.assertTrue(finding["question"]["blocking"])
        self.assertNotIn("header", str(finding["evidence"]).lower())
        self.assertNotIn("value", finding)
        self.assertNotIn("column_id", finding)

    def test_blocks_absent_multiple_or_conflicting_sensitivity_signals(self):
        self.assertIsNone(classify_sensitive_data_processing_restriction(SensitiveDataRestrictionProfile()))
        self.assertIsNone(classify_sensitive_data_processing_restriction(SensitiveDataRestrictionProfile(sensitivity_signal_candidate_count=2)))
        self.assertIsNone(classify_sensitive_data_processing_restriction(SensitiveDataRestrictionProfile(sensitivity_signal_candidate_count=1, sensitivity_conflict_count=1)))

    def test_contract_projection_keeps_evidence_aggregated(self):
        finding = classify_sensitive_data_processing_restriction(SensitiveDataRestrictionProfile(sensitivity_signal_candidate_count=1))
        fragment = to_diagnosis_fragment([finding], sheet_id="opaque-sheet", column_id="opaque-column")
        projected = fragment["findings"][0]
        self.assertEqual(projected["rule_id"], "ALT-SENS-001")
        self.assertNotIn("header", str(projected["evidence"]).lower())
        self.assertEqual(projected["evidence"][0]["observed"], {"observed_value": 1})
        self.assertNotIn("example", str(projected["evidence"]).lower())

    def test_synthetic_golden_calibration_is_deterministic(self):
        self.assertEqual(evaluate(), {"tp": 1, "fp": 0, "fn": 0})

    def test_synthetic_golden_matches_manifest_and_production_stays_blocked(self):
        root = Path(__file__).resolve().parents[2]
        golden = root / "artifacts/golden/alt-sens-draft-golden-v1.json"
        manifest = json.loads((root / "artifacts/golden/alt-sens-draft-golden-v1.manifest.json").read_text())
        self.assertEqual(hashlib.sha256(golden.read_bytes()).hexdigest(), manifest["sha256"])
        self.assertEqual(manifest["calibration"], {"tp": 1, "fp": 0, "fn": 0})
        self.assertFalse(manifest["production_authorized"])
