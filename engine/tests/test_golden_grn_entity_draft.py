import unittest

from engine.calibration.evaluate_grn_entity_draft_golden import evaluate


class GoldenEntityDraftTests(unittest.TestCase):
    def test_golden_calibration_matches_approved_baseline(self) -> None:
        self.assertEqual(
            evaluate(),
            {"true_positives": 3, "false_positives": 0, "false_negatives": 0},
        )
