import unittest

from engine.contracts.diagnosis import to_diagnosis_fragment
from engine.profiling.duplicate_rows import NORMALIZATION_BASIS, DuplicateRowsProfile, profile_duplicate_rows
from engine.quality.duplicates import DuplicateRowsSheetProfile, evaluate_duplicate_rows
from engine.quality.registry import QUALITY_RULE_IMPLEMENTATIONS


class DuplicateRowsTests(unittest.TestCase):
    def test_profiles_only_integral_rows_with_delimited_technical_normalization(self):
        profile = profile_duplicate_rows(
            [
                (" A ", 1),
                ("A", 1),
                ("a", 1),
                ("A", "1"),
                ("A", 1),
            ]
        )

        self.assertEqual(profile.non_empty_row_count, 5)
        self.assertEqual(profile.duplicate_group_count, 1)
        self.assertEqual(profile.duplicate_row_count, 3)
        self.assertEqual(profile.duplicate_row_ratio, 0.6)
        self.assertEqual(profile.largest_duplicate_group, 3)
        self.assertEqual(profile.normalization_basis, NORMALIZATION_BASIS)

    def test_ignores_fully_empty_rows_and_preserves_non_empty_null_positions(self):
        profile = profile_duplicate_rows(
            [
                (None, ""),
                ("", None),
                ("A", None),
                ("A", None),
                ("A", ""),
            ]
        )

        self.assertEqual(profile.non_empty_row_count, 3)
        self.assertEqual(profile.duplicate_group_count, 1)
        self.assertEqual(profile.duplicate_row_count, 2)
        self.assertEqual(profile.duplicate_row_ratio, round(2 / 3, 8))

    def test_emits_high_finding_and_blocking_question_without_row_content(self):
        profile = profile_duplicate_rows([("sigiloso", 7), ("sigiloso", 7), ("sigiloso", 7), ("outro", 8)])
        findings = evaluate_duplicate_rows(DuplicateRowsSheetProfile(name="Aba 1", duplicates=profile))

        self.assertEqual(len(findings), 1)
        finding = findings[0]
        self.assertEqual(finding["rule_id"], "QLT-DUP-002")
        self.assertEqual(finding["severity"], "high")
        self.assertEqual(finding["confidence"], 0.92)
        self.assertTrue(finding["question"])
        self.assertIn("Investigar", finding["recommendation"])
        self.assertNotIn("sigiloso", str(finding))
        self.assertNotIn("outro", str(finding))

    def test_does_not_emit_finding_without_repeated_integral_signature(self):
        profile = profile_duplicate_rows([("A", 1), ("a", 1), ("A", "1"), ("A", 2)])

        self.assertEqual(evaluate_duplicate_rows(DuplicateRowsSheetProfile(name="Aba 1", duplicates=profile)), [])

    def test_applies_confidence_penalty_for_minimal_evidence(self):
        profile = profile_duplicate_rows([("A", 1), ("A", 1)])
        finding = evaluate_duplicate_rows(DuplicateRowsSheetProfile(name="Aba 1", duplicates=profile))[0]

        self.assertEqual(finding["confidence"], 0.78)

    def test_adapts_the_high_finding_to_the_canonical_contract(self):
        profile = profile_duplicate_rows([("A", 1), ("A", 1), ("A", 1), ("B", 2)])
        findings = evaluate_duplicate_rows(DuplicateRowsSheetProfile(name="Aba 1", duplicates=profile))
        fragment = to_diagnosis_fragment(findings, sheet_id="sheet-1", column_id="column-1")

        self.assertEqual(fragment["findings"][0]["rule_id"], "QLT-DUP-002")
        self.assertEqual(fragment["findings"][0]["rule_version"], "0.1.0-reconstructed.1")
        self.assertEqual(fragment["findings"][0]["affected_entities"][0], {"entity_type": "sheet", "entity_id": "sheet-1"})
        self.assertEqual(len(fragment["questions"]), 1)

    def test_profile_contains_only_aggregate_metrics_and_rule_is_registered_after_calibration_gate(self):
        profile = profile_duplicate_rows([("segredo", 1), ("segredo", 1)])

        self.assertNotIn("segredo", str(profile.__dict__))
        self.assertIsNotNone(QUALITY_RULE_IMPLEMENTATIONS["QLT-DUP-002"])


if __name__ == "__main__":
    unittest.main()
