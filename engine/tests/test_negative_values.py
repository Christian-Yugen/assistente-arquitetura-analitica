import json
import unittest
from datetime import date

from engine.contracts.diagnosis import to_diagnosis_fragment
from engine.profiling.negative_values import NORMALIZATION_BASIS, NegativeValuesProfile, profile_negative_values
from engine.quality.negative_values import NegativeValuesColumnProfile, evaluate_negative_values
from engine.quality.registry import QUALITY_RULE_IMPLEMENTATIONS


class NegativeValuesTests(unittest.TestCase):
    def test_profile_counts_only_finite_physical_numbers_without_retaining_header_or_values(self):
        profile = profile_negative_values(
            "  QUANTIDADE  ",
            [1, 2, 3, 4, 5, 6, 7, 8, 9, -1, True, "-2", None, float("nan"), float("inf"), date(2026, 8, 20)],
        )

        self.assertTrue(profile.header_eligible)
        self.assertEqual(profile.physical_numeric_count, 10)
        self.assertEqual(profile.negative_physical_count, 1)
        self.assertEqual(profile.negative_physical_ratio, 0.1)
        self.assertEqual(profile.basis, NORMALIZATION_BASIS)
        self.assertNotIn("QUANTIDADE", str(profile))

    def test_emits_medium_finding_with_aggregate_evidence_and_human_question(self):
        profile = NegativeValuesProfile(True, 20, 2, 0.1)
        finding = evaluate_negative_values(NegativeValuesColumnProfile("Quantidade Confidencial", profile))[0]

        self.assertEqual(finding["rule_id"], "QLT-NEGATIVE-011")
        self.assertEqual(finding["severity"], "medium")
        self.assertEqual(finding["confidence"], 0.85)
        self.assertTrue(finding["question"])
        self.assertFalse(finding["question"]["blocking"])
        self.assertNotIn("Quantidade Confidencial", str(finding))
        self.assertNotIn("-42", str(finding))

    def test_low_and_high_severity_follow_inclusive_thresholds_and_always_require_validation(self):
        low = evaluate_negative_values(NegativeValuesColumnProfile("Campo", NegativeValuesProfile(True, 20, 1, 0.05)))[0]
        high = evaluate_negative_values(NegativeValuesColumnProfile("Campo", NegativeValuesProfile(True, 10, 3, 0.3)))[0]

        self.assertEqual(low["severity"], "low")
        self.assertTrue(low["question"])
        self.assertEqual(high["severity"], "high")
        self.assertTrue(high["question"])
        self.assertFalse(high["question"]["blocking"])

    def test_excludes_ineligible_headers_small_bases_nonnegative_and_inconsistent_profiles(self):
        cases = [
            NegativeValuesProfile(False, 20, 2, 0.1),
            NegativeValuesProfile(True, 9, 1, 0.11111111),
            NegativeValuesProfile(True, 20, 0, 0.0),
            NegativeValuesProfile(True, 20, 2, 0.2, "unapproved_basis"),
            NegativeValuesProfile(True, 20, 2, 0.2),
        ]
        for profile in cases:
            with self.subTest(profile=profile):
                self.assertEqual(evaluate_negative_values(NegativeValuesColumnProfile("Campo", profile)), [])

    def test_adapts_to_canonical_contract_with_aggregate_evidence_only(self):
        profile = NegativeValuesProfile(True, 10, 3, 0.3)
        fragment = to_diagnosis_fragment(
            evaluate_negative_values(NegativeValuesColumnProfile("Segredo de Quantidade", profile)),
            sheet_id="sheet-1",
            column_id="column-1",
        )

        finding = fragment["findings"][0]
        self.assertEqual(finding["rule_version"], "0.1.0-provisional.1")
        self.assertEqual(finding["affected_entities"][1], {"entity_type": "column", "entity_id": "column-1"})
        serialized = json.dumps(fragment)
        self.assertNotIn("Segredo de Quantidade", serialized)
        self.assertNotIn("raw_value", serialized)
        self.assertIsNotNone(QUALITY_RULE_IMPLEMENTATIONS["QLT-NEGATIVE-011"])


if __name__ == "__main__":
    unittest.main()
