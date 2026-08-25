import hashlib
import json
import unittest
from pathlib import Path

from engine.calibration.evaluate_met_wavg_draft_golden import evaluate

from engine.metrics.weighted_average import WeightedAverageConceptProfile, classify_weighted_average_concept
from engine.profiling.semantic_quantity import profile_semantic_quantity


class WeightedAverageMetricTest(unittest.TestCase):
    def test_emits_only_conceptual_weighted_average_with_human_block(self):
        candidate = classify_weighted_average_concept(WeightedAverageConceptProfile(row_count=20, physical_column_count=2, measure_candidate_count=1, weight_candidate_count=1, nonpositive_weight_count=0, has_defined_grain=True))
        self.assertEqual(candidate["conceptual_formula"], "weighted_sum(eligible_measure, eligible_weight) / total(eligible_weight)")
        self.assertTrue(candidate["question"]["blocking"])
        self.assertNotIn("dax", candidate)
        self.assertNotIn("power_query", candidate)

    def test_blocks_nonpositive_weight_and_other_unsafe_conditions(self):
        base = {"row_count": 20, "physical_column_count": 2, "measure_candidate_count": 1, "weight_candidate_count": 1, "nonpositive_weight_count": 0, "has_defined_grain": True}
        self.assertIsNone(classify_weighted_average_concept(WeightedAverageConceptProfile(**{**base, "nonpositive_weight_count": 1})))
        self.assertIsNone(classify_weighted_average_concept(WeightedAverageConceptProfile(**{**base, "weight_candidate_count": 0})))
        self.assertIsNone(classify_weighted_average_concept(WeightedAverageConceptProfile(**{**base, "measure_candidate_count": 2})))
        for key in ("has_sensitive_signal", "has_formula_signal", "has_undefined_classification", "has_fact_without_grain"):
            self.assertIsNone(classify_weighted_average_concept(WeightedAverageConceptProfile(**base, **{key: True})))

    def test_quantity_profile_preserves_only_aggregate_nonpositive_count(self):
        profile = profile_semantic_quantity("qtd", [1, 0, -1])
        self.assertTrue(profile.header_eligible)
        self.assertEqual(profile.physical_numeric_count, 3)
        self.assertEqual(profile.nonpositive_value_count, 2)

    def test_synthetic_golden_matches_manifest_and_calibration(self):
        root = Path(__file__).resolve().parents[2]
        golden = root / "artifacts/golden/met-wavg-draft-golden-v1.json"
        manifest = json.loads((root / "artifacts/golden/met-wavg-draft-golden-v1.manifest.json").read_text())
        self.assertEqual(hashlib.sha256(golden.read_bytes()).hexdigest(), manifest["sha256"])
        self.assertEqual(evaluate(), {"tp": 1, "fp": 0, "fn": 0})
        self.assertFalse(manifest["production_authorized"])
