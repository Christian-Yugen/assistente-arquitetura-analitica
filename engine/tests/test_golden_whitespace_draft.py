import unittest

from engine.calibration.evaluate_whitespace_draft_golden import evaluate


class GoldenWhitespaceDraftTests(unittest.TestCase):
    def test_all_scenarios_match_the_signed_golden_expectations(self):
        report = evaluate()

        self.assertEqual(report["metrics"], {"true_positive": 3, "false_positive": 0, "false_negative": 0})
        self.assertTrue(all(scenario["status"] == "pass" for scenario in report["scenarios"]))


if __name__ == "__main__":
    unittest.main()
