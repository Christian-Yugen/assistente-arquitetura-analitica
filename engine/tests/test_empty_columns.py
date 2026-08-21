import unittest

from engine.contracts.diagnosis import to_diagnosis_fragment
from engine.profiling.missingness import profile_missingness
from engine.quality.empty_columns import EmptyColumnProfile, evaluate_empty_column
from engine.quality.registry import QUALITY_RULE_IMPLEMENTATIONS


class EmptyColumnTests(unittest.TestCase):
    def test_option_a_detects_only_structural_null_and_blank_text_cells(self):
        profile = EmptyColumnProfile(name="Reserva", missingness=profile_missingness([None, "   ", None, ""]))

        finding = evaluate_empty_column(profile)[0]

        self.assertEqual(finding["rule_id"], "QLT-EMPTYCOL-003")
        self.assertEqual(finding["severity"], "low")
        self.assertEqual(finding["confidence"], 0.95)
        self.assertFalse(finding["question"])
        self.assertEqual(finding["evidence"][1]["observed_value"], 4)

    def test_option_a_does_not_treat_valid_values_or_numeric_nan_as_empty(self):
        valid_value_profiles = [
            profile_missingness([None, 0, None]),
            profile_missingness([None, False, None]),
            profile_missingness([None, "=SUM(A1:A2)", None]),
            profile_missingness([None, float("nan"), None]),
        ]

        for missingness in valid_value_profiles:
            with self.subTest(missingness=missingness):
                self.assertEqual(evaluate_empty_column(EmptyColumnProfile(name="Campo", missingness=missingness)), [])

    def test_emits_high_finding_and_blocking_question_for_large_empty_column(self):
        profile = EmptyColumnProfile(name="Campo técnico", missingness=profile_missingness([None] * 101))

        finding = evaluate_empty_column(profile)[0]

        self.assertEqual(finding["severity"], "high")
        self.assertEqual(finding["confidence"], 0.95)
        self.assertTrue(finding["question"])
        self.assertTrue(finding["question"]["blocking"])
        self.assertIn("finalidade", finding["recommendation"])

    def test_adapts_finding_to_canonical_contract_without_raw_cell_values(self):
        profile = EmptyColumnProfile(name="Campo", missingness=profile_missingness([None, " ", None]))
        findings = evaluate_empty_column(profile)
        fragment = to_diagnosis_fragment(findings, sheet_id="sheet-1", column_id="column-1")

        contract_finding = fragment["findings"][0]
        self.assertEqual(contract_finding["rule_id"], "QLT-EMPTYCOL-003")
        self.assertEqual(contract_finding["rule_version"], "0.1.0-reconstructed.1")
        self.assertEqual(contract_finding["affected_entities"][1], {"entity_type": "column", "entity_id": "column-1"})
        self.assertNotIn("segredo", str(contract_finding))

    def test_profile_keeps_only_aggregate_counts(self):
        profile = profile_missingness([None, "   ", "segredo"])

        self.assertNotIn("segredo", str(profile.__dict__))
        self.assertIsNotNone(QUALITY_RULE_IMPLEMENTATIONS["QLT-EMPTYCOL-003"])


if __name__ == "__main__":
    unittest.main()
