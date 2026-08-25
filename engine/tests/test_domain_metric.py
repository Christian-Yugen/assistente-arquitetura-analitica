import hashlib
import json
import unittest
from pathlib import Path

from engine.calibration.evaluate_met_domain_draft_golden import evaluate

from engine.metrics.domain import DomainMetricConceptProfile, classify_domain_metric_concept


class DomainMetricTest(unittest.TestCase):
    def test_emits_only_opaque_conceptual_domain_metric_with_human_block(self):
        candidate = classify_domain_metric_concept(DomainMetricConceptProfile(row_count=20, physical_column_count=2, domain_signal_candidate_count=1, has_defined_grain=True))
        self.assertEqual(candidate["conceptual_formula"], "confirmed_domain_metric")
        self.assertTrue(candidate["question"]["blocking"])
        self.assertNotIn("dax", candidate)
        self.assertNotIn("power_query", candidate)
        self.assertNotIn("domain_name", candidate["evidence"])

    def test_blocks_absent_or_ambiguous_domain_signal_and_unsafe_conditions(self):
        base = {"row_count": 20, "physical_column_count": 2, "domain_signal_candidate_count": 1, "has_defined_grain": True}
        self.assertIsNone(classify_domain_metric_concept(DomainMetricConceptProfile(**{**base, "domain_signal_candidate_count": 0})))
        self.assertIsNone(classify_domain_metric_concept(DomainMetricConceptProfile(**{**base, "domain_signal_candidate_count": 2})))
        for key in ("has_sensitive_signal", "has_formula_signal", "has_undefined_classification", "has_fact_without_grain"):
            self.assertIsNone(classify_domain_metric_concept(DomainMetricConceptProfile(**base, **{key: True})))

    def test_synthetic_golden_matches_manifest_and_calibration(self):
        root = Path(__file__).resolve().parents[2]
        golden = root / "artifacts/golden/met-domain-draft-golden-v1.json"
        manifest = json.loads((root / "artifacts/golden/met-domain-draft-golden-v1.manifest.json").read_text())
        self.assertEqual(hashlib.sha256(golden.read_bytes()).hexdigest(), manifest["sha256"])
        self.assertEqual(evaluate(), {"tp": 1, "fp": 0, "fn": 0})
        self.assertFalse(manifest["production_authorized"])
