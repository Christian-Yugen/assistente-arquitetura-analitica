import dataclasses
import unittest

from engine.metrics.completion import CompletionRateConceptProfile, classify_completion_rate_concept


class CompletionMetricTests(unittest.TestCase):
    def valid_profile(self, **overrides: object) -> CompletionRateConceptProfile:
        values: dict[str, object] = {
            "row_count": 20,
            "physical_column_count": 2,
            "status_candidate_count": 1,
            "has_defined_grain": True,
        }
        values.update(overrides)
        return CompletionRateConceptProfile(**values)

    def test_emits_only_a_conceptual_human_review_metric(self):
        candidate = classify_completion_rate_concept(self.valid_profile())

        assert candidate is not None
        self.assertEqual(candidate["rule_id"], "MET-COMPL-001")
        self.assertEqual(candidate["metric_type"], "completion_rate_conceptual_metric_candidate")
        self.assertEqual(candidate["conceptual_formula"], "completed_items / eligible_items")
        self.assertTrue(candidate["question"]["blocking"])
        self.assertNotIn("dax", candidate)
        self.assertNotIn("status_values", candidate["evidence"])

    def test_blocks_incomplete_ambiguous_or_sensitive_metric_contexts(self):
        blocking_overrides = (
            {"row_count": 19}, {"physical_column_count": 1}, {"status_candidate_count": 0},
            {"status_candidate_count": 2}, {"has_defined_grain": False}, {"grain_ambiguity_count": 1},
            {"has_undefined_classification": True}, {"has_fact_without_grain": True},
            {"classification_conflict_count": 1}, {"has_sensitive_signal": True}, {"has_formula_signal": True},
        )
        for overrides in blocking_overrides:
            with self.subTest(overrides=overrides):
                self.assertIsNone(classify_completion_rate_concept(self.valid_profile(**overrides)))

    def test_private_profile_has_no_status_values_headers_positions_or_dax(self):
        field_names = {field.name for field in dataclasses.fields(CompletionRateConceptProfile)}
        prohibited_fragments = ("value", "header", "column_id", "position", "dax", "status_name")
        self.assertFalse({name for name in field_names if any(fragment in name for fragment in prohibited_fragments)})
