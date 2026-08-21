import unittest

from engine.contracts.diagnosis import to_sensitivity_fragment
from engine.profiling.semantic_identifier import profile_semantic_identifier
from engine.profiling.semantic_sensitivity import profile_semantic_sensitivity
from engine.semantic.sensitivity import SemanticSensitivityColumnProfile, classify_sensitivity


def _profile(header: object, values: list[object]) -> SemanticSensitivityColumnProfile:
    return SemanticSensitivityColumnProfile(
        semantic_sensitivity=profile_semantic_sensitivity(profile_semantic_identifier(header, values)),
    )


class SemanticSensitivityTests(unittest.TestCase):
    def test_classifies_closed_sensitive_headers_with_non_missing_observations_only(self):
        result = classify_sensitivity(_profile("CPF", ["__OBSERVACAO_SINTETICA_A__"]))

        self.assertEqual(result[0]["sensitivity"], "personal_data_candidate")
        self.assertEqual(result[0]["confidence"], 0.90)
        self.assertTrue(result[0]["question"]["blocking"])
        self.assertEqual(result[0]["evidence"]["non_missing_count"], 1)

    def test_accepts_email_and_phone_vocabulary_without_inspecting_values(self):
        self.assertTrue(classify_sensitivity(_profile("E-mail", ["__OBSERVACAO_SINTETICA_B__"])))
        self.assertTrue(classify_sensitivity(_profile("Telefone", ["__OBSERVACAO_SINTETICA_C__"])))

    def test_excludes_header_outside_closed_vocabulary_and_columns_without_observations(self):
        self.assertEqual(classify_sensitivity(_profile("Observação", ["__OBSERVACAO_SINTETICA_D__"])), [])
        self.assertEqual(classify_sensitivity(_profile("Nome", [None, "", "   "])), [])

    def test_projects_a_segregated_contract_fragment_without_raw_header_or_value(self):
        result = classify_sensitivity(_profile("CPF", ["__OBSERVACAO_SINTETICA_E__"]))
        fragment = to_sensitivity_fragment(
            result,
            sheet_id="00000000-0000-4000-8000-000000000010",
            column_id="00000000-0000-4000-8000-000000000011",
        )
        serialized = repr(fragment)

        self.assertIn("sensitivity_classifications", fragment)
        self.assertNotIn("semantic_classifications", fragment)
        self.assertEqual(fragment["sensitivity_classifications"][0]["sensitivity"], "personal_data_candidate")
        self.assertNotIn("CPF", serialized)
        self.assertNotIn("__OBSERVACAO_SINTETICA_E__", serialized)
