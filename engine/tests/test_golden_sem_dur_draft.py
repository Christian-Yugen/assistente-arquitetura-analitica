import unittest

from engine.calibration.evaluate_sem_dur_draft_golden import evaluate


class SemanticDurationGoldenTests(unittest.TestCase):
    def test_golden_dataset_is_calibrated_without_false_positives_or_false_negatives(self):
        self.assertEqual(evaluate(), {"tp": 3, "fp": 0, "fn": 0})
