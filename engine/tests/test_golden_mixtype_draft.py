import json
import unittest
from pathlib import Path

from engine.profiling.mixed_types import MixedTypesProfile
from engine.quality.mixed_types import MixedTypesColumnProfile, evaluate_mixed_types


ROOT = Path(__file__).resolve().parents[2]
GOLDEN_PATH = ROOT / "artifacts/golden/mixtype-draft-golden-v1.json"


def signature(finding: dict[str, object]) -> dict[str, object]:
    return {
        "rule_id": finding["rule_id"],
        "severity": finding["severity"],
        "confidence": finding["confidence"],
        "question": finding["question"] is not None,
    }


class MixedTypesGoldenTests(unittest.TestCase):
    def test_golden_dataset_matches_expected_findings_without_identifiers_or_raw_values(self):
        golden = json.loads(GOLDEN_PATH.read_text(encoding="utf-8"))
        self.assertFalse(golden["privacy"]["contains_raw_workbook_values"])
        self.assertFalse(golden["privacy"]["contains_cell_positions"])
        self.assertFalse(golden["privacy"]["contains_sheet_titles"])
        self.assertFalse(golden["privacy"]["contains_column_names"])

        for scenario in golden["scenarios"]:
            profile = MixedTypesColumnProfile(
                name="Coluna Confidencial",
                mixed_types=MixedTypesProfile(**scenario["column"]["mixed_types"]),
            )
            actual = [signature(finding) for finding in evaluate_mixed_types(profile)]
            self.assertEqual(actual, scenario["expected_findings"], scenario["case_id"])
            self.assertNotIn("Coluna Confidencial", str(actual))


if __name__ == "__main__":
    unittest.main()
