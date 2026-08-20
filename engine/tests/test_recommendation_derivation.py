from __future__ import annotations

import unittest

from engine.pipeline.quality_diagnosis import build_column_analysis_context, execute_quality_diagnosis
from engine.tests.test_numtext_pipeline import METADATA


class RecommendationDerivationTests(unittest.TestCase):
    def test_draft_pipeline_preserves_rule_derived_recommendations_and_keeps_partial_markers_separate(self):
        numeric_text_column = build_column_analysis_context(
            sheet_id="11111111-1111-4111-8111-111111111111",
            column_id="22222222-2222-4222-8222-222222222222",
            column_name="codigo",
            values=["100", "200", "300", "400"],
            sheet_name="Aba 1",
            sheet_position=1,
            sheet_visibility="visible",
            column_position=1,
        )
        nullable_column = build_column_analysis_context(
            sheet_id="11111111-1111-4111-8111-111111111111",
            column_id="33333333-3333-4333-8333-333333333333",
            column_name="observacao",
            values=[None, "", float("nan"), "ok", None],
            sheet_name="Aba 1",
            sheet_position=1,
            sheet_visibility="visible",
            column_position=2,
        )

        diagnosis = execute_quality_diagnosis([numeric_text_column, nullable_column], metadata=METADATA)
        recommendations_by_rule = {finding["rule_id"]: finding["recommendation"] for finding in diagnosis["findings"]}

        self.assertIn("QLT-NUMTEXT-007", recommendations_by_rule)
        self.assertIn("QLT-NULL-001", recommendations_by_rule)
        self.assertIn("converter", recommendations_by_rule["QLT-NUMTEXT-007"].lower())
        self.assertIn("ausência", recommendations_by_rule["QLT-NULL-001"].lower())
        self.assertEqual(diagnosis["proposed_model"]["status"], "insufficient")
        self.assertNotEqual(diagnosis["summary"]["next_recommended_action"], recommendations_by_rule["QLT-NUMTEXT-007"])
