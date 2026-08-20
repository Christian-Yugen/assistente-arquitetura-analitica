import unittest

from engine.contracts.diagnosis import to_diagnosis_fragment
from engine.quality.numtext import (
    CANONICAL_NUMERIC_TEXT_BASIS,
    NumericTextColumnProfile,
    evaluate_numeric_text,
)
from engine.quality.registry import QUALITY_RULE_IMPLEMENTATIONS


class NumericTextRuleTests(unittest.TestCase):
    def test_emits_high_severity_and_blocking_question_for_majority_numeric_text(self):
        findings = evaluate_numeric_text(
            NumericTextColumnProfile(
                name="Valor",
                physical_type="text",
                non_empty_value_count=100,
                numeric_text_candidate_count=92,
                numeric_text_candidate_ratio=0.92,
                numeric_text_basis=CANONICAL_NUMERIC_TEXT_BASIS,
            )
        )

        self.assertEqual(len(findings), 1)
        self.assertEqual(findings[0]["severity"], "high")
        self.assertEqual(findings[0]["confidence"], 0.9)
        self.assertTrue(findings[0]["question"])
        self.assertTrue(all("raw_value" not in item for item in findings[0]["evidence"]))

    def test_emits_medium_severity_and_penalizes_ambiguous_numeric_strings(self):
        findings = evaluate_numeric_text(
            NumericTextColumnProfile(
                name="Quantidade",
                physical_type="mixed",
                non_empty_value_count=100,
                numeric_text_candidate_count=20,
                numeric_text_candidate_ratio=0.2,
                numeric_text_basis=CANONICAL_NUMERIC_TEXT_BASIS,
                numeric_text_ambiguity_count=12,
            )
        )

        self.assertEqual(findings[0]["severity"], "medium")
        self.assertEqual(findings[0]["confidence"], 0.65)
        self.assertIsNone(findings[0]["question"])

    def test_does_not_fire_for_a_true_numeric_column_or_unknown_basis(self):
        numeric = NumericTextColumnProfile(
            name="Saldo",
            physical_type="numeric",
            non_empty_value_count=10,
            numeric_text_candidate_count=10,
            numeric_text_candidate_ratio=1.0,
            numeric_text_basis=CANONICAL_NUMERIC_TEXT_BASIS,
        )
        unsupported = NumericTextColumnProfile(
            name="Código",
            physical_type="text",
            non_empty_value_count=10,
            numeric_text_candidate_count=10,
            numeric_text_candidate_ratio=1.0,
            numeric_text_basis="heuristic_only",
        )

        self.assertEqual(evaluate_numeric_text(numeric), [])
        self.assertEqual(evaluate_numeric_text(unsupported), [])

    def test_registers_the_rule_by_its_canonical_identifier(self):
        self.assertIs(QUALITY_RULE_IMPLEMENTATIONS["QLT-NUMTEXT-007"], evaluate_numeric_text)

    def test_adapts_high_severity_result_to_canonical_findings_and_questions(self):
        findings = evaluate_numeric_text(
            NumericTextColumnProfile(
                name="Receita",
                physical_type="text",
                non_empty_value_count=20,
                numeric_text_candidate_count=18,
                numeric_text_candidate_ratio=0.9,
                numeric_text_basis=CANONICAL_NUMERIC_TEXT_BASIS,
            )
        )

        fragment = to_diagnosis_fragment(findings, sheet_id="sheet-1", column_id="column-1")

        self.assertEqual(fragment["schema_version"], "1.0.0")
        self.assertEqual(fragment["contract_id"], "PM-MVP-PBI-CON-001")
        self.assertEqual(len(fragment["findings"]), 1)
        self.assertEqual(fragment["findings"][0]["rule_id"], "QLT-NUMTEXT-007")
        self.assertEqual(fragment["findings"][0]["affected_entities"][1], {"entity_type": "column", "entity_id": "column-1"})
        self.assertEqual(len(fragment["questions"]), 1)
        self.assertEqual(fragment["questions"][0]["status"], "pending")


if __name__ == "__main__":
    unittest.main()
