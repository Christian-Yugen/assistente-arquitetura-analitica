import unittest
import hashlib
import json
from pathlib import Path

from engine.alerts.snapshot_grain import SnapshotGrainProfile, classify_snapshot_grain
from engine.contracts.diagnosis import RULE_VERSIONS, to_diagnosis_fragment


GOLDEN_DIR = Path(__file__).resolve().parents[2] / "artifacts" / "golden"

class SnapshotGrainTests(unittest.TestCase):
    def test_emits_only_for_independent_aggregate_signal(self):
        finding = classify_snapshot_grain(SnapshotGrainProfile(independent_snapshot_signal_count=1))
        self.assertEqual(finding["rule_id"], "GRN-SNAP-006")
        self.assertTrue(finding["question"]["blocking"])

    def test_blocks_missing_signal_confirmation_conflict_sensitivity_and_contract_error(self):
        for profile in (SnapshotGrainProfile(), SnapshotGrainProfile(independent_snapshot_signal_count=1, confirmed_snapshot_grain_count=1), SnapshotGrainProfile(independent_snapshot_signal_count=1, structural_conflict_count=1), SnapshotGrainProfile(independent_snapshot_signal_count=1, sensitive_signal_count=1), SnapshotGrainProfile(independent_snapshot_signal_count=1, contract_error_count=1)):
            self.assertIsNone(classify_snapshot_grain(profile))

    def test_projects_only_aggregate_snapshot_finding_with_registered_version(self):
        finding = classify_snapshot_grain(SnapshotGrainProfile(independent_snapshot_signal_count=2))
        self.assertEqual(RULE_VERSIONS["GRN-SNAP-006"], "0.1.0-provisional.1")

        fragment = to_diagnosis_fragment([finding], sheet_id="opaque-sheet", column_id=None)

        self.assertEqual(fragment["findings"][0]["rule_id"], "GRN-SNAP-006")
        self.assertEqual(fragment["findings"][0]["rule_version"], "0.1.0-provisional.1")
        self.assertEqual(fragment["findings"][0]["evidence"][0]["observed"], {"observed_value": 2})

    def test_synthetic_golden_hash_calibration_and_fail_closed_cases(self):
        manifest = json.loads((GOLDEN_DIR / "grn-snap-draft-golden-v1.manifest.json").read_text(encoding="utf-8"))
        golden_path = GOLDEN_DIR / manifest["file"]
        golden = json.loads(golden_path.read_text(encoding="utf-8"))

        self.assertTrue(manifest["synthetic_only"])
        self.assertFalse(manifest["production_authorized"])
        self.assertEqual(manifest["calibration"], {"tp": 1, "fp": 0, "fn": 0})
        self.assertEqual(hashlib.sha256(golden_path.read_bytes()).hexdigest(), manifest["sha256"])

        for case in golden["cases"]:
            profile = SnapshotGrainProfile(**(golden["profile_defaults"] | case["overrides"]))
            self.assertEqual(classify_snapshot_grain(profile) is not None, case["expected_finding"])
