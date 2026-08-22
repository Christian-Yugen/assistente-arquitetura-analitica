from __future__ import annotations

import dataclasses
import unittest

from engine.granularity.event_per_row import EventPerRowSheetProfile, classify_event_per_row
from engine.profiling.event_per_row_grain import profile_event_marker_header


def candidate(**overrides: int) -> EventPerRowSheetProfile:
    values = {
        "observed_row_count": 20,
        "event_header_eligible_count": 1,
        "explicit_key_candidate_count": 1,
        "non_competence_date_candidate_count": 1,
        "excluded_event_marker_count": 0,
        "event_marker_formula_count": 0,
        "ambiguity_count": 0,
    }
    values.update(overrides)
    return EventPerRowSheetProfile(**values)


class EventPerRowGrainTests(unittest.TestCase):
    def test_detects_event_per_row_under_all_closed_guards(self) -> None:
        results = classify_event_per_row(candidate())
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["grain_type"], "event_per_row_candidate")
        self.assertEqual(results[0]["confidence"], 0.80)
        self.assertTrue(results[0]["question"]["blocking"])

    def test_accepts_closed_event_marker_vocabulary(self) -> None:
        for header in ("Evento", "Transação", "Ocorrência"):
            with self.subTest(header=header):
                self.assertTrue(profile_event_marker_header(header).header_eligible)
        self.assertFalse(profile_event_marker_header("Movimento").header_eligible)

    def test_rejects_any_guard_or_ambiguity(self) -> None:
        cases = (
            candidate(observed_row_count=19),
            candidate(event_header_eligible_count=0),
            candidate(event_header_eligible_count=2, ambiguity_count=1),
            candidate(explicit_key_candidate_count=0),
            candidate(non_competence_date_candidate_count=0),
            candidate(excluded_event_marker_count=1),
            candidate(event_marker_formula_count=1),
            candidate(ambiguity_count=1),
        )
        for profile in cases:
            with self.subTest(profile=profile):
                self.assertEqual(classify_event_per_row(profile), [])

    def test_profiles_do_not_retain_header_or_values(self) -> None:
        serialized = str(dataclasses.asdict(candidate())) + str(dataclasses.asdict(profile_event_marker_header("Evento")))
        self.assertNotIn("Evento", serialized)
        self.assertNotIn("valor-secreto", serialized)
