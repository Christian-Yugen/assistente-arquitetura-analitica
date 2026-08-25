import dataclasses
import unittest

from engine.relationships.conformed_dimension import ConformedDimensionPairProfile, classify_conformed_dimension


class ConformedDimensionTests(unittest.TestCase):
    def valid_profile(self, **overrides: object) -> ConformedDimensionPairProfile:
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
            "connected_fact_count": 2,
        }
        values.update(overrides)
        return ConformedDimensionPairProfile(**values)

    def test_emits_only_a_blocking_review_hypothesis_for_aggregate_fact_connections(self):
        candidate = classify_conformed_dimension(self.valid_profile())

        assert candidate is not None
        self.assertEqual(candidate["rule_id"], "REL-CONFORMED-010")
        self.assertEqual(candidate["relationship_type"], "conformed_dimension_review_candidate")
        self.assertEqual(candidate["confidence"], 0.75)
        self.assertTrue(candidate["question"]["blocking"])
        self.assertNotIn("connected_fact_ids", candidate["evidence"])

    def test_blocks_every_incompatible_pattern_or_governance_signal(self):
        blocking_overrides = (
            {"source_standard_dimension_candidate": False}, {"target_fact_candidate": False},
            {"source_calendar_dimension_candidate": True}, {"source_or_target_undefined_candidate": True},
            {"source_or_target_fact_without_grain_candidate": True}, {"source_or_target_classification_conflict": True},
            {"source_or_target_sensitive": True}, {"source_or_target_has_formula": True}, {"self_reference": True},
            {"has_one_to_one_pattern": True}, {"has_many_to_many_pattern": True}, {"ambiguity_count": 1},
            {"eligible_dimension_key_count": 0}, {"eligible_dimension_key_count": 2},
            {"eligible_fact_reference_count": 0}, {"eligible_fact_reference_count": 2},
            {"dimension_key_complete": False}, {"dimension_key_unique": False}, {"fact_reference_complete": False},
            {"fact_reference_unique": True}, {"referential_coverage_ratio": 0.5}, {"eligible_direction_count": 2},
            {"connected_fact_count": 1},
        )
        for overrides in blocking_overrides:
            with self.subTest(overrides=overrides):
                self.assertIsNone(classify_conformed_dimension(self.valid_profile(**overrides)))

    def test_private_profile_has_no_identifying_or_fact_list_fields(self):
        field_names = {field.name for field in dataclasses.fields(ConformedDimensionPairProfile)}
        prohibited_fragments = ("sheet", "column", "header", "value", "example", "position", "identifier", "fact_ids")
        self.assertFalse({name for name in field_names if any(fragment in name for fragment in prohibited_fragments)})
