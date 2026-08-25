import unittest
from engine.metrics.count import CountConceptProfile, classify_count_concept

class CountMetricTest(unittest.TestCase):
    def test_emits_concept_only_with_human_block(self):
        candidate = classify_count_concept(CountConceptProfile(row_count=20, physical_column_count=2, entity_candidate_count=1, has_defined_grain=True))
        self.assertEqual(candidate["conceptual_formula"], "COUNT(eligible_entity)")
        self.assertTrue(candidate["question"]["blocking"])
        self.assertNotIn("dax", candidate)
    def test_blocks_privacy_formula_ambiguity_and_entity_uncertainty(self):
        base={"row_count":20,"physical_column_count":2,"entity_candidate_count":1,"has_defined_grain":True}
        for key in ("has_sensitive_signal","has_formula_signal","has_undefined_classification","has_fact_without_grain"):
            self.assertIsNone(classify_count_concept(CountConceptProfile(**base, **{key:True})))
        self.assertIsNone(classify_count_concept(CountConceptProfile(**{**base,"entity_candidate_count":2})))
