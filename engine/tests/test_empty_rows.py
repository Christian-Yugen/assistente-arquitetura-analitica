import unittest
from datetime import date

from engine.contracts.diagnosis import to_diagnosis_fragment
from engine.profiling.empty_rows import EmptyRowsProfile, profile_empty_rows
from engine.quality.empty_rows import EmptyRowsSheetProfile, evaluate_empty_rows


class EmptyRowsTests(unittest.TestCase):
    def test_profiles_only_internal_empty_blocks_and_excludes_boundaries(self):
        profile = profile_empty_rows([
            (None, None),
            ("inicial", 1),
            (None, "  "),
            (None, None),
            ("final", 2),
            (None, None),
        ])

        self.assertEqual(profile.non_empty_row_count, 2)
        self.assertEqual(profile.empty_row_count, 2)
        self.assertEqual(profile.empty_row_block_count, 1)
        self.assertEqual(profile.empty_row_ratio, 0.5)

    def test_does_not_treat_zero_false_dates_or_formulas_as_empty(self):
        profile = profile_empty_rows([
            (0, False),
            (None, None),
            (date(2026, 8, 20), "=SUM(A1:A2)"),
        ])

        self.assertEqual(profile.non_empty_row_count, 2)
        self.assertEqual(profile.empty_row_count, 1)
        self.assertEqual(profile.empty_row_block_count, 1)

    def test_emits_low_medium_and_high_severities_by_internal_ratio(self):
        scenarios = [
            (EmptyRowsProfile(non_empty_row_count=20, empty_row_count=1, empty_row_ratio=1 / 21, empty_row_block_count=1), "low", False),
            (EmptyRowsProfile(non_empty_row_count=19, empty_row_count=1, empty_row_ratio=0.05, empty_row_block_count=1), "medium", False),
            (EmptyRowsProfile(non_empty_row_count=3, empty_row_count=1, empty_row_ratio=0.25, empty_row_block_count=1), "high", True),
        ]

        for aggregate, severity, has_question in scenarios:
            with self.subTest(severity=severity):
                finding = evaluate_empty_rows(EmptyRowsSheetProfile(name="Aba 1", empty_rows=aggregate))[0]
                self.assertEqual(finding["rule_id"], "QLT-EMPTYROW-004")
                self.assertEqual(finding["severity"], severity)
                self.assertEqual(finding["question"] is not None, has_question)

    def test_excludes_profiles_without_internal_empty_rows_or_content(self):
        excluded_profiles = [
            EmptyRowsProfile(non_empty_row_count=2, empty_row_count=0, empty_row_ratio=0.0, empty_row_block_count=0),
            EmptyRowsProfile(non_empty_row_count=0, empty_row_count=0, empty_row_ratio=0.0, empty_row_block_count=0),
            EmptyRowsProfile(non_empty_row_count=1, empty_row_count=1, empty_row_ratio=0.5, empty_row_block_count=1),
        ]

        for aggregate in excluded_profiles:
            with self.subTest(aggregate=aggregate):
                self.assertEqual(evaluate_empty_rows(EmptyRowsSheetProfile(name="Aba 1", empty_rows=aggregate)), [])

    def test_adapts_to_canonical_contract_without_raw_values_or_positions(self):
        aggregate = EmptyRowsProfile(non_empty_row_count=3, empty_row_count=1, empty_row_ratio=0.25, empty_row_block_count=1)
        findings = evaluate_empty_rows(EmptyRowsSheetProfile(name="Aba Confidencial", empty_rows=aggregate))
        fragment = to_diagnosis_fragment(findings, sheet_id="sheet-1", column_id=None)

        contract_finding = fragment["findings"][0]
        self.assertEqual(contract_finding["rule_version"], "0.1.0-reconstructed.1")
        self.assertEqual(contract_finding["affected_entities"], [{"entity_type": "sheet", "entity_id": "sheet-1"}])
        serialized = str(fragment)
        self.assertNotIn("Aba Confidencial", serialized)
        self.assertNotIn("segredo", serialized)
        self.assertNotIn("cell_position", serialized)
        self.assertNotIn("row_number", serialized)

    def test_profile_keeps_only_aggregate_metrics(self):
        profile = profile_empty_rows([("segredo", 1), (None, None), ("resultado", 2)])

        self.assertNotIn("segredo", str(profile.__dict__))
        self.assertNotIn("resultado", str(profile.__dict__))


if __name__ == "__main__":
    unittest.main()
