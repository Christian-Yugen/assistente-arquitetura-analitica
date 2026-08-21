import unittest
from datetime import date

from engine.profiling.formula_consistency import FormulaConsistencyProfile
from engine.profiling.numeric_text import profile_numeric_text
from engine.profiling.semantic_date import profile_semantic_date
from engine.profiling.semantic_percentage import profile_semantic_percentage
from engine.semantic.percentage import SemanticPercentageColumnProfile, classify_percentage


def _profile(header: object, values: list[object], *, physical_type: str = "numeric", formula_count: int = 0):
    return SemanticPercentageColumnProfile(
        physical_type=physical_type,
        formulas=FormulaConsistencyProfile(formula_count=formula_count),
        numeric_text=profile_numeric_text(values),
        semantic_date=profile_semantic_date(values),
        semantic_percentage=profile_semantic_percentage(header, values),
    )


class SemanticPercentageTests(unittest.TestCase):
    def test_classifies_percentual_with_unit_interval_physical_numbers_without_retaining_content(self):
        profile = _profile("Percentual", [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 1.0])
        result = classify_percentage(profile)
        self.assertEqual(result[0]["semantic_type"], "percentage_candidate")
        self.assertEqual(result[0]["confidence"], 0.75)
        self.assertTrue(result[0]["question"]["blocking"])
        self.assertNotIn("0.1", repr(profile.semantic_percentage))

    def test_accepts_pct_and_percent_symbol_in_the_closed_vocabulary(self):
        values = [0.1] * 10
        self.assertTrue(classify_percentage(_profile("pct", values)))
        self.assertTrue(classify_percentage(_profile("%", values)))

    def test_excludes_open_header_small_base_out_of_range_formulas_and_non_numeric_physical_type(self):
        valid_values = [0.1] * 10
        self.assertEqual(classify_percentage(_profile("taxa", valid_values)), [])
        self.assertEqual(classify_percentage(_profile("percentual", [0.1] * 9)), [])
        self.assertEqual(classify_percentage(_profile("percentual", [0.1] * 9 + [1.1])), [])
        self.assertEqual(classify_percentage(_profile("percentual", valid_values, formula_count=1)), [])
        self.assertEqual(classify_percentage(_profile("percentual", valid_values, physical_type="text")), [])

    def test_excludes_numeric_text_ambiguity_and_recognized_dates(self):
        self.assertEqual(classify_percentage(_profile("pct", ["0.1"] * 10, physical_type="numeric")), [])
        self.assertEqual(classify_percentage(_profile("pct", ["1,000"] * 10, physical_type="numeric")), [])
        self.assertEqual(
            classify_percentage(_profile("pct", [date(2026, 1, day) for day in range(1, 11)], physical_type="numeric")),
            [],
        )
