from __future__ import annotations

from dataclasses import replace
import unittest

from engine.fact_dimension.fact_without_grain import (
    FactWithoutDefinedGrainSheetProfile,
    classify_fact_without_defined_grain,
)


class FactWithoutDefinedGrainTests(unittest.TestCase):
    def setUp(self) -> None:
        self.eligible_profile = FactWithoutDefinedGrainSheetProfile(
            observed_row_count=20,
            eligible_numeric_measure_count=1,
            fact_signal_count=1,
            active_grain_hypothesis_count=0,
            dimensional_candidate_count=0,
            formula_column_count=0,
            sensitive_candidate_count=0,
            incompatible_temporal_signal_count=0,
            ambiguity_count=0,
        )

    def test_emits_a_private_blocking_hypothesis_when_all_guards_hold(self):
        candidate = classify_fact_without_defined_grain(self.eligible_profile)

        self.assertEqual(candidate[0]["classification_type"], "fact_without_defined_grain_candidate")
        self.assertEqual(candidate[0]["confidence"], 0.75)
        self.assertEqual(candidate[0]["evidence"]["observed_row_count"], 20)
        self.assertEqual(candidate[0]["evidence"]["active_grain_hypothesis_count"], 0)
        self.assertTrue(candidate[0]["question"]["blocking"])

    def test_profile_and_evidence_do_not_accept_or_emit_raw_workbook_content(self):
        candidate = classify_fact_without_defined_grain(self.eligible_profile)[0]

        self.assertNotIn("header", repr(self.eligible_profile).lower())
        self.assertNotIn("value", repr(self.eligible_profile).lower())
        self.assertFalse({"header", "value", "sheet_name", "position"} & set(candidate["evidence"]))

    def test_all_mandatory_guards_block_the_candidate(self):
        blocked_profiles = (
            replace(self.eligible_profile, observed_row_count=19),
            replace(self.eligible_profile, eligible_numeric_measure_count=0),
            replace(self.eligible_profile, fact_signal_count=0),
            replace(self.eligible_profile, active_grain_hypothesis_count=1),
            replace(self.eligible_profile, dimensional_candidate_count=1),
            replace(self.eligible_profile, formula_column_count=1),
            replace(self.eligible_profile, sensitive_candidate_count=1),
            replace(self.eligible_profile, incompatible_temporal_signal_count=1),
            replace(self.eligible_profile, ambiguity_count=1),
        )

        for blocked_profile in blocked_profiles:
            with self.subTest(profile=blocked_profile):
                self.assertEqual(classify_fact_without_defined_grain(blocked_profile), [])


if __name__ == "__main__":
    unittest.main()
