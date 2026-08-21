import unittest
from datetime import date

from engine.contracts.diagnosis import to_diagnosis_fragment
from engine.profiling.mixed_types import MixedTypesProfile, profile_mixed_types
from engine.quality.mixed_types import MixedTypesColumnProfile, evaluate_mixed_types
from engine.quality.registry import QUALITY_RULE_IMPLEMENTATIONS


class MixedTypesTests(unittest.TestCase):
    def test_profile_excludes_absences_and_delegates_strict_numeric_text(self):
        profile = profile_mixed_types([1, 2, "3", "texto", "outro", None, "  ", float("nan"), date(2026, 8, 20)])

        self.assertEqual(profile.non_empty_value_count, 6)
        self.assertEqual(profile.numeric_count, 2)
        self.assertEqual(profile.strict_numeric_text_count, 1)
        self.assertEqual(profile.text_non_numeric_count, 2)
        self.assertEqual(profile.temporal_count, 1)

    def test_detects_material_mixture_and_emits_validation_question_without_column_name(self):
        profile = profile_mixed_types([1, 2, 3, 4, 5, 6, 7, 8, "texto", "outro"])
        finding = evaluate_mixed_types(MixedTypesColumnProfile(name="Campo Confidencial", mixed_types=profile))[0]

        self.assertEqual(finding["rule_id"], "QLT-MIXTYPE-005")
        self.assertEqual(finding["severity"], "medium")
        self.assertEqual(finding["confidence"], 0.95)
        self.assertTrue(finding["question"])
        self.assertFalse(finding["question"]["blocking"])
        self.assertNotIn("Campo Confidencial", str(finding))
        self.assertNotIn("texto", str(finding))

    def test_high_severity_for_balanced_incompatible_groups(self):
        profile = profile_mixed_types([True, False, True, date(2026, 1, 1), date(2026, 1, 2), date(2026, 1, 3)])
        finding = evaluate_mixed_types(MixedTypesColumnProfile(name="Campo", mixed_types=profile))[0]

        self.assertEqual(finding["severity"], "high")
        self.assertTrue(finding["question"])
        self.assertTrue(finding["question"]["blocking"])

    def test_excludes_single_outlier_delegated_numeric_text_and_invalid_profile(self):
        cases = [
            profile_mixed_types([1, 2, 3, 4, 5, 6, 7, 8, 9, "outlier"]),
            profile_mixed_types([1, 2, 3, 4, 5, "6", "7", "8", "9", "10"]),
            MixedTypesProfile(non_empty_value_count=5, numeric_count=7),
        ]
        for profile in cases:
            with self.subTest(profile=profile):
                self.assertEqual(evaluate_mixed_types(MixedTypesColumnProfile(name="Campo", mixed_types=profile)), [])

    def test_adapts_finding_to_contract_with_aggregate_evidence_only(self):
        profile = profile_mixed_types([1, 2, 3, 4, 5, 6, 7, 8, "a", "b"])
        fragment = to_diagnosis_fragment(
            evaluate_mixed_types(MixedTypesColumnProfile(name="Segredo", mixed_types=profile)),
            sheet_id="sheet-1",
            column_id="column-1",
        )

        finding = fragment["findings"][0]
        self.assertEqual(finding["rule_version"], "0.1.0-provisional.1")
        self.assertEqual(finding["affected_entities"][1], {"entity_type": "column", "entity_id": "column-1"})
        self.assertNotIn("Segredo", str(fragment))
        self.assertNotIn("\"a\"", str(fragment))
        self.assertIsNotNone(QUALITY_RULE_IMPLEMENTATIONS["QLT-MIXTYPE-005"])


if __name__ == "__main__":
    unittest.main()
