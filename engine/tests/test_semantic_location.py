import unittest

from engine.profiling.formula_consistency import FormulaConsistencyProfile
from engine.profiling.numeric_text import infer_physical_type
from engine.profiling.semantic_date import profile_semantic_date
from engine.profiling.semantic_identifier import profile_semantic_identifier
from engine.profiling.semantic_location import profile_semantic_location
from engine.semantic.location import SemanticLocationColumnProfile, classify_location


def _profile(header: object, values: list[object], *, formula_count: int = 0) -> SemanticLocationColumnProfile:
    return SemanticLocationColumnProfile(
        physical_type=infer_physical_type(values),
        formulas=FormulaConsistencyProfile(formula_count=formula_count),
        semantic_date=profile_semantic_date(values),
        semantic_identifier=profile_semantic_identifier(str(header), values),
        semantic_location=profile_semantic_location(header, values),
    )


class SemanticLocationTests(unittest.TestCase):
    def test_classifies_closed_header_with_aggregate_cardinality_without_retaining_labels(self):
        values = ["local_sintetico_a"] * 5 + ["local_sintetico_b"] * 5
        profile = _profile("Cidade", values)
        result = classify_location(profile)
        self.assertEqual(result[0]["semantic_type"], "location_candidate")
        self.assertEqual(result[0]["confidence"], 0.75)
        self.assertTrue(result[0]["question"]["blocking"])
        self.assertNotIn("Cidade", repr(profile.semantic_location))
        self.assertNotIn("local_sintetico_a", repr(result[0]["evidence"]))

    def test_accepts_only_closed_headers_after_transient_normalization(self):
        values = ["local_a"] * 5 + ["local_b"] * 5
        for header in ("cidade", " Município ", "PAÍS", "Região", "LOCALIZAÇÃO"):
            self.assertTrue(classify_location(_profile(header, values)))
        for header in ("estado", "uf", "endereco", "bairro"):
            self.assertEqual(classify_location(_profile(header, values)), [])

    def test_excludes_small_base_formula_dates_mixed_types_and_invalid_cardinality(self):
        values = ["local_a"] * 5 + ["local_b"] * 5
        self.assertEqual(classify_location(_profile("cidade", values[:9])), [])
        self.assertEqual(classify_location(_profile("cidade", values, formula_count=1)), [])
        self.assertEqual(classify_location(_profile("cidade", [f"2026-01-{index:02d}" for index in range(1, 11)])), [])
        self.assertEqual(classify_location(_profile("cidade", [1, *values[1:]])), [])
        self.assertEqual(classify_location(_profile("cidade", [f"local_{index:02d}" for index in range(51)])), [])
        self.assertEqual(classify_location(_profile("cidade", [f"local_{index}" for index in range(10)])), [])
