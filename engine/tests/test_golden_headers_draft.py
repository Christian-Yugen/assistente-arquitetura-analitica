import hashlib
import json
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
GOLDEN_PATH = PROJECT_ROOT / "artifacts/golden/headers-draft-golden-v1.json"
MANIFEST_PATH = PROJECT_ROOT / "artifacts/golden/headers-draft-golden-v1.manifest.json"


class HeadersGoldenDatasetTests(unittest.TestCase):
    def test_manifest_matches_immutable_golden_dataset(self):
        manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
        digest = hashlib.sha256(GOLDEN_PATH.read_bytes()).hexdigest()
        self.assertEqual(manifest["dataset_id"], "GD-QLT-HEADERS-014-001")
        self.assertEqual(manifest["sha256"], digest)

    def test_golden_dataset_contains_only_aggregate_private_profiles(self):
        golden = json.loads(GOLDEN_PATH.read_text(encoding="utf-8"))
        self.assertEqual(golden["privacy"], {
            "contains_raw_cell_values": False,
            "contains_header_texts": False,
            "contains_sheet_titles": False,
            "contains_positions": False,
            "contains_ranges": False,
        })
        for scenario in golden["scenarios"]:
            self.assertEqual(set(scenario["profile"]), {
                "header_column_count",
                "missing_header_count",
                "duplicate_normalized_group_count",
                "duplicate_header_count",
                "multilevel_candidate_count",
            })
