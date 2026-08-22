import unittest

from engine.profiling.formula_consistency import FormulaConsistencyProfile
from engine.profiling.numeric_text import infer_physical_type
from engine.profiling.semantic_date import profile_semantic_date
from engine.profiling.semantic_description import profile_semantic_description
from engine.profiling.semantic_identifier import profile_semantic_identifier
from engine.profiling.semantic_status import profile_semantic_status
from engine.semantic.status import SemanticStatusColumnProfile, classify_status


def _profile(header: object, values: list[object], *, formula_count: int = 0) -> SemanticStatusColumnProfile:
    return SemanticStatusColumnProfile(
        physical_type=infer_physical_type(values),
        formulas=FormulaConsistencyProfile(formula_count=formula_count),
        semantic_date=profile_semantic_date(values),
        semantic_identifier=profile_semantic_identifier(str(header), values),
        semantic_description=profile_semantic_description(header),
        semantic_status=profile_semantic_status(header, values),
    )


class SemanticStatusTests(unittest.TestCase):
    def test_classifies_closed_vocabulary_with_aggregate_cardinality_without_retaining_labels(self):
        values = ["rotulo_sintetico_a"] * 5 + ["rotulo_sintetico_b"] * 5
        profile = _profile("Situação", values)
        result = classify_status(profile)
        self.assertEqual(result[0]["semantic_type"], "status_candidate")
        self.assertEqual(result[0]["confidence"], 0.75)
        self.assertTrue(result[0]["question"]["blocking"])
        self.assertNotIn("Situação", repr(profile.semantic_status))
        self.assertNotIn("rotulo_sintetico_a", repr(result[0]["evidence"]))

    def test_accepts_the_complete_closed_header_vocabulary(self):
        values = ["grupo_a"] * 5 + ["grupo_b"] * 5
        self.assertTrue(classify_status(_profile("status", values)))
        self.assertTrue(classify_status(_profile("situação", values)))
        self.assertTrue(classify_status(_profile("estado", values)))

    def test_excludes_open_header_small_base_formula_dates_mixed_types_and_invalid_cardinality(self):
        values = ["categoria_a"] * 5 + ["categoria_b"] * 5
        self.assertEqual(classify_status(_profile("fase", values)), [])
        self.assertEqual(classify_status(_profile("status", values[:9])), [])
        self.assertEqual(classify_status(_profile("status", values, formula_count=1)), [])
        self.assertEqual(classify_status(_profile("situação", [f"2026-01-{index:02d}" for index in range(1, 11)])), [])
        self.assertEqual(classify_status(_profile("estado", [1, *values[1:]])), [])
        self.assertEqual(classify_status(_profile("status", [f"categoria_{index:02d}" for index in range(13)])), [])
        self.assertEqual(classify_status(_profile("status", [f"grupo_{index}" for index in range(6)] + ["grupo_0"] * 4)), [])
