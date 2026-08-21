import unittest

from engine.profiling.semantic_identifier import profile_semantic_identifier
from engine.semantic.identifier import SemanticIdentifierColumnProfile, classify_identifier


class SemanticIdentifierTests(unittest.TestCase):
    def test_classifies_complete_unique_identifier_without_retaining_content(self):
        profile = profile_semantic_identifier("codigo", list(range(1001, 1021)))
        result = classify_identifier(SemanticIdentifierColumnProfile("numeric", 0, profile))
        self.assertEqual(result[0]["semantic_type"], "identifier")
        self.assertTrue(result[0]["evidence"]["individually_unique"])
        self.assertNotIn("1001", repr(profile))

    def test_classifies_repeated_component_when_diversity_is_sufficient(self):
        profile = profile_semantic_identifier("cod", [value for value in range(1, 11) for _ in range(2)])
        result = classify_identifier(SemanticIdentifierColumnProfile("numeric", 0, profile))
        self.assertTrue(result[0]["evidence"]["component_eligible"])

    def test_excludes_sensitive_header_low_coverage_formula_and_small_base(self):
        self.assertEqual(classify_identifier(SemanticIdentifierColumnProfile("numeric", 0, profile_semantic_identifier("cpf", range(1, 21)))), [])
        self.assertEqual(classify_identifier(SemanticIdentifierColumnProfile("numeric", 0, profile_semantic_identifier("codigo", [*range(1, 18), None, None, None]))), [])
        self.assertEqual(classify_identifier(SemanticIdentifierColumnProfile("numeric", 1, profile_semantic_identifier("codigo", range(1, 21)))), [])
        self.assertEqual(classify_identifier(SemanticIdentifierColumnProfile("numeric", 0, profile_semantic_identifier("codigo", range(1, 20)))), [])
