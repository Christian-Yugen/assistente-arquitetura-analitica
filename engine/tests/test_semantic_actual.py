import unittest
from datetime import date

from engine.profiling.formula_consistency import FormulaConsistencyProfile
from engine.profiling.numeric_text import profile_numeric_text
from engine.profiling.semantic_actual import profile_semantic_actual
from engine.profiling.semantic_date import profile_semantic_date
from engine.semantic.actual import SemanticActualColumnProfile, classify_actual


def _profile(header: object, values: list[object], *, physical_type: str = "numeric", formula_count: int = 0):
    return SemanticActualColumnProfile(
        physical_type=physical_type,
        formulas=FormulaConsistencyProfile(formula_count=formula_count),
        numeric_text=profile_numeric_text(values),
        semantic_date=profile_semantic_date(values),
        semantic_actual=profile_semantic_actual(header, values),
    )


class SemanticActualTests(unittest.TestCase):
    def test_classifies_closed_vocabulary_with_physical_numbers_without_retaining_content(self):
        profile = _profile("Realizado", list(range(10, 30)))
        result = classify_actual(profile)
        self.assertEqual(result[0]["semantic_type"], "actual_candidate")
        self.assertEqual(result[0]["confidence"], 0.75)
        self.assertTrue(result[0]["question"]["blocking"])
        self.assertNotIn("10", repr(profile.semantic_actual))

    def test_accepts_actual_and_executed_vocabulary(self):
        self.assertTrue(classify_actual(_profile("valor executado", list(range(10, 20)))))
        self.assertTrue(classify_actual(_profile("observado", list(range(10, 20)))))
        self.assertTrue(classify_actual(_profile("actual", list(range(10, 20)))))

    def test_excludes_open_header_small_base_formulas_and_non_numeric_physical_type(self):
        self.assertEqual(classify_actual(_profile("meta", list(range(10, 20)))), [])
        self.assertEqual(classify_actual(_profile("realizado", list(range(9)))), [])
        self.assertEqual(classify_actual(_profile("realizado", list(range(10, 20)), formula_count=1)), [])
        self.assertEqual(classify_actual(_profile("realizado", list(range(10, 20)), physical_type="text")), [])

    def test_excludes_numeric_text_ambiguity_and_recognized_dates(self):
        self.assertEqual(classify_actual(_profile("realizado", ["10"] * 10, physical_type="numeric")), [])
        self.assertEqual(classify_actual(_profile("realizado", ["1,000"] * 10, physical_type="numeric")), [])
        self.assertEqual(
            classify_actual(_profile("realizado", [date(2026, 1, day) for day in range(1, 11)], physical_type="numeric")),
            [],
        )
