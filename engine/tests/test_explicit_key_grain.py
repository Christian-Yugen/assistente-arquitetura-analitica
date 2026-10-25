from __future__ import annotations

import dataclasses
import unittest

from engine.granularity.explicit_key import ExplicitKeyColumnProfile, ExplicitKeySheetProfile, classify_explicit_key
from engine.profiling.explicit_key_grain import profile_explicit_key_header


def candidate(
    header: str = "ID",
    *,
    identifier_signal: bool = True,
    sensitive_header: bool = False,
    description_header: bool = False,
    recognized_date_count: int = 0,
    physical_type: str = "numeric",
    non_missing_count: int = 20,
    distinct_non_missing_count: int = 20,
    formula_count: int = 0,
) -> ExplicitKeyColumnProfile:
    return ExplicitKeyColumnProfile(
        header=profile_explicit_key_header(header),
        identifier_signal=identifier_signal,
        sensitive_header=sensitive_header,
        description_header=description_header,
        recognized_date_count=recognized_date_count,
        physical_type=physical_type,
        non_missing_count=non_missing_count,
        distinct_non_missing_count=distinct_non_missing_count,
        formula_count=formula_count,
    )


class ExplicitKeyGrainTests(unittest.TestCase):
    def test_detects_single_complete_unique_explicit_key(self) -> None:
        results = classify_explicit_key(ExplicitKeySheetProfile(20, (candidate(),)))
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["grain_type"], "explicit_key_candidate")
        self.assertEqual(results[0]["confidence"], 0.85)
        self.assertTrue(results[0]["question"]["blocking"])

    def test_accepts_the_closed_header_vocabulary(self) -> None:
        for header in ("ID", "Chave", "Key"):
            with self.subTest(header=header):
                self.assertEqual(len(classify_explicit_key(ExplicitKeySheetProfile(20, (candidate(header),)))), 1)

    def test_rejects_insufficient_base_incomplete_duplicate_formula_or_ambiguity(self) -> None:
        cases = (
            ExplicitKeySheetProfile(19, (candidate(non_missing_count=19, distinct_non_missing_count=19),)),
            ExplicitKeySheetProfile(20, (candidate(non_missing_count=19, distinct_non_missing_count=19),)),
            ExplicitKeySheetProfile(20, (candidate(distinct_non_missing_count=19),)),
            ExplicitKeySheetProfile(20, (candidate(formula_count=1),)),
            ExplicitKeySheetProfile(20, (candidate("ID"), candidate("Chave"))),
        )
        for profile in cases:
            with self.subTest(profile=profile):
                self.assertEqual(classify_explicit_key(profile), [])

    def test_accepts_a_semantic_identifier_signal_with_a_compound_header(self) -> None:
        self.assertEqual(len(classify_explicit_key(ExplicitKeySheetProfile(20, (candidate("Código do registro"),)))), 1)

    def test_rejects_open_header_and_excluded_semantics(self) -> None:
        cases = (
            candidate("Referência", identifier_signal=False),
            candidate(sensitive_header=True),
            candidate(description_header=True),
            candidate(recognized_date_count=20, physical_type="date"),
        )
        for column in cases:
            with self.subTest(column=column):
                self.assertEqual(classify_explicit_key(ExplicitKeySheetProfile(20, (column,))), [])

    def test_profiles_do_not_retain_headers_or_values(self) -> None:
        profile = ExplicitKeySheetProfile(20, (candidate("Chave"),))
        serialized = str(dataclasses.asdict(profile))
        self.assertNotIn("Chave", serialized)
        self.assertNotIn("valor-secreto", serialized)
