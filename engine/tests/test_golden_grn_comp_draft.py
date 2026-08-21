from __future__ import annotations

import unittest
from pathlib import Path

from engine.calibration.evaluate_grn_comp_draft_golden import evaluate


class GoldenCompositeGrainTests(unittest.TestCase):
    def test_calibration_has_no_false_positives_or_false_negatives(self) -> None:
        result = evaluate(Path("artifacts/golden/grn-comp-draft-golden-v1.json"))
        self.assertEqual(result, {"true_positives": 1, "false_positives": 0, "false_negatives": 0})
