import unittest

from engine.profiling.formula_consistency import FormulaConsistencyProfile
from engine.profiling.numeric_text import infer_physical_type
from engine.profiling.semantic_date import profile_semantic_date
from engine.profiling.semantic_description import profile_semantic_description
from engine.profiling.semantic_identifier import profile_semantic_identifier
from engine.semantic.description import SemanticDescriptionColumnProfile, classify_name_or_description


def _profile(header: object, values: list[object], *, formula_count: int = 0):
    return SemanticDescriptionColumnProfile(
        physical_type=infer_physical_type(values),
        formulas=FormulaConsistencyProfile(formula_count=formula_count),
        semantic_date=profile_semantic_date(values),
        semantic_identifier=profile_semantic_identifier(str(header), values),
        semantic_description=profile_semantic_description(header),
    )


class SemanticDescriptionTests(unittest.TestCase):
    def test_classifies_closed_vocabulary_from_aggregate_text_signals_without_retaining_header(self):
        profile = _profile("Nome", [f"rotulo-{index:02d}" for index in range(1, 11)])
        result = classify_name_or_description(profile)
        self.assertEqual(result[0]["semantic_type"], "name_or_description_candidate")
        self.assertEqual(result[0]["confidence"], 0.70)
        self.assertTrue(result[0]["question"]["blocking"])
        self.assertNotIn("Nome", repr(profile.semantic_description))
        self.assertNotIn("rotulo-01", repr(result[0]["evidence"]))

    def test_accepts_the_complete_closed_header_vocabulary(self):
        values = [f"texto-sintetico-{index:02d}" for index in range(1, 11)]
        self.assertTrue(classify_name_or_description(_profile("nome", values)))
        self.assertTrue(classify_name_or_description(_profile("descrição", values)))
        self.assertTrue(classify_name_or_description(_profile("descricao", values)))

    def test_excludes_open_header_small_base_formula_dates_mixed_types_and_low_distinction(self):
        labels = [f"valor-sintetico-{index:02d}" for index in range(1, 11)]
        self.assertEqual(classify_name_or_description(_profile("categoria", labels)), [])
        self.assertEqual(classify_name_or_description(_profile("nome", labels[:9])), [])
        self.assertEqual(classify_name_or_description(_profile("nome", labels, formula_count=1)), [])
        self.assertEqual(classify_name_or_description(_profile("descrição", [f"2026-01-{index:02d}" for index in range(1, 11)])), [])
        self.assertEqual(classify_name_or_description(_profile("descricao", [1, *labels[1:]])), [])
        self.assertEqual(classify_name_or_description(_profile("descricao", ["constante"] * 10)), [])
