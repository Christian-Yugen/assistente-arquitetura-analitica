import unittest
from engine.metrics.average import AverageConceptProfile, classify_average_concept
class AverageMetricTest(unittest.TestCase):
    def test_emits_only_conceptual_average_with_human_block(self):
        candidate=classify_average_concept(AverageConceptProfile(row_count=20,physical_column_count=2,summable_candidate_count=1,has_defined_grain=True))
        self.assertEqual(candidate["conceptual_formula"],"AVERAGE(eligible_measure)")
        self.assertTrue(candidate["question"]["blocking"])
        self.assertNotIn("dax",candidate)
    def test_blocks_sensitive_formula_and_ambiguous_measure(self):
        base={"row_count":20,"physical_column_count":2,"summable_candidate_count":1,"has_defined_grain":True}
        for key in ("has_sensitive_signal","has_formula_signal","has_undefined_classification","has_fact_without_grain"):
            self.assertIsNone(classify_average_concept(AverageConceptProfile(**base,**{key:True})))
        self.assertIsNone(classify_average_concept(AverageConceptProfile(**{**base,"summable_candidate_count":2})))
