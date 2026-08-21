import unittest
from datetime import date

from engine.profiling.formula_consistency import FormulaConsistencyProfile
from engine.profiling.numeric_text import profile_numeric_text
from engine.profiling.semantic_date import profile_semantic_date
from engine.profiling.semantic_quantity import profile_semantic_quantity
from engine.semantic.quantity import SemanticQuantityColumnProfile, classify_quantity


def _profile(header: object, values: list[object], *, physical_type: str = "numeric", formula_count: int = 0):
    return SemanticQuantityColumnProfile(
        physical_type=physical_type,
        formulas=FormulaConsistencyProfile(formula_count=formula_count),
        numeric_text=profile_numeric_text(values),
        semantic_date=profile_semantic_date(values),
        semantic_quantity=profile_semantic_quantity(header, values),
    )


class SemanticQuantityTests(unittest.TestCase):
    def test_classifies_closed_vocabulary_with_physical_numbers_without_retaining_content(self):
        profile = _profile("Quantidade", list(range(10, 30)))
        result = classify_quantity(profile)
        self.assertEqual(result[0]["semantic_type"], "quantity_candidate")
        self.assertEqual(result[0]["confidence"], 0.75)
        self.assertTrue(result[0]["question"]["blocking"])
        self.assertNotIn("10", repr(profile.semantic_quantity))

    def test_accepts_the_two_abbreviations_in_the_closed_vocabulary(self):
        self.assertTrue(classify_quantity(_profile("qtd", list(range(10, 20)))))
        self.assertTrue(classify_quantity(_profile("qtde", list(range(10, 20)))))

    def test_excludes_open_header_small_base_formulas_and_non_numeric_physical_type(self):
        self.assertEqual(classify_quantity(_profile("estoque", list(range(10, 20)))), [])
        self.assertEqual(classify_quantity(_profile("qtd", list(range(9)))), [])
        self.assertEqual(classify_quantity(_profile("qtd", list(range(10, 20)), formula_count=1)), [])
        self.assertEqual(classify_quantity(_profile("qtd", list(range(10, 20)), physical_type="text")), [])

    def test_excludes_numeric_text_ambiguity_and_recognized_dates(self):
        self.assertEqual(classify_quantity(_profile("qtd", ["10"] * 10, physical_type="numeric")), [])
        self.assertEqual(classify_quantity(_profile("qtd", ["1,000"] * 10, physical_type="numeric")), [])
        self.assertEqual(
            classify_quantity(_profile("qtd", [date(2026, 1, day) for day in range(1, 11)], physical_type="numeric")),
            [],
        )
