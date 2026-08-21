import json
import unittest

from engine.contracts.diagnosis import to_diagnosis_fragment
from engine.profiling.identifier_completeness import NORMALIZATION_BASIS, IdentifierCompletenessProfile, profile_identifier_completeness
from engine.quality.identifier_completeness import IdentifierCompletenessColumnProfile, evaluate_identifier_completeness
from engine.quality.registry import QUALITY_RULE_IMPLEMENTATIONS


class IdentifierCompletenessTests(unittest.TestCase):
    def test_profile_is_aggregate_and_discards_header_and_identifier_values(self):
        profile = profile_identifier_completeness("Código", ["A-001", "A-001", None, "B-002", "C-003", "D-004", "E-005", "F-006", "G-007", "H-008"])

        self.assertTrue(profile.header_eligible)
        self.assertEqual(profile.observed_cell_count, 10)
        self.assertEqual(profile.missing_cell_count, 1)
        self.assertEqual(profile.duplicate_group_count, 1)
        self.assertEqual(profile.duplicate_occurrence_count, 2)
        serialized = json.dumps(profile.__dict__, ensure_ascii=False)
        self.assertNotIn("Código", serialized)
        self.assertNotIn("A-001", serialized)
        self.assertNotIn("B-002", serialized)

    def test_finding_uses_only_aggregate_evidence_and_requires_human_confirmation(self):
        profile = IdentifierCompletenessColumnProfile("Código", IdentifierCompletenessProfile(True, 20, 1, 19, 1, 2, 0.05, 0.1))
        findings = evaluate_identifier_completeness(profile)

        self.assertEqual(len(findings), 1)
        self.assertEqual(findings[0]["severity"], "medium")
        self.assertEqual(findings[0]["confidence"], 0.85)
        self.assertIsNotNone(findings[0]["question"])
        self.assertFalse(findings[0]["question"]["blocking"])
        evidence_serialized = json.dumps(findings[0]["evidence"], ensure_ascii=False)
        self.assertNotIn("Código", evidence_serialized)
        self.assertNotIn("A-001", evidence_serialized)

    def test_excludes_noneligible_headers_small_bases_format_inference_and_inconsistent_profiles(self):
        self.assertEqual(evaluate_identifier_completeness(IdentifierCompletenessColumnProfile("Valor", profile_identifier_completeness("Valor", ["x"] * 20))), [])
        self.assertEqual(evaluate_identifier_completeness(IdentifierCompletenessColumnProfile("ID", profile_identifier_completeness("ID", ["1"] * 9))), [])
        self.assertEqual(evaluate_identifier_completeness(IdentifierCompletenessColumnProfile("CPF", profile_identifier_completeness("CPF", [f"invalid-{index}" for index in range(10)]))), [])
        self.assertEqual(evaluate_identifier_completeness(IdentifierCompletenessColumnProfile("ID", IdentifierCompletenessProfile(True, 10, 0, 10, 1, 2, 0.0, 0.1, "other"))), [])

    def test_contract_and_registry_keep_the_rule_private_and_registered(self):
        profile = IdentifierCompletenessColumnProfile("ID", IdentifierCompletenessProfile(True, 10, 1, 9, 0, 0, 0.1, 0.0))
        fragment = to_diagnosis_fragment(evaluate_identifier_completeness(profile), sheet_id="sheet-x", column_id="column-y")

        self.assertIn("QLT-IDMISS-015", QUALITY_RULE_IMPLEMENTATIONS)
        self.assertEqual(fragment["findings"][0]["rule_id"], "QLT-IDMISS-015")
        self.assertEqual(fragment["findings"][0]["rule_version"], "0.1.0-provisional.1")
        self.assertEqual(profile.identifiers.basis, NORMALIZATION_BASIS)
