import dataclasses
import unittest

from engine.relationships.composite_key import (
    CompositeRelationshipKeyPairProfile,
    classify_composite_relationship_key,
)


class CompositeRelationshipKeyTests(unittest.TestCase):
    def valid_profile(self, **overrides: object) -> CompositeRelationshipKeyPairProfile:
        values: dict[str, object] = {
            "source_standard_dimension_candidate": True,
            "target_fact_candidate": True,
            "eligible_composite_key_pair_count": 1,
            "eligible_composite_reference_pair_count": 1,
            "has_eligible_simple_key": False,
            "composite_key_complete": True,
            "composite_key_unique": True,
            "composite_reference_complete": True,
            "composite_reference_unique": False,
            "referential_coverage_ratio": 1.0,
            "eligible_direction_count": 1,
        }
        values.update(overrides)
        return CompositeRelationshipKeyPairProfile(**values)

    def test_emits_only_a_blocking_review_hypothesis_for_one_opaque_composite_pair(self):
        candidate = classify_composite_relationship_key(self.valid_profile())

        assert candidate is not None
        self.assertEqual(candidate["rule_id"], "REL-COMPKEY-009")
        self.assertEqual(candidate["relationship_type"], "composite_relationship_key_review_candidate")
        self.assertEqual(candidate["confidence"], 0.70)
        self.assertEqual(candidate["severity"], "review_required")
        self.assertTrue(candidate["question"]["blocking"])
        self.assertNotIn("source_sheet_id", candidate["evidence"])
        self.assertNotIn("tuple_signature", candidate["evidence"])

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
            {"has_eligible_simple_key": True},
            {"has_one_to_one_pattern": True},
            {"has_many_to_many_pattern": True},
            {"ambiguity_count": 1},
            {"eligible_composite_key_pair_count": 0},
            {"eligible_composite_key_pair_count": 2},
            {"eligible_composite_reference_pair_count": 0},
            {"eligible_composite_reference_pair_count": 2},
            {"composite_key_complete": False},
            {"composite_key_unique": False},
            {"composite_reference_complete": False},
            {"composite_reference_unique": True},
            {"referential_coverage_ratio": 0.5},
            {"eligible_direction_count": 2},
        )

        for overrides in blocking_overrides:
            with self.subTest(overrides=overrides):
                self.assertIsNone(classify_composite_relationship_key(self.valid_profile(**overrides)))

    def test_private_profile_has_no_identifying_or_tuple_fields(self):
        field_names = {field.name for field in dataclasses.fields(CompositeRelationshipKeyPairProfile)}
        prohibited_fragments = ("sheet", "column", "header", "value", "example", "position", "tuple", "signature", "identifier")

        self.assertFalse({name for name in field_names if any(fragment in name for fragment in prohibited_fragments)})
