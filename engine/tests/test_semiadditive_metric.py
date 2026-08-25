import hashlib
import json
import unittest
from pathlib import Path

from engine.calibration.evaluate_met_semiadd_draft_golden import evaluate

from engine.metrics.semiadditive import SemiadditiveConceptProfile, classify_semiadditive_concept


class SemiadditiveMetricTest(unittest.TestCase):
    def test_emits_only_conceptual_semiadditive_metric_with_human_block(self):
        candidate = classify_semiadditive_concept(SemiadditiveConceptProfile(row_count=20, physical_column_count=2, potential_balance_candidate_count=1, temporal_order_candidate_count=1, temporal_order_duplicate_count=0, has_defined_grain=True))
        self.assertEqual(candidate["conceptual_formula"], "aggregate eligible_balance across confirmed non_time_dimensions at confirmed time_grain")
        self.assertTrue(candidate["question"]["blocking"])
        self.assertNotIn("dax", candidate)
        self.assertNotIn("power_query", candidate)

    def test_blocks_ambiguous_time_or_balance_and_other_unsafe_conditions(self):
        base = {"row_count": 20, "physical_column_count": 2, "potential_balance_candidate_count": 1, "temporal_order_candidate_count": 1, "temporal_order_duplicate_count": 0, "has_defined_grain": True}
        self.assertIsNone(classify_semiadditive_concept(SemiadditiveConceptProfile(**{**base, "temporal_order_duplicate_count": 1})))
        self.assertIsNone(classify_semiadditive_concept(SemiadditiveConceptProfile(**{**base, "temporal_order_candidate_count": 0})))
        self.assertIsNone(classify_semiadditive_concept(SemiadditiveConceptProfile(**{**base, "potential_balance_candidate_count": 2})))
        for key in ("has_sensitive_signal", "has_formula_signal", "has_undefined_classification", "has_fact_without_grain"):
            self.assertIsNone(classify_semiadditive_concept(SemiadditiveConceptProfile(**base, **{key: True})))

    def test_synthetic_golden_matches_manifest_and_calibration(self):
        root = Path(__file__).resolve().parents[2]
        golden = root / "artifacts/golden/met-semiadd-draft-golden-v1.json"
        manifest = json.loads((root / "artifacts/golden/met-semiadd-draft-golden-v1.manifest.json").read_text())
        self.assertEqual(hashlib.sha256(golden.read_bytes()).hexdigest(), manifest["sha256"])
        self.assertEqual(evaluate(), {"tp": 1, "fp": 0, "fn": 0})
        self.assertFalse(manifest["production_authorized"])
