import hashlib
import json
import unittest
from pathlib import Path

from engine.contracts.diagnosis import to_diagnosis_fragment
from engine.profiling.identifier_completeness import IdentifierCompletenessProfile
from engine.quality.identifier_completeness import IdentifierCompletenessColumnProfile, evaluate_identifier_completeness


PROJECT_ROOT = Path(__file__).resolve().parents[2]
GOLDEN_PATH = PROJECT_ROOT / "artifacts/golden/idmiss-draft-golden-v1.json"
MANIFEST_PATH = PROJECT_ROOT / "artifacts/golden/idmiss-draft-golden-v1.manifest.json"


class GoldenIdentifierCompletenessTests(unittest.TestCase):
    def test_manifest_and_golden_dataset_are_private_and_stable(self):
        golden_bytes = GOLDEN_PATH.read_bytes()
        golden = json.loads(golden_bytes)
        manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))

        self.assertEqual(manifest["dataset_id"], "GD-QLT-IDMISS-015-001")
        self.assertEqual(manifest["sha256"], hashlib.sha256(golden_bytes).hexdigest())
        self.assertFalse(golden["privacy"]["contains_raw_identifiers"])
        self.assertFalse(golden["privacy"]["contains_headers"])

    def test_golden_scenarios_match_expected_findings_without_raw_output(self):
        golden = json.loads(GOLDEN_PATH.read_text(encoding="utf-8"))
        for scenario in golden["scenarios"]:
            findings = evaluate_identifier_completeness(IdentifierCompletenessColumnProfile("Field", IdentifierCompletenessProfile(**scenario["profile"])))
            reduced = [{"rule_id": finding["rule_id"], "severity": finding["severity"], "question": finding["question"] is not None} for finding in findings]
            self.assertEqual(reduced, scenario["expected_findings"], scenario["scenario_id"])

        fragment = to_diagnosis_fragment(
            evaluate_identifier_completeness(IdentifierCompletenessColumnProfile("Field", IdentifierCompletenessProfile(True, 20, 1, 19, 1, 2, 0.05, 0.1))),
            sheet_id="sheet-x",
            column_id="column-y",
        )
        serialized = json.dumps(fragment, ensure_ascii=False)
        self.assertNotIn("raw_identifier", serialized)
        self.assertNotIn("example_value", serialized)
