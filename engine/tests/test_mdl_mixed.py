import hashlib
import json
import unittest
from pathlib import Path

from engine.calibration.evaluate_mdl_mixed_draft_golden import evaluate
from engine.contracts.diagnosis import RULE_VERSIONS
from engine.fact_dimension.mixed_table import MixedTableProfile, classify_mixed_table


GOLDEN_DIR = Path(__file__).resolve().parents[2] / "artifacts/golden"


class MixedTableTests(unittest.TestCase):
    def test_signal_and_guards(self):
        candidate = classify_mixed_table(MixedTableProfile(independent_mixed_table_signal_count=1))[0]
        self.assertEqual(candidate["rule_id"], "MDL-MIXED-013")
        self.assertTrue(candidate["question"]["blocking"])
        profiles = (MixedTableProfile(), MixedTableProfile(independent_mixed_table_signal_count=1, confirmed_decomposition_design_count=1), MixedTableProfile(independent_mixed_table_signal_count=1, structural_conflict_count=1), MixedTableProfile(independent_mixed_table_signal_count=1, sensitive_signal_count=1), MixedTableProfile(independent_mixed_table_signal_count=1, contract_error_count=1))
        for profile in profiles:
            self.assertEqual(classify_mixed_table(profile), [])

    def test_contract_and_golden(self):
        self.assertEqual(RULE_VERSIONS["MDL-MIXED-013"], "0.1.0-provisional.1")
        manifest = json.loads((GOLDEN_DIR / "mdl-mixed-draft-golden-v1.manifest.json").read_text())
        golden = GOLDEN_DIR / manifest["file"]
        self.assertEqual(hashlib.sha256(golden.read_bytes()).hexdigest(), manifest["sha256"])
        self.assertEqual(evaluate(), manifest["calibration"])
        self.assertFalse(manifest["production_authorized"])
