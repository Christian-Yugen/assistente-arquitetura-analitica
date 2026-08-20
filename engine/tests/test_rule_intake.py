import json
import unittest
from pathlib import Path

from engine.catalog import get_rule_execution_record


PROJECT_ROOT = Path(__file__).resolve().parents[2]


class RuleIntakeTests(unittest.TestCase):
    def test_readiness_index_accounts_for_every_official_rule(self):
        readiness = json.loads(
            (PROJECT_ROOT / "artifacts/catalogs/rule-implementation-readiness-v1.json").read_text(encoding="utf-8")
        )

        self.assertEqual(readiness["source_blueprint"]["blueprint_id"], "PM-MVP-PBI-RULE-BP-001")
        self.assertEqual(len(readiness["rules"]), 95)
        self.assertEqual(readiness["counts"], {
            "baseline_reference": 6,
            "executable_draft": 1,
            "reference_catalog_draft": 6,
            "intake_required": 82,
        })

    def test_catvar_intake_preserves_policy_gaps_and_blocks_execution(self):
        intake = json.loads(
            (PROJECT_ROOT / "artifacts/intake/QLT-CATVAR-008.json").read_text(encoding="utf-8")
        )

        self.assertEqual(intake["rule"]["rule_id"], "QLT-CATVAR-008")
        self.assertEqual(intake["rule"]["title"], "Variações de categoria")
        self.assertEqual(intake["local_readiness"], "intake_required")
        self.assertFalse(intake["authorization"]["implementation_authorized"])
        self.assertEqual(intake["authorization"]["required_gate"], "QLT-CATVAR-008-AUTHORIZATION")
        self.assertIn("condition", intake["required_policy_elements"])
        self.assertEqual(get_rule_execution_record("QLT-CATVAR-008").status, "reserved_definition")
