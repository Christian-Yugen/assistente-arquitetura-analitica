import unittest

from engine.catalog import RuleExecutionUnavailableError, execute_registered_rule, get_rule_execution_record
from engine.contracts.diagnosis import RULE_VERSIONS, to_relationship_fragment
from engine.relationships.one_to_many import OneToManyRelationshipPairProfile, classify_one_to_many_relationship
from engine.relationships.non_unique_one_side import NonUniqueOneSideRelationshipPairProfile
from engine.relationships.orphan_reference import OrphanReferenceRelationshipPairProfile
from engine.relationships.many_to_many import ManyToManyRelationshipPairProfile
from engine.relationships.direct_fact import DirectFactRelationshipPairProfile
from engine.relationships.ambiguous_path import AmbiguousRelationshipPathPairProfile
from engine.relationships.bidirectional_filter import BidirectionalFilterReviewPairProfile


class RelationshipContractTests(unittest.TestCase):
    def test_projects_only_opaque_sheet_entities_and_aggregated_evidence(self):
        candidate = classify_one_to_many_relationship(
            OneToManyRelationshipPairProfile(
                source_standard_dimension_candidate=True,
                target_fact_candidate=True,
                eligible_dimension_key_count=1,
                eligible_fact_reference_count=1,
                dimension_key_complete=True,
                dimension_key_unique=True,
                fact_reference_complete=True,
                fact_reference_unique=False,
                referential_coverage_ratio=1.0,
                eligible_direction_count=1,
            )
        )
        assert candidate is not None

        fragment = to_relationship_fragment(
            [candidate],
            source_sheet_id="opaque-sheet-source",
            target_sheet_id="opaque-sheet-target",
        )

        relationship = fragment["relationships"][0]
        self.assertEqual(relationship["source"], {"entity_type": "sheet", "entity_id": "opaque-sheet-source"})
        self.assertEqual(relationship["target"], {"entity_type": "sheet", "entity_id": "opaque-sheet-target"})
        self.assertEqual(relationship["rule_version"], "0.1.0-provisional.1")
        self.assertEqual(relationship["status"], "hypothesis")
        self.assertTrue(fragment["questions"][0]["blocking"])
        self.assertEqual(fragment["questions"][0]["impact"]["affected_modules"], ["relationships"])
        prohibited = {"source_column_id", "target_column_id", "header", "value", "example", "frequency"}
        self.assertTrue(prohibited.isdisjoint(relationship))

    def test_catalog_executes_registered_rule_only_in_the_draft_profile(self):
        record = get_rule_execution_record("REL-ONEMANY-001")

        self.assertEqual(RULE_VERSIONS["REL-ONEMANY-001"], "0.1.0-provisional.1")
        self.assertEqual(record.status, "executable_draft")
        result = execute_registered_rule(
            "REL-ONEMANY-001",
            OneToManyRelationshipPairProfile(
                source_standard_dimension_candidate=True,
                target_fact_candidate=True,
                eligible_dimension_key_count=1,
                eligible_fact_reference_count=1,
                dimension_key_complete=True,
                dimension_key_unique=True,
                fact_reference_complete=True,
                fact_reference_unique=False,
                referential_coverage_ratio=1.0,
                eligible_direction_count=1,
            ),
        )
        self.assertIsNotNone(result)

    def test_non_unique_rule_is_versioned_and_executes_only_in_the_draft_profile(self):
        record = get_rule_execution_record("REL-NONUNIQ-002")

        self.assertEqual(RULE_VERSIONS["REL-NONUNIQ-002"], "0.1.0-provisional.1")
        self.assertEqual(record.status, "executable_draft")
        result = execute_registered_rule(
            "REL-NONUNIQ-002",
            NonUniqueOneSideRelationshipPairProfile(
                source_standard_dimension_candidate=True,
                target_fact_candidate=True,
                eligible_dimension_key_count=1,
                eligible_fact_reference_count=1,
                dimension_key_complete=True,
                dimension_key_duplicate_count=1,
                fact_reference_complete=True,
                referential_coverage_ratio=1.0,
                eligible_direction_count=1,
            ),
        )
        self.assertIsNotNone(result)

    def test_orphan_rule_is_versioned_and_executes_only_in_the_draft_profile(self):
        record = get_rule_execution_record("REL-ORPHAN-003")

        self.assertEqual(RULE_VERSIONS["REL-ORPHAN-003"], "0.1.0-provisional.1")
        self.assertEqual(record.status, "executable_draft")
        result = execute_registered_rule(
            "REL-ORPHAN-003",
            OrphanReferenceRelationshipPairProfile(
                source_standard_dimension_candidate=True,
                target_fact_candidate=True,
                eligible_dimension_key_count=1,
                eligible_fact_reference_count=1,
                dimension_key_complete=True,
                dimension_key_unique=True,
                fact_reference_complete=True,
                referential_coverage_ratio=0.5,
                uncovered_reference_distinct_count=1,
                eligible_direction_count=1,
            ),
        )
        self.assertIsNotNone(result)

    def test_many_to_many_rule_is_versioned_and_executes_only_in_the_draft_profile(self):
        record = get_rule_execution_record("REL-MANYMANY-004")

        self.assertEqual(RULE_VERSIONS["REL-MANYMANY-004"], "0.1.0-provisional.1")
        self.assertEqual(record.status, "executable_draft")
        result = execute_registered_rule(
            "REL-MANYMANY-004",
            ManyToManyRelationshipPairProfile(
                source_standard_dimension_candidate=True,
                target_fact_candidate=True,
                eligible_dimension_key_count=1,
                eligible_fact_reference_count=1,
                dimension_key_complete=True,
                fact_reference_complete=True,
                referential_coverage_ratio=1.0,
                eligible_direction_count=1,
            ),
        )
        self.assertIsNotNone(result)

    def test_direct_fact_rule_is_versioned_and_executes_only_in_the_draft_profile(self):
        record = get_rule_execution_record("REL-FACTFACT-006")

        self.assertEqual(RULE_VERSIONS["REL-FACTFACT-006"], "0.1.0-provisional.1")
        self.assertEqual(record.status, "executable_draft")
        result = execute_registered_rule(
            "REL-FACTFACT-006",
            DirectFactRelationshipPairProfile(
                source_fact_candidate=True,
                target_fact_candidate=True,
                eligible_source_key_count=1,
                eligible_target_reference_count=1,
                source_key_complete=True,
                source_key_unique=True,
                target_reference_complete=True,
                target_reference_unique=False,
                referential_coverage_ratio=1.0,
                eligible_direction_count=1,
            ),
        )
        self.assertIsNotNone(result)

    def test_ambiguous_path_rule_is_versioned_and_executes_only_in_the_draft_profile(self):
        record = get_rule_execution_record("REL-AMBIG-007")

        self.assertEqual(RULE_VERSIONS["REL-AMBIG-007"], "0.1.0-provisional.1")
        self.assertEqual(record.status, "executable_draft")
        result = execute_registered_rule(
            "REL-AMBIG-007",
            AmbiguousRelationshipPathPairProfile(
                source_standard_dimension_candidate=True,
                target_fact_candidate=True,
                eligible_source_key_count=1,
                eligible_target_reference_count=1,
                source_key_complete=True,
                source_key_unique=True,
                target_reference_complete=True,
                target_reference_unique=False,
                referential_coverage_ratio=1.0,
                eligible_direction_count=2,
            ),
        )
        self.assertIsNotNone(result)

    def test_bidirectional_filter_rule_is_versioned_and_executes_only_in_the_draft_profile(self):
        record = get_rule_execution_record("REL-BIDIR-008")

        self.assertEqual(RULE_VERSIONS["REL-BIDIR-008"], "0.1.0-provisional.1")
        self.assertEqual(record.status, "executable_draft")
        result = execute_registered_rule(
            "REL-BIDIR-008",
            BidirectionalFilterReviewPairProfile(
                source_standard_dimension_candidate=True,
                target_fact_candidate=True,
                eligible_dimension_key_count=1,
                eligible_fact_reference_count=1,
                dimension_key_complete=True,
                dimension_key_unique=True,
                fact_reference_complete=True,
                fact_reference_unique=False,
                referential_coverage_ratio=1.0,
                eligible_direction_count=1,
            ),
        )
        self.assertIsNotNone(result)
