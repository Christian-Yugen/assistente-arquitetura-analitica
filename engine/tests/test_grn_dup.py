import hashlib,json,unittest
from pathlib import Path
from engine.alerts.duplicate_grain import DuplicateGrainProfile,classify_duplicate_grain
from engine.calibration.evaluate_grn_dup_draft_golden import evaluate
from engine.contracts.diagnosis import RULE_VERSIONS,to_diagnosis_fragment
GOLDEN_DIR=Path(__file__).resolve().parents[2]/"artifacts/golden"
class DuplicateGrainTests(unittest.TestCase):
 def test_signal_and_guards(self):
  finding=classify_duplicate_grain(DuplicateGrainProfile(independent_duplicate_grain_signal_count=1)); self.assertEqual(finding["rule_id"],"GRN-DUP-010"); self.assertTrue(finding["question"]["blocking"])
  for p in (DuplicateGrainProfile(),DuplicateGrainProfile(independent_duplicate_grain_signal_count=1,confirmed_duplicate_resolution_count=1),DuplicateGrainProfile(independent_duplicate_grain_signal_count=1,structural_conflict_count=1),DuplicateGrainProfile(independent_duplicate_grain_signal_count=1,sensitive_signal_count=1),DuplicateGrainProfile(independent_duplicate_grain_signal_count=1,contract_error_count=1)): self.assertIsNone(classify_duplicate_grain(p))
 def test_contract_and_golden(self):
  f=classify_duplicate_grain(DuplicateGrainProfile(independent_duplicate_grain_signal_count=2)); frag=to_diagnosis_fragment([f],sheet_id="opaque",column_id=None); self.assertEqual(RULE_VERSIONS["GRN-DUP-010"],"0.1.0-provisional.1"); self.assertEqual(frag["findings"][0]["evidence"][0]["observed"],{"observed_value":2})
  manifest=json.loads((GOLDEN_DIR/"grn-dup-draft-golden-v1.manifest.json").read_text()); path=GOLDEN_DIR/manifest["file"]; self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(),manifest["sha256"]); self.assertEqual(evaluate(),manifest["calibration"]); self.assertFalse(manifest["production_authorized"])
