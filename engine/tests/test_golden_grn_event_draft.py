from __future__ import annotations

import unittest

from engine.calibration.evaluate_grn_event_draft_golden import evaluate


class EventPerRowGoldenCalibrationTests(unittest.TestCase):
    def test_golden_dataset_has_no_false_positives_or_false_negatives(self) -> None:
        self.assertEqual(
            evaluate(),
            {"true_positives": 3, "false_positives": 0, "false_negatives": 0},
        )
