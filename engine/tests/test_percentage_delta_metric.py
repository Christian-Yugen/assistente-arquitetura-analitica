import hashlib
import json
import unittest
from pathlib import Path

from engine.calibration.evaluate_met_pctdelta_draft_golden import evaluate

from engine.metrics.percentage_delta import PercentageDeltaConceptProfile, classify_percentage_delta_concept
from engine.profiling.semantic_target import profile_semantic_target


class PercentageDeltaMetricTest(unittest.TestCase):
    def test_emits_only_conceptual_percentage_delta_with_human_block(self):
        candidate = classify_percentage_delta_concept(PercentageDeltaConceptProfile(row_count=20, physical_column_count=2, actual_candidate_count=1, baseline_candidate_count=1, baseline_zero_value_count=0, has_defined_grain=True))
        self.assertEqual(candidate["conceptual_formula"], "((eligible_actual - eligible_baseline) / eligible_baseline) * 100")
        self.assertTrue(candidate["question"]["blocking"])
        self.assertNotIn("dax", candidate)
        self.assertNotIn("power_query", candidate)

    def test_blocks_zero_reference_and_other_unsafe_conditions(self):
        base = {"row_count": 20, "physical_column_count": 2, "actual_candidate_count": 1, "baseline_candidate_count": 1, "baseline_zero_value_count": 0, "has_defined_grain": True}
        self.assertIsNone(classify_percentage_delta_concept(PercentageDeltaConceptProfile(**{**base, "baseline_zero_value_count": 1})))
        for key in ("has_sensitive_signal", "has_formula_signal", "has_undefined_classification", "has_fact_without_grain"):
            self.assertIsNone(classify_percentage_delta_concept(PercentageDeltaConceptProfile(**base, **{key: True})))
        self.assertIsNone(classify_percentage_delta_concept(PercentageDeltaConceptProfile(**{**base, "baseline_candidate_count": 0})))
        self.assertIsNone(classify_percentage_delta_concept(PercentageDeltaConceptProfile(**{**base, "actual_candidate_count": 2})))

    def test_target_profile_preserves_only_aggregate_zero_count(self):
        profile = profile_semantic_target("meta", [0, 1, 2])
        self.assertTrue(profile.header_eligible)
        self.assertEqual(profile.physical_numeric_count, 3)
        self.assertEqual(profile.zero_value_count, 1)

    def test_synthetic_golden_matches_manifest_and_calibration(self):
        root = Path(__file__).resolve().parents[2]
        golden = root / "artifacts/golden/met-pctdelta-draft-golden-v1.json"
        manifest = json.loads((root / "artifacts/golden/met-pctdelta-draft-golden-v1.manifest.json").read_text())
        self.assertEqual(hashlib.sha256(golden.read_bytes()).hexdigest(), manifest["sha256"])
        self.assertEqual(evaluate(), {"tp": 1, "fp": 0, "fn": 0})
        self.assertFalse(manifest["production_authorized"])
