import dataclasses
import unittest

from engine.relationships.direct_fact import (
    DirectFactRelationshipPairProfile,
    classify_direct_fact_relationship,
)


class DirectFactRelationshipTests(unittest.TestCase):
    def valid_profile(self, **overrides: object) -> DirectFactRelationshipPairProfile:
        values: dict[str, object] = {
            "source_fact_candidate": True,
            "target_fact_candidate": True,
            "eligible_source_key_count": 1,
            "eligible_target_reference_count": 1,
            "source_key_complete": True,
            "source_key_unique": True,
            "target_reference_complete": True,
            "target_reference_unique": False,
            "referential_coverage_ratio": 1.0,
            "eligible_direction_count": 1,
        }
        values.update(overrides)
        return DirectFactRelationshipPairProfile(**values)

    def test_emits_only_a_blocking_review_hypothesis_for_an_eligible_opaque_pair(self):
        candidate = classify_direct_fact_relationship(self.valid_profile())

        assert candidate is not None
        self.assertEqual(candidate["rule_id"], "REL-FACTFACT-006")
        self.assertEqual(candidate["relationship_type"], "direct_fact_to_fact_relationship_review_candidate")
        self.assertEqual(candidate["confidence"], 0.65)
        self.assertEqual(candidate["severity"], "review_required")
        self.assertTrue(candidate["question"]["blocking"])
        self.assertNotIn("source_sheet_id", candidate["evidence"])
        self.assertNotIn("target_sheet_id", candidate["evidence"])

    def test_blocks_every_incompatible_pattern_or_governance_signal(self):
        blocking_overrides = (
            {"source_fact_candidate": False},
            {"target_fact_candidate": False},
            {"source_or_target_dimension_candidate": True},
            {"source_or_target_undefined_candidate": True},
            {"source_or_target_fact_without_grain_candidate": True},
            {"source_or_target_classification_conflict": True},
            {"source_or_target_sensitive": True},
            {"source_or_target_has_formula": True},
            {"self_reference": True},
            {"has_one_to_one_pattern": True},
            {"has_many_to_many_pattern": True},
            {"ambiguity_count": 1},
            {"eligible_source_key_count": 2},
            {"eligible_target_reference_count": 2},
            {"source_key_complete": False},
            {"source_key_unique": False},
            {"target_reference_complete": False},
            {"target_reference_unique": True},
            {"referential_coverage_ratio": 0.99},
            {"eligible_direction_count": 2},
        )

        for overrides in blocking_overrides:
            with self.subTest(overrides=overrides):
                self.assertIsNone(classify_direct_fact_relationship(self.valid_profile(**overrides)))

    def test_private_profile_has_no_identifying_fields(self):
        field_names = {field.name for field in dataclasses.fields(DirectFactRelationshipPairProfile)}
        prohibited_fragments = ("sheet", "column", "header", "value", "example", "position", "pair", "identifier")

        self.assertFalse({name for name in field_names if any(fragment in name for fragment in prohibited_fragments)})
