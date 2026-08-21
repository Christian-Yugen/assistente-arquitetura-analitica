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
            "baseline_reference": 0,
            "executable_draft": 12,
            "reference_catalog_draft": 6,
            "intake_required": 77,
        })

        by_id = {rule["rule_id"]: rule for rule in readiness["rules"]}
        for rule_id in ("QLT-NULL-001", "QLT-DUP-002", "QLT-EMPTYCOL-003", "QLT-EMPTYROW-004", "QLT-MIXTYPE-005", "QLT-BADDATE-006", "QLT-NUMTEXT-007", "QLT-CATVAR-008", "QLT-WHITESPACE-009", "QLT-TOTALROW-010", "QLT-NEGATIVE-011", "QLT-OUTLIER-012"):
            self.assertEqual(by_id[rule_id]["local_readiness"], "executable_draft")
            self.assertTrue(by_id[rule_id]["executable"])

    def test_catvar_intake_preserves_policy_gaps_after_provisional_draft_activation(self):
        intake = json.loads(
            (PROJECT_ROOT / "artifacts/intake/QLT-CATVAR-008.json").read_text(encoding="utf-8")
        )

        self.assertEqual(intake["rule"]["rule_id"], "QLT-CATVAR-008")
        self.assertEqual(intake["rule"]["title"], "Variações de categoria")
        self.assertEqual(intake["local_readiness"], "intake_required")
        self.assertFalse(intake["authorization"]["implementation_authorized"])
        self.assertEqual(intake["authorization"]["required_gate"], "QLT-CATVAR-008-AUTHORIZATION")
        self.assertIn("condition", intake["required_policy_elements"])
        self.assertEqual(get_rule_execution_record("QLT-CATVAR-008").status, "executable_draft")
