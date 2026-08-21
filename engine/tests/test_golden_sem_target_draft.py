import unittest

from engine.calibration.evaluate_sem_target_draft_golden import evaluate


class SemanticTargetGoldenTests(unittest.TestCase):
    def test_golden_calibration_has_only_true_positives(self):
        self.assertEqual(evaluate(), {"tp": 3, "fp": 0, "fn": 0})
