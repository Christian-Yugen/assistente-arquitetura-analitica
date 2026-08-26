import hashlib
import json
import unittest
from pathlib import Path

from engine.calibration.evaluate_mdl_aux_draft_golden import evaluate
from engine.contracts.diagnosis import RULE_VERSIONS
from engine.fact_dimension.auxiliary_table import AuxiliaryTableProfile, classify_auxiliary_table


GOLDEN_DIR = Path(__file__).resolve().parents[2] / "artifacts/golden"


class AuxiliaryTableTests(unittest.TestCase):
    def test_signal_and_guards(self):
        candidate = classify_auxiliary_table(AuxiliaryTableProfile(independent_auxiliary_table_signal_count=1))[0]
        self.assertEqual(candidate["rule_id"], "MDL-AUX-010")
        self.assertTrue(candidate["question"]["blocking"])
        profiles = (AuxiliaryTableProfile(), AuxiliaryTableProfile(independent_auxiliary_table_signal_count=1, confirmed_supporting_design_count=1), AuxiliaryTableProfile(independent_auxiliary_table_signal_count=1, structural_conflict_count=1), AuxiliaryTableProfile(independent_auxiliary_table_signal_count=1, sensitive_signal_count=1), AuxiliaryTableProfile(independent_auxiliary_table_signal_count=1, contract_error_count=1))
        for profile in profiles:
            self.assertEqual(classify_auxiliary_table(profile), [])

    def test_contract_and_golden(self):
        self.assertEqual(RULE_VERSIONS["MDL-AUX-010"], "0.1.0-provisional.1")
        manifest = json.loads((GOLDEN_DIR / "mdl-aux-draft-golden-v1.manifest.json").read_text())
        golden = GOLDEN_DIR / manifest["file"]
        self.assertEqual(hashlib.sha256(golden.read_bytes()).hexdigest(), manifest["sha256"])
        self.assertEqual(evaluate(), manifest["calibration"])
        self.assertFalse(manifest["production_authorized"])
