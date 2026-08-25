import dataclasses
import unittest

from engine.relationships.bidirectional_filter import (
    BidirectionalFilterReviewPairProfile,
    classify_bidirectional_filter_review,
)


class BidirectionalFilterReviewTests(unittest.TestCase):
    def valid_profile(self, **overrides: object) -> BidirectionalFilterReviewPairProfile:
        values: dict[str, object] = {
            "source_standard_dimension_candidate": True,
            "target_fact_candidate": True,
            "eligible_dimension_key_count": 1,
            "eligible_fact_reference_count": 1,
            "dimension_key_complete": True,
            "dimension_key_unique": True,
            "fact_reference_complete": True,
            "fact_reference_unique": False,
            "referential_coverage_ratio": 1.0,
            "eligible_direction_count": 1,
        }
        values.update(overrides)
        return BidirectionalFilterReviewPairProfile(**values)

    def test_emits_only_a_blocking_review_hypothesis_for_an_eligible_opaque_pair(self):
        candidate = classify_bidirectional_filter_review(self.valid_profile())

        assert candidate is not None
        self.assertEqual(candidate["rule_id"], "REL-BIDIR-008")
        self.assertEqual(candidate["relationship_type"], "bidirectional_filter_review_candidate")
        self.assertEqual(candidate["confidence"], 0.70)
        self.assertEqual(candidate["severity"], "review_required")
        self.assertTrue(candidate["question"]["blocking"])
        self.assertNotIn("source_sheet_id", candidate["evidence"])
        self.assertNotIn("target_sheet_id", candidate["evidence"])

    def test_blocks_every_incompatible_pattern_or_governance_signal(self):
        blocking_overrides = (
            {"source_standard_dimension_candidate": False},
            {"target_fact_candidate": False},
            {"source_calendar_dimension_candidate": True},
            {"source_or_target_undefined_candidate": True},
            {"source_or_target_fact_without_grain_candidate": True},
            {"source_or_target_classification_conflict": True},
            {"source_or_target_sensitive": True},
            {"source_or_target_has_formula": True},
            {"self_reference": True},
            {"has_one_to_one_pattern": True},
            {"has_many_to_many_pattern": True},
            {"ambiguity_count": 1},
            {"eligible_dimension_key_count": 2},
            {"eligible_fact_reference_count": 2},
            {"dimension_key_complete": False},
            {"dimension_key_unique": False},
            {"fact_reference_complete": False},
            {"fact_reference_unique": True},
            {"referential_coverage_ratio": 0.99},
            {"eligible_direction_count": 2},
        )

        for overrides in blocking_overrides:
            with self.subTest(overrides=overrides):
                self.assertIsNone(classify_bidirectional_filter_review(self.valid_profile(**overrides)))

    def test_private_profile_has_no_identifying_fields(self):
        field_names = {field.name for field in dataclasses.fields(BidirectionalFilterReviewPairProfile)}
        prohibited_fragments = ("sheet", "column", "header", "value", "example", "position", "pair", "identifier")

        self.assertFalse({name for name in field_names if any(fragment in name for fragment in prohibited_fragments)})
