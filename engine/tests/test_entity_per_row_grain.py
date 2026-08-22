import dataclasses
import unittest

from engine.granularity.entity_per_row import EntityPerRowSheetProfile, classify_entity_per_row
from engine.profiling.entity_per_row_grain import profile_entity_marker_header


def candidate(**overrides: int) -> EntityPerRowSheetProfile:
    values = {
        "observed_row_count": 20,
        "entity_header_eligible_count": 1,
        "explicit_key_candidate_count": 1,
        "descriptive_attribute_candidate_count": 1,
        "non_competence_date_candidate_count": 0,
        "event_candidate_count": 0,
        "measure_candidate_count": 0,
        "sensitive_candidate_count": 0,
        "excluded_entity_marker_count": 0,
        "entity_marker_formula_count": 0,
        "ambiguity_count": 0,
    }
    values.update(overrides)
    return EntityPerRowSheetProfile(**values)


class EntityPerRowGrainTests(unittest.TestCase):
    def test_detects_entity_per_row_under_all_closed_guards(self) -> None:
        results = classify_entity_per_row(candidate())
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["grain_type"], "entity_per_row_candidate")
        self.assertEqual(results[0]["confidence"], 0.75)
        self.assertTrue(results[0]["question"]["blocking"])

    def test_accepts_closed_entity_marker_vocabulary(self) -> None:
        for header in ("Cliente", "Produto", "Fornecedor", "Colaborador", "Funcionário", "Paciente", "Aluno", "Conta"):
            with self.subTest(header=header):
                self.assertTrue(profile_entity_marker_header(header).header_eligible)
        self.assertFalse(profile_entity_marker_header("Empresa").header_eligible)

    def test_rejects_any_guard_or_ambiguity(self) -> None:
        cases = (
            candidate(observed_row_count=19),
            candidate(entity_header_eligible_count=0),
            candidate(entity_header_eligible_count=2, ambiguity_count=1),
            candidate(explicit_key_candidate_count=0),
            candidate(descriptive_attribute_candidate_count=0),
            candidate(non_competence_date_candidate_count=1),
            candidate(event_candidate_count=1),
            candidate(measure_candidate_count=1),
            candidate(sensitive_candidate_count=1),
            candidate(excluded_entity_marker_count=1),
            candidate(entity_marker_formula_count=1),
            candidate(ambiguity_count=1),
        )
        for profile in cases:
            with self.subTest(profile=profile):
                self.assertEqual(classify_entity_per_row(profile), [])

    def test_profiles_do_not_retain_header_or_values(self) -> None:
        serialized = str(dataclasses.asdict(candidate())) + str(dataclasses.asdict(profile_entity_marker_header("Cliente")))
        self.assertNotIn("Cliente", serialized)
        self.assertNotIn("valor-secreto", serialized)
