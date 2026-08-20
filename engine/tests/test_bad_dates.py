import unittest
from datetime import date

from engine.contracts.diagnosis import to_diagnosis_fragment
from engine.profiling.bad_dates import BadDateProfile, profile_bad_dates
from engine.quality.bad_dates import BadDateColumnProfile, evaluate_bad_dates
from engine.quality.registry import QUALITY_RULE_IMPLEMENTATIONS


class BadDatesTests(unittest.TestCase):
    def test_profile_accepts_three_strict_grammars_and_excludes_non_candidates(self):
        profile = profile_bad_dates([
            "2026-02-28", "29-02-2024", "31/12/2026",
            "2026-02-30", "31-04-2026", "31/04/2026",
            None, "  ", float("nan"), date(2026, 8, 20), 45292, "2026/02/30",
        ])

        self.assertEqual(profile.strict_date_candidate_count, 6)
        self.assertEqual(profile.invalid_strict_date_count, 3)
        self.assertEqual(profile.invalid_strict_date_ratio, 0.5)
        self.assertNotIn("2026-02-30", str(profile))

    def test_emits_medium_finding_without_column_name_or_raw_value(self):
        profile = BadDateProfile(strict_date_candidate_count=20, invalid_strict_date_count=2, invalid_strict_date_ratio=0.1)
        finding = evaluate_bad_dates(BadDateColumnProfile(name="Data do Cliente", bad_dates=profile))[0]

        self.assertEqual(finding["rule_id"], "QLT-BADDATE-006")
        self.assertEqual(finding["severity"], "medium")
        self.assertEqual(finding["confidence"], 0.98)
        self.assertTrue(finding["question"])
        self.assertFalse(finding["question"]["blocking"])
        self.assertNotIn("Data do Cliente", str(finding))
        self.assertNotIn("31/04/2026", str(finding))

    def test_low_and_high_severity_follow_inclusive_thresholds(self):
        low = evaluate_bad_dates(BadDateColumnProfile("Campo", BadDateProfile(20, 1, 0.05)))[0]
        high = evaluate_bad_dates(BadDateColumnProfile("Campo", BadDateProfile(8, 2, 0.25)))[0]

        self.assertEqual(low["severity"], "low")
        self.assertIsNone(low["question"])
        self.assertEqual(high["severity"], "high")
        self.assertTrue(high["question"])
        self.assertTrue(high["question"]["blocking"])

    def test_excludes_valid_only_empty_and_inconsistent_profiles(self):
        cases = [
            BadDateProfile(strict_date_candidate_count=12, invalid_strict_date_count=0, invalid_strict_date_ratio=0.0),
            BadDateProfile(),
            BadDateProfile(strict_date_candidate_count=10, invalid_strict_date_count=2, invalid_strict_date_ratio=0.1),
        ]
        for profile in cases:
            with self.subTest(profile=profile):
                self.assertEqual(evaluate_bad_dates(BadDateColumnProfile("Campo", profile)), [])

    def test_adapts_to_canonical_contract_with_aggregate_evidence_only(self):
        profile = BadDateProfile(strict_date_candidate_count=10, invalid_strict_date_count=3, invalid_strict_date_ratio=0.3)
        fragment = to_diagnosis_fragment(
            evaluate_bad_dates(BadDateColumnProfile("Segredo de Data", profile)),
            sheet_id="sheet-1",
            column_id="column-1",
        )

        finding = fragment["findings"][0]
        self.assertEqual(finding["rule_version"], "0.1.0-provisional.1")
        self.assertEqual(finding["affected_entities"][1], {"entity_type": "column", "entity_id": "column-1"})
        self.assertNotIn("Segredo de Data", str(fragment))
        self.assertNotIn("31/04/2026", str(fragment))
        self.assertIsNotNone(QUALITY_RULE_IMPLEMENTATIONS["QLT-BADDATE-006"])


if __name__ == "__main__":
    unittest.main()
