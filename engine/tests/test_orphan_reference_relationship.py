import unittest

from engine.relationships.orphan_reference import (
    OrphanReferenceRelationshipPairProfile,
    classify_orphan_reference_relationship,
)


def valid_profile(**changes):
    values = {
        "source_standard_dimension_candidate": True,
        "target_fact_candidate": True,
        "eligible_dimension_key_count": 1,
        "eligible_fact_reference_count": 1,
        "dimension_key_complete": True,
        "dimension_key_unique": True,
        "fact_reference_complete": True,
        "fact_reference_unique": False,
        "referential_coverage_ratio": 0.75,
        "uncovered_reference_distinct_count": 1,
        "eligible_direction_count": 1,
    }
    values.update(changes)
    return OrphanReferenceRelationshipPairProfile(**values)


class OrphanReferenceRelationshipTests(unittest.TestCase):
    def test_emits_aggregated_orphan_hypothesis_with_blocking_question(self):
        candidate = classify_orphan_reference_relationship(valid_profile())

        self.assertIsNotNone(candidate)
        assert candidate is not None
        self.assertEqual(candidate["relationship_type"], "orphan_reference_candidate")
        self.assertEqual(candidate["confidence"], 0.80)
        self.assertTrue(candidate["question"]["blocking"])
        self.assertEqual(candidate["evidence"]["uncovered_reference_distinct_count"], 1)

    def test_blocks_incompatible_or_insufficient_signals(self):
        for change in (
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
            {"referential_coverage_ratio": 0.0},
            {"referential_coverage_ratio": 1.0},
            {"uncovered_reference_distinct_count": 0},
            {"fact_reference_unique": True},
            {"eligible_direction_count": 2},
        ):
            with self.subTest(change=change):
                self.assertIsNone(classify_orphan_reference_relationship(valid_profile(**change)))

    def test_profile_does_not_define_fields_for_names_values_or_pair_identity(self):
        prohibited = {"sheet_name", "column_name", "header", "value", "pair_id", "source_id", "target_id"}
        self.assertTrue(prohibited.isdisjoint(OrphanReferenceRelationshipPairProfile.__dataclass_fields__))
