import unittest

from engine.profiling.formula_consistency import FormulaConsistencyProfile
from engine.profiling.numeric_text import infer_physical_type, profile_numeric_text
from engine.profiling.semantic_date import profile_semantic_date
from engine.profiling.semantic_duration import profile_semantic_duration
from engine.semantic.duration import SemanticDurationColumnProfile, classify_duration


def _profile(header: str, values: list[object], *, formula_count: int = 0) -> SemanticDurationColumnProfile:
    return SemanticDurationColumnProfile(
        physical_type=infer_physical_type(values),
        formulas=FormulaConsistencyProfile(formula_count=formula_count),
        numeric_text=profile_numeric_text(values),
        semantic_date=profile_semantic_date(values),
        semantic_duration=profile_semantic_duration(header, values),
    )


class SemanticDurationTests(unittest.TestCase):
    def test_classifies_closed_vocabulary_with_physical_numbers_without_retaining_header_or_values(self):
        profile = _profile("Duração (horas)", list(range(101, 111)))
        result = classify_duration(profile)
        self.assertEqual(result[0]["semantic_type"], "duration_candidate")
        self.assertEqual(result[0]["confidence"], 0.80)
        self.assertTrue(result[0]["question"]["blocking"])
        self.assertNotIn("Duração", repr(profile.semantic_duration))
        self.assertNotIn("101", repr(profile.semantic_duration))

    def test_accepts_the_entire_closed_header_vocabulary(self):
        values = list(range(1, 11))
        self.assertTrue(classify_duration(_profile("duração", values)))
        self.assertTrue(classify_duration(_profile("duração (horas)", values)))
        self.assertTrue(classify_duration(_profile("duração (minutos)", values)))
        self.assertTrue(classify_duration(_profile("duração (segundos)", values)))
        self.assertTrue(classify_duration(_profile("duração (dias)", values)))

    def test_excludes_open_header_small_base_formula_text_and_ambiguous_values(self):
        numbers = list(range(1, 11))
        self.assertEqual(classify_duration(_profile("tempo", numbers)), [])
        self.assertEqual(classify_duration(_profile("duração", numbers[:9])), [])
        self.assertEqual(classify_duration(_profile("duração", numbers, formula_count=1)), [])
        self.assertEqual(classify_duration(_profile("duração", [*numbers[:9], "10"])), [])
        self.assertEqual(classify_duration(_profile("duração", [*numbers[:9], True])), [])

    def test_excludes_dates_and_non_finite_numbers(self):
        self.assertEqual(classify_duration(_profile("duração", [f"2026-01-{day:02d}" for day in range(1, 11)])), [])
        self.assertEqual(classify_duration(_profile("duração", [*range(1, 10), float("inf")])), [])
