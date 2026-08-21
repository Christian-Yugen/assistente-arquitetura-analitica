import json
import unittest
from hashlib import sha256
from pathlib import Path

from engine.contracts.diagnosis import to_diagnosis_fragment
from engine.profiling.duplicate_rows import DuplicateRowsProfile
from engine.quality.duplicates import DuplicateRowsSheetProfile, evaluate_duplicate_rows


ROOT = Path(__file__).resolve().parents[2]
GOLDEN_PATH = ROOT / "artifacts/golden/dup-draft-golden-v1.json"
MANIFEST_PATH = ROOT / "artifacts/golden/dup-draft-golden-v1.manifest.json"


class GoldenDuplicateRowsTests(unittest.TestCase):
    def test_all_aggregate_cases_match_expected_findings_and_preserve_privacy(self):
        golden = json.loads(GOLDEN_PATH.read_text(encoding="utf-8"))
        manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))

        self.assertEqual(golden["dataset_id"], "GD-QLT-DUP-002-001")
        self.assertEqual(manifest["dataset_id"], golden["dataset_id"])
        self.assertEqual(manifest["sha256"], sha256(GOLDEN_PATH.read_bytes()).hexdigest())
        self.assertFalse(golden["privacy"]["contains_raw_workbook_values"])
        self.assertFalse(golden["privacy"]["contains_row_signatures"])
        self.assertFalse(golden["privacy"]["contains_row_indices"])

        for scenario in golden["scenarios"]:
            sheet = scenario["sheet"]
            profile = DuplicateRowsSheetProfile(
                name="Aba 1",
                duplicates=DuplicateRowsProfile(**sheet["duplicates"]),
            )
            findings = evaluate_duplicate_rows(profile)
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
            fragment = to_diagnosis_fragment(findings, sheet_id="sheet-1", column_id="column-1")
            serialized = json.dumps(fragment)
            self.assertNotIn("raw_value", serialized)
            self.assertNotIn("row_signature", serialized)
            self.assertNotIn("row_index", serialized)
            self.assertNotIn("sensitive_example", serialized)


if __name__ == "__main__":
    unittest.main()
