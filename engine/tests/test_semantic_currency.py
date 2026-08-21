import unittest
from datetime import date

from engine.profiling.formula_consistency import FormulaConsistencyProfile
from engine.profiling.numeric_text import profile_numeric_text
from engine.profiling.semantic_currency import profile_semantic_currency
from engine.profiling.semantic_date import profile_semantic_date
from engine.semantic.currency import SemanticCurrencyColumnProfile, classify_currency


def _profile(
    header: object,
    values: list[object],
    number_formats: list[object],
    *,
    physical_type: str = "numeric",
    formula_count: int = 0,
):
    return SemanticCurrencyColumnProfile(
        physical_type=physical_type,
        formulas=FormulaConsistencyProfile(formula_count=formula_count),
        numeric_text=profile_numeric_text(values),
        semantic_date=profile_semantic_date(values),
        semantic_currency=profile_semantic_currency(header, values, number_formats),
    )


class SemanticCurrencyTests(unittest.TestCase):
    def test_classifies_receita_with_explicit_currency_format_without_retaining_content(self):
        values = [100.0 + index for index in range(10)]
        profile = _profile("Receita", values, ["R$ #,##0.00"] * 10)
        result = classify_currency(profile)
        self.assertEqual(result[0]["semantic_type"], "currency_candidate")
        self.assertEqual(result[0]["confidence"], 0.80)
        self.assertTrue(result[0]["question"]["blocking"])
        self.assertNotIn("100.0", repr(profile.semantic_currency))
        self.assertNotIn("R$", repr(profile.semantic_currency))

    def test_accepts_normalized_closed_currency_headers_and_explicit_markers(self):
        values = [19.99] * 10
        self.assertTrue(classify_currency(_profile("Preço Unitário", values, ["$#,##0.00"] * 10)))
        self.assertTrue(classify_currency(_profile("Custo", values, ["€ #,##0.00"] * 10)))

    def test_excludes_open_header_small_base_incomplete_format_formulas_and_non_numeric_physical_type(self):
        values = [10.0] * 10
        formats = ["R$ #,##0.00"] * 10
        self.assertEqual(classify_currency(_profile("Montante", values, formats)), [])
        self.assertEqual(classify_currency(_profile("Receita", values[:9], formats[:9])), [])
        self.assertEqual(classify_currency(_profile("Receita", values, formats[:9] + ["0.00"])), [])
        self.assertEqual(classify_currency(_profile("Receita", values, formats, formula_count=1)), [])
        self.assertEqual(classify_currency(_profile("Receita", values, formats, physical_type="text")), [])

    def test_excludes_numeric_text_ambiguity_recognized_dates_and_absent_formats(self):
        self.assertEqual(classify_currency(_profile("Receita", ["10.00"] * 10, ["R$ #,##0.00"] * 10, physical_type="numeric")), [])
        self.assertEqual(classify_currency(_profile("Receita", ["1,000"] * 10, ["R$ #,##0.00"] * 10, physical_type="numeric")), [])
        self.assertEqual(
            classify_currency(_profile("Receita", [date(2026, 1, day) for day in range(1, 11)], ["R$ #,##0.00"] * 10, physical_type="numeric")),
            [],
        )
        self.assertEqual(classify_currency(_profile("Receita", [10.0] * 10, ["0.00"] * 10)), [])
