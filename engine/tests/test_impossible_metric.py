import hashlib
import json
import unittest
from pathlib import Path

from engine.calibration.evaluate_met_imposs_draft_golden import evaluate

from engine.metrics.impossible import InsufficientMetricConceptProfile, classify_insufficient_metric_concept


class InsufficientMetricTest(unittest.TestCase):
    def test_emits_conceptual_insufficiency_alert_with_blocking_human_question(self):
        candidate = classify_insufficient_metric_concept(
            InsufficientMetricConceptProfile(
                row_count=20,
                physical_column_count=2,
                eligible_measure_candidate_count=0,
                has_defined_grain=True,
            )
        )
        self.assertEqual(candidate["metric_type"], "metric_insufficient_review_required")
        self.assertEqual(candidate["conceptual_formula"], "no_conceptual_metric_without_confirmed_measure")
        self.assertTrue(candidate["question"]["blocking"])
        self.assertNotIn("dax", candidate)
        self.assertNotIn("power_query", candidate)
        self.assertNotIn("column_id", candidate["evidence"])

    def test_blocks_existing_measure_and_all_unsafe_or_ambiguous_conditions(self):
        base = {"row_count": 20, "physical_column_count": 2, "eligible_measure_candidate_count": 0, "has_defined_grain": True}
        self.assertIsNone(classify_insufficient_metric_concept(InsufficientMetricConceptProfile(**{**base, "eligible_measure_candidate_count": 1})))
        for key in ("has_sensitive_signal", "has_formula_signal", "has_undefined_classification", "has_fact_without_grain"):
            self.assertIsNone(classify_insufficient_metric_concept(InsufficientMetricConceptProfile(**base, **{key: True})))
        self.assertIsNone(classify_insufficient_metric_concept(InsufficientMetricConceptProfile(**base, grain_ambiguity_count=1)))
        self.assertIsNone(classify_insufficient_metric_concept(InsufficientMetricConceptProfile(**base, classification_conflict_count=1)))

    def test_synthetic_golden_calibration_is_deterministic(self):
        self.assertEqual(evaluate(), {"tp": 1, "fp": 0, "fn": 0})

    def test_synthetic_golden_matches_manifest_and_production_stays_blocked(self):
        root = Path(__file__).resolve().parents[2]
        golden = root / "artifacts/golden/met-imposs-draft-golden-v1.json"
        manifest = json.loads((root / "artifacts/golden/met-imposs-draft-golden-v1.manifest.json").read_text())
        self.assertEqual(hashlib.sha256(golden.read_bytes()).hexdigest(), manifest["sha256"])
        self.assertEqual(manifest["calibration"], {"tp": 1, "fp": 0, "fn": 0})
        self.assertFalse(manifest["production_authorized"])
