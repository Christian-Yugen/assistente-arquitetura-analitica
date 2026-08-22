import unittest

from engine.profiling.formula_consistency import FormulaConsistencyProfile
from engine.profiling.numeric_text import infer_physical_type
from engine.profiling.semantic_date import profile_semantic_date
from engine.profiling.semantic_identifier import profile_semantic_identifier
from engine.profiling.semantic_responsible import profile_semantic_responsible
from engine.semantic.responsible import SemanticResponsibleColumnProfile, classify_responsible


def _profile(header: object, values: list[object], *, formula_count: int = 0) -> SemanticResponsibleColumnProfile:
    return SemanticResponsibleColumnProfile(
        physical_type=infer_physical_type(values),
        formulas=FormulaConsistencyProfile(formula_count=formula_count),
        semantic_date=profile_semantic_date(values),
        semantic_identifier=profile_semantic_identifier(str(header), values),
        semantic_responsible=profile_semantic_responsible(header, values),
    )


class SemanticResponsibleTests(unittest.TestCase):
    def test_classifies_closed_header_with_aggregate_cardinality_without_retaining_labels(self):
        values = ["papel_sintetico_a"] * 5 + ["papel_sintetico_b"] * 5
        profile = _profile("Responsável", values)
        result = classify_responsible(profile)
        self.assertEqual(result[0]["semantic_type"], "responsible_candidate")
        self.assertEqual(result[0]["confidence"], 0.70)
        self.assertTrue(result[0]["question"]["blocking"])
        self.assertNotIn("Responsável", repr(profile.semantic_responsible))
        self.assertNotIn("papel_sintetico_a", repr(result[0]["evidence"]))

    def test_accepts_only_closed_header_after_transient_normalization(self):
        values = ["papel_a"] * 5 + ["papel_b"] * 5
        for header in ("responsável", " RESPONSÁVEL ", "Responsavel"):
            self.assertTrue(classify_responsible(_profile(header, values)))
        for header in ("responsaveis", "gestor", "owner", "equipe"):
            self.assertEqual(classify_responsible(_profile(header, values)), [])

    def test_excludes_small_base_formula_dates_mixed_types_and_invalid_cardinality(self):
        values = ["papel_a"] * 5 + ["papel_b"] * 5
        self.assertEqual(classify_responsible(_profile("responsável", values[:9])), [])
        self.assertEqual(classify_responsible(_profile("responsável", values, formula_count=1)), [])
        self.assertEqual(classify_responsible(_profile("responsável", [f"2026-01-{index:02d}" for index in range(1, 11)])), [])
        self.assertEqual(classify_responsible(_profile("responsável", [1, *values[1:]])), [])
        self.assertEqual(classify_responsible(_profile("responsável", [f"papel_{index:02d}" for index in range(51)])), [])
        self.assertEqual(classify_responsible(_profile("responsável", [f"papel_{index}" for index in range(10)])), [])
