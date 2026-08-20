import json
import unittest
from pathlib import Path

from engine.contracts.diagnosis import to_diagnosis_fragment
from engine.quality.numtext import (
    CANONICAL_NUMERIC_TEXT_BASIS,
    NumericTextColumnProfile,
    evaluate_numeric_text,
)


PROJECT_ROOT = Path(__file__).resolve().parents[2]


class NumericTextIntegrationAndRegressionTests(unittest.TestCase):
    def test_mixed_type_input_is_supplemental_and_respects_ruleset_precedence(self):
        ruleset = json.loads(
            (PROJECT_ROOT / "artifacts/rulesets/quality-ruleset-v0.7.0.json").read_text(encoding="utf-8")
        )
        profile = NumericTextColumnProfile(
            name="Quantidade",
            physical_type="mixed",
            non_empty_value_count=100,
            numeric_text_candidate_count=60,
            numeric_text_candidate_ratio=0.6,
            numeric_text_basis=CANONICAL_NUMERIC_TEXT_BASIS,
        )

        finding = evaluate_numeric_text(profile)[0]
        numtext_position = ruleset["execution_order"].index("QLT-NUMTEXT-007")
        mixtype_position = ruleset["execution_order"].index("QLT-MIXTYPE-005")

        self.assertGreater(numtext_position, mixtype_position)
        self.assertEqual(finding["severity"], "high")
        self.assertEqual(finding["rule_id"], "QLT-NUMTEXT-007")
        self.assertTrue(finding["question"])

    def test_no_numeric_text_candidates_do_not_change_canonical_fragment(self):
        profile = NumericTextColumnProfile(
            name="Descrição",
            physical_type="text",
            non_empty_value_count=30,
            numeric_text_candidate_count=0,
            numeric_text_candidate_ratio=0.0,
            numeric_text_basis=CANONICAL_NUMERIC_TEXT_BASIS,
        )

        fragment = to_diagnosis_fragment(
            evaluate_numeric_text(profile), sheet_id="sheet-regression", column_id="column-regression"
        )

        self.assertEqual(fragment["findings"], [])
        self.assertEqual(fragment["questions"], [])
        self.assertEqual(fragment["schema_version"], "1.0.0")
