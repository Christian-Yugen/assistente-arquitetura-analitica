import unittest

from engine.relationships.one_to_many import OneToManyRelationshipPairProfile, classify_one_to_many_relationship


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
        "referential_coverage_ratio": 1.0,
        "eligible_direction_count": 1,
    }
    values.update(changes)
    return OneToManyRelationshipPairProfile(**values)


class OneToManyRelationshipTests(unittest.TestCase):
    def test_emits_aggregated_one_to_many_hypothesis_with_blocking_question(self):
        candidate = classify_one_to_many_relationship(valid_profile())

        self.assertIsNotNone(candidate)
        assert candidate is not None
        self.assertEqual(candidate["relationship_type"], "one_to_many_relationship_candidate")
        self.assertEqual(candidate["confidence"], 0.85)
        self.assertTrue(candidate["question"]["blocking"])
        self.assertEqual(
            set(candidate["evidence"]),
            {
                "source_standard_dimension_candidate",
                "target_fact_candidate",
                "eligible_dimension_key_count",
                "eligible_fact_reference_count",
                "dimension_key_complete",
                "dimension_key_unique",
                "fact_reference_complete",
                "fact_reference_unique",
                "referential_coverage_ratio",
                "eligible_direction_count",
            },
        )

    def test_blocks_every_disqualifying_relationship_signal(self):
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
            {"referential_coverage_ratio": 0.99},
            {"fact_reference_unique": True},
            {"eligible_direction_count": 2},
        ):
            with self.subTest(change=change):
                self.assertIsNone(classify_one_to_many_relationship(valid_profile(**change)))

    def test_profile_does_not_define_fields_for_names_values_or_pair_identity(self):
        prohibited = {"sheet_name", "column_name", "header", "value", "pair_id", "source_id", "target_id"}
        self.assertTrue(prohibited.isdisjoint(OneToManyRelationshipPairProfile.__dataclass_fields__))
