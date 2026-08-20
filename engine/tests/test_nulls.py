import json
import unittest
from pathlib import Path

from engine.profiling.missingness import MissingnessProfile
from engine.quality.nulls import RULE_ID, RULE_VERSION, NullColumnProfile, evaluate_nulls
from engine.quality.registry import QUALITY_RULE_IMPLEMENTATIONS


BASELINE_PATH = Path(__file__).resolve().parents[2] / "artifacts/baselines/qlt-null-001-v0.1.0-reconstructed.1-baseline.json"


class NullRuleTests(unittest.TestCase):
    def test_matches_every_preimplementation_baseline_outcome(self):
        baseline = json.loads(BASELINE_PATH.read_text(encoding="utf-8"))
        for case in baseline["profiles"]:
            profile = case["profile"]
            finding = evaluate_nulls(
                NullColumnProfile(
                    name="Campo",
                    physical_type="text",
                    missingness=MissingnessProfile(**profile),
                )
            )
            expected = case["expected"]
            self.assertEqual(bool(finding), expected["finding"], case["case_id"])
            if finding:
                self.assertEqual(finding[0]["severity"], expected["severity"], case["case_id"])
                self.assertEqual(finding[0]["confidence"], expected["confidence"], case["case_id"])
                self.assertEqual(bool(finding[0]["question"]), expected["question"], case["case_id"])
                self.assertTrue(all("raw_value" not in evidence for evidence in finding[0]["evidence"]))

    def test_registers_the_reconstructed_rule_with_its_governed_identity(self):
        self.assertIs(QUALITY_RULE_IMPLEMENTATIONS[RULE_ID], evaluate_nulls)
        self.assertEqual(RULE_VERSION, "0.1.0-reconstructed.1")


if __name__ == "__main__":
    unittest.main()
