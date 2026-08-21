import unittest
from dataclasses import asdict, dataclass

from engine.profiling.headers import HEADERS_BASIS, HeadersProfile, profile_headers
from engine.quality.headers import HeadersSheetProfile, evaluate_headers


@dataclass(frozen=True)
class Cell:
    value: object
    data_type: str = "s"


class HeadersTests(unittest.TestCase):
    def test_profiles_absence_duplicates_and_multilevel_without_retaining_text_or_ranges(self):
        profile = profile_headers(
            (Cell("Código"), Cell(" codigo "), Cell(""), Cell("Grupo")),
            (Cell("Norte"), Cell("Sul"), Cell(None), Cell(None)),
            ((1, 1, 2, 1),),
        )
        self.assertEqual(profile.header_column_count, 4)
        self.assertEqual(profile.missing_header_count, 1)
        self.assertEqual(profile.duplicate_normalized_group_count, 1)
        self.assertEqual(profile.duplicate_header_count, 2)
        self.assertEqual(profile.multilevel_candidate_count, 1)
        serialized = str(asdict(profile))
        self.assertNotIn("Código", serialized)
        self.assertNotIn("Norte", serialized)

    def test_evaluator_emits_high_priority_question_for_multilevel_candidate(self):
        findings = evaluate_headers(HeadersSheetProfile("Aba privada", HeadersProfile(4, 0, 0, 0, 1)))
        self.assertEqual(findings[0]["rule_id"], "QLT-HEADERS-014")
        self.assertEqual(findings[0]["severity"], "high")
        self.assertTrue(findings[0]["question"]["blocking"])
        self.assertNotIn("Aba privada", str(findings))

    def test_excludes_valid_headers_and_inconsistent_profiles(self):
        self.assertEqual(evaluate_headers(HeadersSheetProfile("Aba", HeadersProfile(3, 0, 0, 0, 0))), [])
        self.assertEqual(evaluate_headers(HeadersSheetProfile("Aba", HeadersProfile(3, 0, 1, 1, 0))), [])
        self.assertEqual(evaluate_headers(HeadersSheetProfile("Aba", HeadersProfile(3, 1, 0, 0, 0, "other"))), [])

    def test_formula_in_header_is_counted_as_missing_without_exposing_expression(self):
        profile = profile_headers((Cell("=SENSITIVE()", "f"), Cell("Campo")), None, ())
        self.assertEqual(profile.missing_header_count, 1)
        self.assertEqual(profile.basis, HEADERS_BASIS)
        self.assertNotIn("SENSITIVE", str(asdict(profile)))
