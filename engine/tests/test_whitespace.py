import unittest

from engine.contracts.diagnosis import to_diagnosis_fragment
from engine.profiling.whitespace import WhitespaceProfile, profile_whitespace
from engine.quality.registry import QUALITY_RULE_IMPLEMENTATIONS
from engine.quality.whitespace import WhitespaceColumnProfile, evaluate_whitespace


class WhitespaceTests(unittest.TestCase):
    def test_profile_counts_only_approved_text_signals_and_excludes_missing_values(self):
        profile = profile_whitespace([
            " alfa", "beta\u00a0", "gam\u200ba", "delta",
            None, "  ", "\t", 42, float("nan"),
        ])

        self.assertEqual(profile.non_blank_text_count, 4)
        self.assertEqual(profile.leading_or_trailing_space_count, 2)
        self.assertEqual(profile.hidden_character_count, 1)
        self.assertEqual(profile.affected_text_count, 3)
        self.assertEqual(profile.affected_text_ratio, 0.75)
        self.assertNotIn("gam", str(profile))

    def test_emits_medium_finding_without_column_name_or_raw_text(self):
        profile = WhitespaceProfile(20, 2, 0, 2, 0.1)
        finding = evaluate_whitespace(WhitespaceColumnProfile(name="Identificador confidencial", whitespace=profile))[0]

        self.assertEqual(finding["rule_id"], "QLT-WHITESPACE-009")
        self.assertEqual(finding["severity"], "medium")
        self.assertEqual(finding["confidence"], 0.95)
        self.assertTrue(finding["question"])
        self.assertFalse(finding["question"]["blocking"])
        self.assertNotIn("Identificador confidencial", str(finding))
        self.assertNotIn("gam\u200ba", str(finding))

    def test_low_and_high_severity_follow_inclusive_thresholds(self):
        low = evaluate_whitespace(WhitespaceColumnProfile("Campo", WhitespaceProfile(20, 1, 0, 1, 0.05)))[0]
        high = evaluate_whitespace(WhitespaceColumnProfile("Campo", WhitespaceProfile(8, 1, 2, 2, 0.25)))[0]

        self.assertEqual(low["severity"], "low")
        self.assertIsNone(low["question"])
        self.assertEqual(high["severity"], "high")
        self.assertTrue(high["question"])
        self.assertTrue(high["question"]["blocking"])

    def test_excludes_unaffected_empty_and_inconsistent_profiles(self):
        cases = [
            WhitespaceProfile(12, 0, 0, 0, 0.0),
            WhitespaceProfile(),
            WhitespaceProfile(10, 1, 1, 2, 0.1),
        ]
        for profile in cases:
            with self.subTest(profile=profile):
                self.assertEqual(evaluate_whitespace(WhitespaceColumnProfile("Campo", profile)), [])

    def test_adapts_to_canonical_contract_with_aggregate_evidence_only(self):
        profile = WhitespaceProfile(10, 2, 2, 3, 0.3)
        fragment = to_diagnosis_fragment(
            evaluate_whitespace(WhitespaceColumnProfile("Segredo de Texto", profile)),
            sheet_id="sheet-1",
            column_id="column-1",
        )

        finding = fragment["findings"][0]
        self.assertEqual(finding["rule_version"], "0.1.0-provisional.1")
        self.assertEqual(finding["affected_entities"][1], {"entity_type": "column", "entity_id": "column-1"})
        self.assertNotIn("Segredo de Texto", str(fragment))
        self.assertNotIn("gam\u200ba", str(fragment))
        self.assertIsNotNone(QUALITY_RULE_IMPLEMENTATIONS["QLT-WHITESPACE-009"])


if __name__ == "__main__":
    unittest.main()
