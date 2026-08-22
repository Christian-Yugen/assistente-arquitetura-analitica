import unittest

from engine.calibration.evaluate_sem_resp_draft_golden import evaluate


class GoldenSemanticResponsibleTests(unittest.TestCase):
    def test_draft_golden_metrics_are_calibrated(self):
        self.assertEqual(evaluate(), {"tp": 3, "fp": 0, "fn": 0})
