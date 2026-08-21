import unittest

from engine.contracts.diagnosis import to_diagnosis_fragment
from engine.profiling.total_rows import TotalRowsProfile, profile_total_rows
from engine.quality.total_rows import TotalRowsSheetProfile, evaluate_total_rows


class TotalRowsTests(unittest.TestCase):
    def test_profiles_only_authorized_labels_after_three_non_empty_rows_with_numeric_peer(self):
        profile = profile_total_rows([
            ("registro", 12),
            ("registro", 14),
            ("registro", 16),
            (" Total Geral ", 42),
            ("Subtotal", 7),
            ("total", "=SUM(B1:B5)"),
        ])

        self.assertEqual(profile.non_empty_row_count, 6)
        self.assertEqual(profile.total_row_candidate_count, 2)
        self.assertEqual(profile.total_row_candidate_ratio, round(2 / 6, 8))

    def test_excludes_short_prefix_partial_labels_formula_only_peers_and_non_portuguese_labels(self):
        profile = profile_total_rows([
            ("total", 3),
            ("registro", 4),
            ("registro", 5),
            ("total mensal", 9),
            ("TOTAL", "=SUM(B1:B4)"),
            ("grand total", 21),
        ])

        self.assertEqual(profile.non_empty_row_count, 6)
        self.assertEqual(profile.total_row_candidate_count, 0)

    def test_emits_low_medium_and_high_severities_by_candidate_ratio(self):
        scenarios = [
            (TotalRowsProfile(non_empty_row_count=20, total_row_candidate_count=1, total_row_candidate_ratio=0.05), "low", False),
            (TotalRowsProfile(non_empty_row_count=10, total_row_candidate_count=1, total_row_candidate_ratio=0.10), "medium", True),
            (TotalRowsProfile(non_empty_row_count=5, total_row_candidate_count=2, total_row_candidate_ratio=0.40), "high", True),
        ]

        for aggregate, severity, has_question in scenarios:
            with self.subTest(severity=severity):
                finding = evaluate_total_rows(TotalRowsSheetProfile(name="Aba 1", total_rows=aggregate))[0]
                self.assertEqual(finding["rule_id"], "QLT-TOTALROW-010")
                self.assertEqual(finding["severity"], severity)
                self.assertEqual(finding["question"] is not None, has_question)

    def test_excludes_profiles_without_candidates_insufficient_rows_or_unknown_basis(self):
        excluded_profiles = [
            TotalRowsProfile(non_empty_row_count=6, total_row_candidate_count=0, total_row_candidate_ratio=0.0),
            TotalRowsProfile(non_empty_row_count=3, total_row_candidate_count=1, total_row_candidate_ratio=1 / 3),
            TotalRowsProfile(non_empty_row_count=6, total_row_candidate_count=1, total_row_candidate_ratio=1 / 6, normalization_basis="unapproved"),
        ]

        for aggregate in excluded_profiles:
            with self.subTest(aggregate=aggregate):
                self.assertEqual(evaluate_total_rows(TotalRowsSheetProfile(name="Aba 1", total_rows=aggregate)), [])

    def test_adapts_to_canonical_contract_without_raw_values_or_positions(self):
        aggregate = TotalRowsProfile(non_empty_row_count=4, total_row_candidate_count=1, total_row_candidate_ratio=0.25)
        findings = evaluate_total_rows(TotalRowsSheetProfile(name="Aba Confidencial", total_rows=aggregate))
        fragment = to_diagnosis_fragment(findings, sheet_id="sheet-1", column_id=None)

        contract_finding = fragment["findings"][0]
        self.assertEqual(contract_finding["rule_version"], "0.1.0-provisional.1")
        self.assertEqual(contract_finding["affected_entities"], [{"entity_type": "sheet", "entity_id": "sheet-1"}])
        serialized = str(fragment)
        self.assertNotIn("Aba Confidencial", serialized)
        self.assertNotIn("Total Geral", serialized)
        self.assertNotIn("formula", serialized)
        self.assertNotIn("row_number", serialized)

    def test_profile_keeps_only_aggregate_metrics(self):
        profile = profile_total_rows([("segredo", 4), ("segredo", 5), ("segredo", 6), ("Total Geral", 15)])

        self.assertNotIn("segredo", str(profile.__dict__))
        self.assertNotIn("Total Geral", str(profile.__dict__))


if __name__ == "__main__":
    unittest.main()
