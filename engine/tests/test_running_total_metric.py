import hashlib
import json
import unittest
from pathlib import Path

from engine.calibration.evaluate_met_running_draft_golden import evaluate

from engine.metrics.running_total import RunningTotalConceptProfile, classify_running_total_concept
from engine.profiling.semantic_date import profile_semantic_date


class RunningTotalMetricTest(unittest.TestCase):
    def test_emits_only_conceptual_running_total_with_human_block(self):
        candidate = classify_running_total_concept(RunningTotalConceptProfile(row_count=20, physical_column_count=2, measure_candidate_count=1, temporal_order_candidate_count=1, temporal_order_duplicate_count=0, has_defined_grain=True))
        self.assertEqual(candidate["conceptual_formula"], "cumulative eligible_measure ordered by eligible_time")
        self.assertTrue(candidate["question"]["blocking"])
        self.assertNotIn("dax", candidate)
        self.assertNotIn("power_query", candidate)

    def test_blocks_duplicate_or_missing_temporal_order_and_other_unsafe_conditions(self):
        base = {"row_count": 20, "physical_column_count": 2, "measure_candidate_count": 1, "temporal_order_candidate_count": 1, "temporal_order_duplicate_count": 0, "has_defined_grain": True}
        self.assertIsNone(classify_running_total_concept(RunningTotalConceptProfile(**{**base, "temporal_order_duplicate_count": 1})))
        self.assertIsNone(classify_running_total_concept(RunningTotalConceptProfile(**{**base, "temporal_order_candidate_count": 0})))
        self.assertIsNone(classify_running_total_concept(RunningTotalConceptProfile(**{**base, "measure_candidate_count": 2})))
        for key in ("has_sensitive_signal", "has_formula_signal", "has_undefined_classification", "has_fact_without_grain"):
            self.assertIsNone(classify_running_total_concept(RunningTotalConceptProfile(**base, **{key: True})))

    def test_date_profile_preserves_only_aggregate_distinct_date_count(self):
        profile = profile_semantic_date(["01/01/2026", "01/01/2026", "02/01/2026"])
        self.assertEqual(profile.recognized_date_count, 3)
        self.assertEqual(profile.distinct_recognized_date_count, 2)

    def test_synthetic_golden_matches_manifest_and_calibration(self):
        root = Path(__file__).resolve().parents[2]
        golden = root / "artifacts/golden/met-running-draft-golden-v1.json"
        manifest = json.loads((root / "artifacts/golden/met-running-draft-golden-v1.manifest.json").read_text())
        self.assertEqual(hashlib.sha256(golden.read_bytes()).hexdigest(), manifest["sha256"])
        self.assertEqual(evaluate(), {"tp": 1, "fp": 0, "fn": 0})
        self.assertFalse(manifest["production_authorized"])
