from datetime import date
import unittest

from engine.profiling.semantic_date import profile_semantic_date
from engine.semantic.date_generic import SemanticDateColumnProfile, classify_date_generic


class SemanticDateTests(unittest.TestCase):
    def test_recognizes_only_approved_valid_formats_and_physical_dates(self):
        profile = profile_semantic_date([date(2026, 1, 1), "2026-01-02", "03-01-2026", "04/01/2026"] * 3)
        self.assertEqual(profile.non_missing_count, 12)
        self.assertEqual(profile.recognized_date_ratio, 1.0)
        self.assertEqual(profile.physical_date_count, 3)
        self.assertEqual(profile.iso_text_count, 3)
        self.assertEqual(profile.br_hyphen_text_count, 3)
        self.assertEqual(profile.br_slash_text_count, 3)
        self.assertNotIn("2026-01-02", repr(profile))

    def test_rejects_invalid_calendar_and_non_complete_coverage(self):
        profile = profile_semantic_date(["2026-02-30"] + ["2026-02-01"] * 9)
        self.assertEqual(profile.recognized_date_ratio, 0.9)
        self.assertEqual(classify_date_generic(SemanticDateColumnProfile("Data", profile)), [])

    def test_requires_minimum_of_ten_non_missing_values(self):
        profile = profile_semantic_date(["2026-01-01"] * 9)
        self.assertEqual(classify_date_generic(SemanticDateColumnProfile("Data", profile)), [])

    def test_classifies_with_aggregate_evidence_only(self):
        result = classify_date_generic(SemanticDateColumnProfile("Data", profile_semantic_date(["2026-01-01"] * 10)))
        self.assertEqual(result[0]["semantic_type"], "date_generic")
        self.assertEqual(result[0]["confidence"], 0.85)
        self.assertTrue(result[0]["question"]["blocking"] is False)


if __name__ == "__main__":
    unittest.main()
