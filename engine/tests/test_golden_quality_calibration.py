import json
import unittest
from pathlib import Path

from engine.calibration.evaluate_quality_draft_golden import REPORT_PATH, evaluate


class GoldenQualityCalibrationTests(unittest.TestCase):
    def test_golden_calibration_has_zero_known_deviation_and_preserves_production_block(self):
        report = evaluate()

        self.assertEqual(report["report_id"], "CAL-QUALITY-DRAFT-001")
        self.assertEqual(report["scenario_count"], 9)
        self.assertEqual(report["mismatch_count"], 0)
        self.assertEqual(report["decision"], "calibrated_for_draft")
        self.assertEqual(report["production_status"], "blocked")

        for rule_id in ("QLT-NUMTEXT-007", "QLT-NULL-001"):
            self.assertEqual(report["rules"][rule_id]["true_positive"], 4)
            self.assertEqual(report["rules"][rule_id]["false_positive"], 0)
            self.assertEqual(report["rules"][rule_id]["false_negative"], 0)

        self.assertTrue(any(not item["expected_signatures"] for item in report["scenarios"]))

    def test_persisted_report_matches_reproducible_evaluation(self):
        persisted = json.loads(Path(REPORT_PATH).read_text(encoding="utf-8"))
        self.assertEqual(persisted, evaluate())
