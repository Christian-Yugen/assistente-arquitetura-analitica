import hashlib
import json
import unittest
from pathlib import Path

from engine.calibration.evaluate_met_dax_draft_golden import evaluate
from engine.metrics.dax import DaxTemplateConceptProfile, classify_dax_template_concept


class DaxTemplateMetricTests(unittest.TestCase):
    def test_emits_only_abstract_template_after_confirmed_formula_and_human_confirmation(self):
        candidate = classify_dax_template_concept(
            DaxTemplateConceptProfile(
                row_count=20,
                physical_column_count=2,
                confirmed_conceptual_formula_count=1,
                human_confirmation_count=1,
                has_defined_grain=True,
            )
        )
        self.assertEqual(candidate["metric_type"], "dax_template_review_required")
        self.assertEqual(candidate["conceptual_formula"], "SUM([CONFIRMED_MEASURE])")
        self.assertTrue(candidate["question"]["blocking"])
        self.assertNotIn("column_id", candidate["evidence"])
        self.assertNotIn("value", candidate["evidence"])
        self.assertNotIn("power_query", candidate)

    def test_blocks_without_human_confirmation_or_when_guarded_conditions_exist(self):
        base = {"row_count": 20, "physical_column_count": 2, "confirmed_conceptual_formula_count": 1, "human_confirmation_count": 1, "has_defined_grain": True}
        self.assertIsNone(classify_dax_template_concept(DaxTemplateConceptProfile(**{**base, "human_confirmation_count": 0})))
        self.assertIsNone(classify_dax_template_concept(DaxTemplateConceptProfile(**{**base, "confirmed_conceptual_formula_count": 0})))
        self.assertIsNone(classify_dax_template_concept(DaxTemplateConceptProfile(**{**base, "confirmed_conceptual_formula_count": 2})))
        for key in ("has_sensitive_signal", "has_formula_signal", "has_undefined_classification", "has_fact_without_grain"):
            self.assertIsNone(classify_dax_template_concept(DaxTemplateConceptProfile(**base, **{key: True})))
        self.assertIsNone(classify_dax_template_concept(DaxTemplateConceptProfile(**base, grain_ambiguity_count=1)))
        self.assertIsNone(classify_dax_template_concept(DaxTemplateConceptProfile(**base, classification_conflict_count=1)))

    def test_synthetic_golden_calibration_is_deterministic(self):
        self.assertEqual(evaluate(), {"tp": 1, "fp": 0, "fn": 0})

    def test_synthetic_golden_matches_manifest_and_production_stays_blocked(self):
        root = Path(__file__).resolve().parents[2]
        golden = root / "artifacts/golden/met-dax-draft-golden-v1.json"
        manifest = json.loads((root / "artifacts/golden/met-dax-draft-golden-v1.manifest.json").read_text())
        self.assertEqual(hashlib.sha256(golden.read_bytes()).hexdigest(), manifest["sha256"])
        self.assertEqual(manifest["calibration"], {"tp": 1, "fp": 0, "fn": 0})
        self.assertFalse(manifest["production_authorized"])
