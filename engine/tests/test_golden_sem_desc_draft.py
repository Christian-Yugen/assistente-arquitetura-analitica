import unittest

from engine.calibration.evaluate_sem_desc_draft_golden import evaluate


class SemanticDescriptionGoldenTests(unittest.TestCase):
    def test_golden_dataset_calibrates_without_false_positive_or_false_negative(self):
        self.assertEqual(evaluate(), {"tp": 3, "fp": 0, "fn": 0})
