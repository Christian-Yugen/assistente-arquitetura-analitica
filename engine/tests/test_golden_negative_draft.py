import json
import unittest
from hashlib import sha256
from pathlib import Path

from engine.contracts.diagnosis import to_diagnosis_fragment
from engine.profiling.negative_values import NegativeValuesProfile
from engine.quality.negative_values import NegativeValuesColumnProfile, evaluate_negative_values


ROOT = Path(__file__).resolve().parents[2]
GOLDEN_PATH = ROOT / "artifacts/golden/negative-draft-golden-v1.json"
MANIFEST_PATH = ROOT / "artifacts/golden/negative-draft-golden-v1.manifest.json"


class GoldenNegativeValuesTests(unittest.TestCase):
    def test_all_aggregate_cases_match_expected_findings_and_preserve_privacy(self):
        golden = json.loads(GOLDEN_PATH.read_text(encoding="utf-8"))
        manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))

        self.assertEqual(golden["dataset_id"], "GD-QLT-NEGATIVE-011-001")
        self.assertEqual(manifest["dataset_id"], golden["dataset_id"])
        self.assertEqual(manifest["sha256"], sha256(GOLDEN_PATH.read_bytes()).hexdigest())
        self.assertFalse(golden["privacy"]["contains_raw_workbook_values"])
        self.assertFalse(golden["privacy"]["contains_cell_positions"])
        self.assertFalse(golden["privacy"]["contains_column_headers"])
        self.assertFalse(golden["privacy"]["contains_sheet_titles"])

        for scenario in golden["scenarios"]:
            profile = NegativeValuesColumnProfile(
                name="Coluna Confidencial",
                negative_values=NegativeValuesProfile(**scenario["column"]["negative_values"]),
            )
            findings = evaluate_negative_values(profile)
            observed = [
                {
                    "rule_id": finding["rule_id"],
                    "severity": finding["severity"],
                    "confidence": finding["confidence"],
                    "question": finding["question"] is not None,
                }
                for finding in findings
            ]
            self.assertCountEqual(observed, scenario["expected_findings"], msg=scenario["case_id"])
            serialized = json.dumps(to_diagnosis_fragment(findings, sheet_id="sheet-1", column_id="column-1"))
            self.assertNotIn("raw_value", serialized)
            self.assertNotIn("cell_position", serialized)
            self.assertNotIn("sensitive_example", serialized)
            self.assertNotIn("Coluna Confidencial", serialized)


if __name__ == "__main__":
    unittest.main()
