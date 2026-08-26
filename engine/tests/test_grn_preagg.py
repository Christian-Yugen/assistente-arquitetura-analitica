import hashlib
import json
import unittest
from pathlib import Path

from engine.alerts.pre_aggregation import PreAggregationProfile, classify_pre_aggregation
from engine.calibration.evaluate_grn_preagg_draft_golden import evaluate
from engine.contracts.diagnosis import RULE_VERSIONS, to_diagnosis_fragment


GOLDEN_DIR = Path(__file__).resolve().parents[2] / "artifacts" / "golden"


class PreAggregationTests(unittest.TestCase):
    def test_emits_only_for_independent_aggregate_signal(self):
        finding = classify_pre_aggregation(PreAggregationProfile(independent_pre_aggregation_signal_count=1))
        self.assertEqual(finding["rule_id"], "GRN-PREAGG-008")
        self.assertTrue(finding["question"]["blocking"])
        for profile in (PreAggregationProfile(), PreAggregationProfile(independent_pre_aggregation_signal_count=1, confirmed_pre_aggregation_count=1), PreAggregationProfile(independent_pre_aggregation_signal_count=1, structural_conflict_count=1), PreAggregationProfile(independent_pre_aggregation_signal_count=1, sensitive_signal_count=1), PreAggregationProfile(independent_pre_aggregation_signal_count=1, contract_error_count=1)):
            self.assertIsNone(classify_pre_aggregation(profile))

    def test_projects_only_aggregate_finding_with_registered_version(self):
        finding = classify_pre_aggregation(PreAggregationProfile(independent_pre_aggregation_signal_count=2))
        fragment = to_diagnosis_fragment([finding], sheet_id="opaque-sheet", column_id=None)
        self.assertEqual(RULE_VERSIONS["GRN-PREAGG-008"], "0.1.0-provisional.1")
        self.assertEqual(fragment["findings"][0]["rule_version"], "0.1.0-provisional.1")
        self.assertEqual(fragment["findings"][0]["evidence"][0]["observed"], {"observed_value": 2})

    def test_synthetic_golden_hash_calibration_and_fail_closed_cases(self):
        manifest = json.loads((GOLDEN_DIR / "grn-preagg-draft-golden-v1.manifest.json").read_text(encoding="utf-8"))
        golden_path = GOLDEN_DIR / manifest["file"]
        golden = json.loads(golden_path.read_text(encoding="utf-8"))
        self.assertTrue(manifest["synthetic_only"])
        self.assertFalse(manifest["production_authorized"])
        self.assertEqual(manifest["calibration"], {"tp": 1, "fp": 0, "fn": 0})
        self.assertEqual(hashlib.sha256(golden_path.read_bytes()).hexdigest(), manifest["sha256"])
        self.assertEqual(evaluate(), manifest["calibration"])
        for case in golden["cases"]:
            profile = PreAggregationProfile(**(golden["profile_defaults"] | case["overrides"]))
            self.assertEqual(classify_pre_aggregation(profile) is not None, case["expected_finding"])

