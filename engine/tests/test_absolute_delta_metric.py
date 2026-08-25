import hashlib
import json
import unittest
from pathlib import Path

from engine.calibration.evaluate_met_absdelta_draft_golden import evaluate

from engine.metrics.absolute_delta import AbsoluteDeltaConceptProfile, classify_absolute_delta_concept


class AbsoluteDeltaMetricTest(unittest.TestCase):
    def test_emits_only_conceptual_delta_with_human_block(self):
        candidate = classify_absolute_delta_concept(AbsoluteDeltaConceptProfile(row_count=20, physical_column_count=2, actual_candidate_count=1, baseline_candidate_count=1, has_defined_grain=True))
        self.assertEqual(candidate["conceptual_formula"], "eligible_actual - eligible_baseline")
        self.assertTrue(candidate["question"]["blocking"])
        self.assertNotIn("dax", candidate)
        self.assertNotIn("power_query", candidate)

    def test_blocks_sensitive_formula_missing_and_ambiguous_components(self):
        base = {"row_count": 20, "physical_column_count": 2, "actual_candidate_count": 1, "baseline_candidate_count": 1, "has_defined_grain": True}
        for key in ("has_sensitive_signal", "has_formula_signal", "has_undefined_classification", "has_fact_without_grain"):
            self.assertIsNone(classify_absolute_delta_concept(AbsoluteDeltaConceptProfile(**base, **{key: True})))
        self.assertIsNone(classify_absolute_delta_concept(AbsoluteDeltaConceptProfile(**{**base, "baseline_candidate_count": 0})))
        self.assertIsNone(classify_absolute_delta_concept(AbsoluteDeltaConceptProfile(**{**base, "actual_candidate_count": 2})))

    def test_synthetic_golden_matches_manifest_and_calibration(self):
        root = Path(__file__).resolve().parents[2]
        golden = root / "artifacts/golden/met-absdelta-draft-golden-v1.json"
        manifest = json.loads((root / "artifacts/golden/met-absdelta-draft-golden-v1.manifest.json").read_text())
        self.assertEqual(hashlib.sha256(golden.read_bytes()).hexdigest(), manifest["sha256"])
        self.assertEqual(evaluate(), {"tp": 1, "fp": 0, "fn": 0})
        self.assertFalse(manifest["production_authorized"])
