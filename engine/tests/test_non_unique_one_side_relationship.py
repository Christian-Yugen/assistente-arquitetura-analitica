import unittest

from engine.relationships.non_unique_one_side import (
    NonUniqueOneSideRelationshipPairProfile,
    classify_non_unique_one_side_relationship,
)


def valid_profile(**changes):
    values = {
        "source_standard_dimension_candidate": True,
        "target_fact_candidate": True,
        "eligible_dimension_key_count": 1,
        "eligible_fact_reference_count": 1,
        "dimension_key_complete": True,
        "dimension_key_unique": False,
        "dimension_key_duplicate_count": 1,
        "fact_reference_complete": True,
        "referential_coverage_ratio": 1.0,
        "eligible_direction_count": 1,
    }
    values.update(changes)
    return NonUniqueOneSideRelationshipPairProfile(**values)


class NonUniqueOneSideRelationshipTests(unittest.TestCase):
    def test_emits_opaque_alert_and_blocking_question(self):
        candidate = classify_non_unique_one_side_relationship(valid_profile(dimension_key_duplicate_count=3))

        self.assertIsNotNone(candidate)
        assert candidate is not None
        self.assertEqual(candidate["relationship_type"], "one_side_key_non_unique_candidate")
        self.assertEqual(candidate["confidence"], 0.80)
        self.assertEqual(candidate["severity"], "warning")
        self.assertTrue(candidate["question"]["blocking"])
        self.assertEqual(candidate["evidence"]["dimension_key_duplicate_count"], 3)

    def test_blocks_all_disqualifying_or_incomplete_conditions(self):
        for change in (
            {"dimension_key_unique": True},
            {"dimension_key_duplicate_count": 0},
            {"source_or_target_sensitive": True},
            {"source_or_target_has_formula": True},
            {"source_calendar_dimension_candidate": True},
            {"source_or_target_undefined_candidate": True},
            {"source_or_target_fact_without_grain_candidate": True},
            {"source_or_target_classification_conflict": True},
            {"self_reference": True},
            {"has_one_to_one_pattern": True},
            {"has_many_to_many_pattern": True},
            {"ambiguity_count": 1},
            {"referential_coverage_ratio": 0.99},
            {"eligible_direction_count": 2},
            {"dimension_key_complete": False},
            {"fact_reference_complete": False},
        ):
            with self.subTest(change=change):
                self.assertIsNone(classify_non_unique_one_side_relationship(valid_profile(**change)))

    def test_profile_has_no_names_values_or_pair_identifiers(self):
        prohibited = {"sheet_name", "column_name", "header", "value", "pair_id", "source_id", "target_id"}
        self.assertTrue(prohibited.isdisjoint(NonUniqueOneSideRelationshipPairProfile.__dataclass_fields__))
