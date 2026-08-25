import hashlib
import json
import unittest
from pathlib import Path
from engine.calibration.evaluate_met_rate_draft_golden import evaluate
from engine.metrics.rate import RateConceptProfile, classify_rate_concept
class RateMetricTest(unittest.TestCase):
    def test_emits_only_conceptual_rate_with_human_block(self):
        candidate=classify_rate_concept(RateConceptProfile(row_count=20,physical_column_count=2,numerator_candidate_count=1,denominator_candidate_count=1,has_defined_grain=True))
        self.assertEqual(candidate["conceptual_formula"],"eligible_numerator / eligible_denominator")
        self.assertTrue(candidate["question"]["blocking"])
        self.assertNotIn("dax",candidate)
    def test_blocks_sensitive_formula_and_missing_pair(self):
        base={"row_count":20,"physical_column_count":2,"numerator_candidate_count":1,"denominator_candidate_count":1,"has_defined_grain":True}
        for key in ("has_sensitive_signal","has_formula_signal","has_undefined_classification","has_fact_without_grain"):
            self.assertIsNone(classify_rate_concept(RateConceptProfile(**base,**{key:True})))
        self.assertIsNone(classify_rate_concept(RateConceptProfile(**{**base,"denominator_candidate_count":0})))

    def test_synthetic_golden_matches_manifest_and_calibration(self):
        root = Path(__file__).resolve().parents[2]
        golden = root / "artifacts/golden/met-rate-draft-golden-v1.json"
        manifest = json.loads((root / "artifacts/golden/met-rate-draft-golden-v1.manifest.json").read_text())
        self.assertEqual(hashlib.sha256(golden.read_bytes()).hexdigest(), manifest["sha256"])
        self.assertEqual(evaluate(), {"tp": 1, "fp": 0, "fn": 0})
        self.assertFalse(manifest["production_authorized"])
