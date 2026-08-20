import json
import unittest
from pathlib import Path

from engine.profiling.bad_dates import BadDateProfile
from engine.quality.bad_dates import BadDateColumnProfile, evaluate_bad_dates


ROOT = Path(__file__).resolve().parents[2]
GOLDEN_PATH = ROOT / "artifacts/golden/baddate-draft-golden-v1.json"


def signature(finding: dict[str, object]) -> dict[str, object]:
    return {
        "rule_id": finding["rule_id"],
        "severity": finding["severity"],
        "confidence": finding["confidence"],
        "question": finding["question"] is not None,
    }


class GoldenBadDateDraftTests(unittest.TestCase):
    def test_golden_dataset_is_aggregate_only_and_regression_is_exact(self):
        golden = json.loads(GOLDEN_PATH.read_text(encoding="utf-8"))
        self.assertEqual(golden["dataset_id"], "GD-QLT-BADDATE-006-001")
        self.assertFalse(golden["privacy"]["contains_raw_workbook_values"])
        self.assertFalse(golden["privacy"]["contains_cell_positions"])
        self.assertFalse(golden["privacy"]["contains_sheet_titles"])
        self.assertFalse(golden["privacy"]["contains_column_names"])

        for scenario in golden["scenarios"]:
            profile = BadDateColumnProfile(name="Campo Privado", bad_dates=BadDateProfile(**scenario["column"]["bad_dates"]))
            actual = [signature(finding) for finding in evaluate_bad_dates(profile)]
            self.assertEqual(actual, scenario["expected_findings"], scenario["case_id"])


if __name__ == "__main__":
    unittest.main()
