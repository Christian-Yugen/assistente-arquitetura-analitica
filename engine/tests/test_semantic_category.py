import unittest

from engine.profiling.formula_consistency import FormulaConsistencyProfile
from engine.profiling.numeric_text import infer_physical_type
from engine.profiling.semantic_category import profile_semantic_category
from engine.profiling.semantic_date import profile_semantic_date
from engine.profiling.semantic_identifier import profile_semantic_identifier
from engine.semantic.category import SemanticCategoryColumnProfile, classify_category


def _profile(header: object, values: list[object], *, formula_count: int = 0) -> SemanticCategoryColumnProfile:
    return SemanticCategoryColumnProfile(
        physical_type=infer_physical_type(values),
        formulas=FormulaConsistencyProfile(formula_count=formula_count),
        semantic_date=profile_semantic_date(values),
        semantic_identifier=profile_semantic_identifier(str(header), values),
        semantic_category=profile_semantic_category(header, values),
    )


class SemanticCategoryTests(unittest.TestCase):
    def test_classifies_closed_header_with_aggregate_cardinality_without_retaining_labels(self):
        values = ["rotulo_sintetico_a"] * 5 + ["rotulo_sintetico_b"] * 5
        profile = _profile("Categoria", values)
        result = classify_category(profile)
        self.assertEqual(result[0]["semantic_type"], "category_candidate")
        self.assertEqual(result[0]["confidence"], 0.70)
        self.assertTrue(result[0]["question"]["blocking"])
        self.assertNotIn("Categoria", repr(profile.semantic_category))
        self.assertNotIn("rotulo_sintetico_a", repr(result[0]["evidence"]))

    def test_accepts_only_the_closed_header_after_transient_normalization(self):
        values = ["grupo_a"] * 5 + ["grupo_b"] * 5
        self.assertTrue(classify_category(_profile("categoria", values)))
        self.assertTrue(classify_category(_profile("  CATEGORIA  ", values)))
        self.assertEqual(classify_category(_profile("categorias", values)), [])

    def test_excludes_open_header_small_base_formula_dates_mixed_types_and_invalid_cardinality(self):
        values = ["categoria_a"] * 5 + ["categoria_b"] * 5
        self.assertEqual(classify_category(_profile("grupo", values)), [])
        self.assertEqual(classify_category(_profile("categoria", values[:9])), [])
        self.assertEqual(classify_category(_profile("categoria", values, formula_count=1)), [])
        self.assertEqual(classify_category(_profile("categoria", [f"2026-01-{index:02d}" for index in range(1, 11)])), [])
        self.assertEqual(classify_category(_profile("categoria", [1, *values[1:]])), [])
        self.assertEqual(classify_category(_profile("categoria", [f"grupo_{index:02d}" for index in range(21)])), [])
        self.assertEqual(classify_category(_profile("categoria", [f"grupo_{index}" for index in range(6)] + ["grupo_0"] * 4)), [])
