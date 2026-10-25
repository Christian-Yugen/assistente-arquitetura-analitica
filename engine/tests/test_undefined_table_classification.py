from __future__ import annotations

from dataclasses import replace
import unittest

from engine.fact_dimension.undefined_classification import (
    UndefinedTableClassificationSheetProfile,
    classify_undefined_table_classification,
)


class UndefinedTableClassificationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.eligible_profile = UndefinedTableClassificationSheetProfile(
            observed_row_count=20,
            physical_column_count=2,
            evaluated_table_classifier_count=5,
            positive_table_classification_count=0,
            classification_conflict_count=0,
            formula_column_count=0,
            sensitive_candidate_count=0,
            classification_ambiguity_count=0,
        )

    def test_emits_a_private_blocking_residual_hypothesis_when_all_guards_hold(self):
        candidate = classify_undefined_table_classification(self.eligible_profile)

        self.assertEqual(candidate[0]["classification_type"], "table_classification_undefined_candidate")
        self.assertEqual(candidate[0]["confidence"], 0.60)
        self.assertEqual(candidate[0]["evidence"]["evaluated_table_classifier_count"], 5)
        self.assertEqual(candidate[0]["evidence"]["positive_table_classification_count"], 0)
        self.assertTrue(candidate[0]["question"]["blocking"])

    def test_keeps_the_residual_hypothesis_when_a_non_structural_sensitive_attribute_exists(self):
        candidate = classify_undefined_table_classification(replace(self.eligible_profile, sensitive_candidate_count=1))

        self.assertEqual(candidate[0]["classification_type"], "table_classification_undefined_candidate")
        self.assertEqual(candidate[0]["evidence"]["sensitive_candidate_count"], 1)

    def test_profile_and_evidence_do_not_accept_or_emit_raw_or_classifier_identity_data(self):
        candidate = classify_undefined_table_classification(self.eligible_profile)[0]

        self.assertNotIn("header", repr(self.eligible_profile).lower())
        self.assertNotIn("value", repr(self.eligible_profile).lower())
        self.assertFalse({"header", "value", "sheet_name", "position", "classifier_ids"} & set(candidate["evidence"]))

    def test_all_mandatory_guards_block_the_residual_hypothesis(self):
        blocked_profiles = (
            replace(self.eligible_profile, observed_row_count=19),
            replace(self.eligible_profile, physical_column_count=1),
            replace(self.eligible_profile, evaluated_table_classifier_count=4),
            replace(self.eligible_profile, evaluated_table_classifier_count=6),
            replace(self.eligible_profile, positive_table_classification_count=1),
            replace(self.eligible_profile, classification_conflict_count=1),
            replace(self.eligible_profile, formula_column_count=1),
            replace(self.eligible_profile, classification_ambiguity_count=1),
        )

        for blocked_profile in blocked_profiles:
            with self.subTest(profile=blocked_profile):
                self.assertEqual(classify_undefined_table_classification(blocked_profile), [])


if __name__ == "__main__":
    unittest.main()
