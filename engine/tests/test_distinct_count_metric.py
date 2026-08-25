import unittest
from engine.metrics.distinct_count import DistinctCountConceptProfile, classify_distinct_count_concept

class DistinctCountMetricTest(unittest.TestCase):
    def test_emits_only_conceptual_distinct_count_with_human_block(self):
        candidate=classify_distinct_count_concept(DistinctCountConceptProfile(row_count=20,physical_column_count=2,entity_candidate_count=1,has_defined_grain=True))
        self.assertEqual(candidate["conceptual_formula"],"DISTINCTCOUNT(eligible_entity)")
        self.assertTrue(candidate["question"]["blocking"])
        self.assertNotIn("dax",candidate)
    def test_blocks_sensitive_formula_and_ambiguous_entity(self):
        base={"row_count":20,"physical_column_count":2,"entity_candidate_count":1,"has_defined_grain":True}
        for key in ("has_sensitive_signal","has_formula_signal","has_undefined_classification","has_fact_without_grain"):
            self.assertIsNone(classify_distinct_count_concept(DistinctCountConceptProfile(**base,**{key:True})))
        self.assertIsNone(classify_distinct_count_concept(DistinctCountConceptProfile(**{**base,"entity_candidate_count":2})))
