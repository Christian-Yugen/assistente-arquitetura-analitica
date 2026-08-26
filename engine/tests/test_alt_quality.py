import hashlib
import json
import unittest
from pathlib import Path

from engine.alerts.quality import CriticalQualityRiskProfile, classify_critical_quality_risk
from engine.calibration.evaluate_alt_quality_draft_golden import evaluate
from engine.contracts.diagnosis import to_diagnosis_fragment


class CriticalQualityRiskTests(unittest.TestCase):
    def test_emits_aggregated_model_risk_with_blocking_human_question(self):
        finding = classify_critical_quality_risk(
            CriticalQualityRiskProfile(high_quality_finding_count=3, distinct_quality_rule_count=2, analyzed_sheet_count=1)
        )
        self.assertEqual(finding["rule_id"], "ALT-QUALITY-002")
        self.assertEqual(finding["severity"], "high")
        self.assertTrue(finding["question"]["blocking"])
        self.assertNotIn("header", str(finding["evidence"]).lower())
        self.assertNotIn("column_id", finding)

    def test_blocks_when_quality_aggregate_threshold_or_contract_guard_is_not_met(self):
        base = {"high_quality_finding_count": 3, "distinct_quality_rule_count": 2, "analyzed_sheet_count": 1}
        self.assertIsNone(classify_critical_quality_risk(CriticalQualityRiskProfile(**{**base, "high_quality_finding_count": 2})))
        self.assertIsNone(classify_critical_quality_risk(CriticalQualityRiskProfile(**{**base, "distinct_quality_rule_count": 1})))
        self.assertIsNone(classify_critical_quality_risk(CriticalQualityRiskProfile(**{**base, "analyzed_sheet_count": 0})))
        self.assertIsNone(classify_critical_quality_risk(CriticalQualityRiskProfile(**{**base, "contract_error_count": 1})))

    def test_contract_projection_keeps_only_aggregate_counts(self):
        finding = classify_critical_quality_risk(
            CriticalQualityRiskProfile(high_quality_finding_count=3, distinct_quality_rule_count=2, analyzed_sheet_count=1)
        )
        fragment = to_diagnosis_fragment([finding], sheet_id="model", column_id="model")
        projected = fragment["findings"][0]
        self.assertEqual(projected["rule_id"], "ALT-QUALITY-002")
        self.assertEqual(projected["evidence"][0]["observed"], {"observed_value": 3})
        self.assertNotIn("header", str(projected["evidence"]).lower())
        self.assertNotIn("example", str(projected["evidence"]).lower())

    def test_synthetic_golden_calibration_is_deterministic(self):
        self.assertEqual(evaluate(), {"tp": 1, "fp": 0, "fn": 0})

    def test_synthetic_golden_matches_manifest_and_production_stays_blocked(self):
        root = Path(__file__).resolve().parents[2]
        golden = root / "artifacts/golden/alt-quality-draft-golden-v1.json"
        manifest = json.loads((root / "artifacts/golden/alt-quality-draft-golden-v1.manifest.json").read_text())
        self.assertEqual(hashlib.sha256(golden.read_bytes()).hexdigest(), manifest["sha256"])
        self.assertEqual(manifest["calibration"], {"tp": 1, "fp": 0, "fn": 0})
        self.assertFalse(manifest["production_authorized"])
