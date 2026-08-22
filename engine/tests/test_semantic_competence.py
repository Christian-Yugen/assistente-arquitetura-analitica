import unittest
from datetime import date

from engine.profiling.formula_consistency import FormulaConsistencyProfile
from engine.profiling.semantic_competence import profile_semantic_competence
from engine.profiling.semantic_date import profile_semantic_date
from engine.semantic.competence import SemanticCompetenceColumnProfile, classify_competence_date


def _profile(header: object, values: list[object], *, formula_count: int = 0):
    return SemanticCompetenceColumnProfile(
        formulas=FormulaConsistencyProfile(formula_count=formula_count),
        semantic_date=profile_semantic_date(values),
        semantic_competence=profile_semantic_competence(header),
    )


class SemanticCompetenceTests(unittest.TestCase):
    def test_classifies_closed_vocabulary_and_strict_dates_without_retaining_header(self):
        profile = _profile("Data de Competência", [date(2026, 1, day) for day in range(1, 11)])
        result = classify_competence_date(profile)
        self.assertEqual(result[0]["semantic_type"], "competence_date_candidate")
        self.assertEqual(result[0]["confidence"], 0.85)
        self.assertTrue(result[0]["question"]["blocking"])
        self.assertNotIn("Competência", repr(profile.semantic_competence))

    def test_accepts_the_entire_closed_header_vocabulary(self):
        values = [f"2026-02-{day:02d}" for day in range(1, 11)]
        self.assertTrue(classify_competence_date(_profile("competência", values)))
        self.assertTrue(classify_competence_date(_profile("data competência", values)))
        self.assertTrue(classify_competence_date(_profile("data de competência", values)))

    def test_excludes_open_header_small_base_formula_and_partial_coverage(self):
        strict_dates = [f"2026-03-{day:02d}" for day in range(1, 11)]
        self.assertEqual(classify_competence_date(_profile("período", strict_dates)), [])
        self.assertEqual(classify_competence_date(_profile("competência", strict_dates[:9])), [])
        self.assertEqual(classify_competence_date(_profile("competência", strict_dates, formula_count=1)), [])
        self.assertEqual(classify_competence_date(_profile("competência", [*strict_dates[:9], "2026-02-30"])), [])

    def test_accepts_brazilian_hyphen_and_slash_dates_without_date_conversion(self):
        hyphen = [f"{day:02d}-04-2026" for day in range(1, 11)]
        slash = [f"{day:02d}/05/2026" for day in range(1, 11)]
        self.assertTrue(classify_competence_date(_profile("competência", hyphen)))
        self.assertTrue(classify_competence_date(_profile("competência", slash)))
