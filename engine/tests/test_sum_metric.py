import unittest

from engine.metrics.sum import SumConceptProfile, classify_sum_concept


class SumMetricTest(unittest.TestCase):
    def test_emits_only_conceptual_review_with_blocking_question(self):
        candidate = classify_sum_concept(SumConceptProfile(row_count=20, physical_column_count=2, summable_candidate_count=1, has_defined_grain=True))
        self.assertEqual(candidate["metric_type"], "sum_conceptual_metric_candidate")
        self.assertEqual(candidate["conceptual_formula"], "SUM(eligible_measure)")
        self.assertTrue(candidate["question"]["blocking"])
        self.assertNotIn("dax", candidate["conceptual_formula"].lower())
        self.assertNotIn("measure_id", candidate)
        self.assertNotIn("dax", candidate)

    def test_blocks_every_policy_guard(self):
        base = {"row_count": 20, "physical_column_count": 2, "summable_candidate_count": 1, "has_defined_grain": True}
        for guard in ("has_sensitive_signal", "has_formula_signal", "has_undefined_classification", "has_fact_without_grain"):
            self.assertIsNone(classify_sum_concept(SumConceptProfile(**base, **{guard: True})))
        self.assertIsNone(classify_sum_concept(SumConceptProfile(**base, grain_ambiguity_count=1)))
        self.assertIsNone(classify_sum_concept(SumConceptProfile(**base, classification_conflict_count=1)))
        self.assertIsNone(classify_sum_concept(SumConceptProfile(**{**base, "summable_candidate_count": 2})))
