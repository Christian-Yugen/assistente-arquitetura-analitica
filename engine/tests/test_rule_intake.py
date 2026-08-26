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
            "executable_draft": 90,
            "reference_catalog_draft": 0,
            "intake_required": 5,
        })

        by_id = {rule["rule_id"]: rule for rule in readiness["rules"]}
        for rule_id in ("QLT-NULL-001", "QLT-DUP-002", "QLT-EMPTYCOL-003", "QLT-EMPTYROW-004", "QLT-MIXTYPE-005", "QLT-BADDATE-006", "QLT-NUMTEXT-007", "QLT-CATVAR-008", "QLT-WHITESPACE-009", "QLT-TOTALROW-010", "QLT-NEGATIVE-011", "QLT-OUTLIER-012", "QLT-FORMULA-013", "QLT-HEADERS-014", "QLT-IDMISS-015", "SEM-DATE-001", "SEM-COMP-002", "SEM-DESC-004", "SEM-DUR-008", "SEM-STATUS-009", "SEM-CAT-010", "SEM-LOC-011", "SEM-RESP-012", "SEM-ID-003", "SEM-QTY-005", "SEM-CURR-006", "SEM-PCT-007", "SEM-TARGET-013", "SEM-ACTUAL-014", "SEM-SENS-015", "GRN-COMP-001", "GRN-EXPL-002", "GRN-EVENT-004", "GRN-ENTITY-003", "MDL-FACTPER-001", "MDL-FACTTXN-002", "MDL-FACTNOGRAIN-019", "MDL-UNDEFINED-020", "MDL-DIMSTD-004", "MDL-DIMCAL-006", "REL-ONEMANY-001", "REL-NONUNIQ-002", "REL-ORPHAN-003", "REL-MANYMANY-004", "REL-FACTFACT-006", "REL-AMBIG-007", "REL-BIDIR-008", "REL-COMPKEY-009", "REL-CONFORMED-010", "MET-COMPL-001", "MET-SUM-002", "MET-COUNT-003", "MET-DCOUNT-004", "MET-AVG-005", "MET-MINMAX-006", "MET-RATE-007", "MET-ABSDELTA-008", "MET-PCTDELTA-009", "MET-RUNNING-010", "MET-WAVG-011", "MET-SEMIADD-012", "MET-DOMAIN-013"):
            self.assertEqual(by_id[rule_id]["local_readiness"], "executable_draft")
            self.assertTrue(by_id[rule_id]["executable"])
        self.assertEqual(by_id["MET-IMPOSS-014"]["local_readiness"], "executable_draft")
        self.assertTrue(by_id["MET-IMPOSS-014"]["executable"])
        self.assertEqual(by_id["MET-DAX-015"]["local_readiness"], "executable_draft")
        self.assertTrue(by_id["MET-DAX-015"]["executable"])
        self.assertEqual(by_id["ALT-SENS-001"]["local_readiness"], "executable_draft")
        self.assertTrue(by_id["ALT-SENS-001"]["executable"])
        self.assertEqual(by_id["ALT-QUALITY-002"]["local_readiness"], "executable_draft")
        self.assertTrue(by_id["ALT-QUALITY-002"]["executable"])
        self.assertEqual(by_id["ALT-GRAIN-003"]["local_readiness"], "executable_draft")
        self.assertTrue(by_id["ALT-GRAIN-003"]["executable"])
        self.assertEqual(by_id["ALT-KEY-004"]["local_readiness"], "executable_draft")
        self.assertTrue(by_id["ALT-KEY-004"]["executable"])
        self.assertEqual(by_id["ALT-AMBIG-005"]["local_readiness"], "executable_draft")
        self.assertTrue(by_id["ALT-AMBIG-005"]["executable"])
        self.assertEqual(by_id["ALT-LOWCONF-010"]["local_readiness"], "executable_draft")
        self.assertTrue(by_id["ALT-LOWCONF-010"]["executable"])
        self.assertEqual(by_id["GRN-SNAP-006"]["local_readiness"], "executable_draft")
        self.assertTrue(by_id["GRN-SNAP-006"]["executable"])
        self.assertEqual(by_id["GRN-PERIOD-005"]["local_readiness"], "executable_draft")
        self.assertTrue(by_id["GRN-PERIOD-005"]["executable"])
        self.assertEqual(by_id["GRN-ASSOC-007"]["local_readiness"], "executable_draft")
        self.assertTrue(by_id["GRN-ASSOC-007"]["executable"])
        self.assertEqual(by_id["GRN-PREAGG-008"]["local_readiness"], "executable_draft")
        self.assertTrue(by_id["GRN-PREAGG-008"]["executable"])
        self.assertEqual(by_id["GRN-INCONS-009"]["local_readiness"], "executable_draft")
        self.assertTrue(by_id["GRN-INCONS-009"]["executable"])
        self.assertEqual(by_id["GRN-DUP-010"]["local_readiness"], "executable_draft")
        self.assertTrue(by_id["GRN-DUP-010"]["executable"])
        self.assertEqual(by_id["MDL-FACTACC-003"]["local_readiness"], "executable_draft")
        self.assertTrue(by_id["MDL-FACTACC-003"]["executable"])
        self.assertEqual(by_id["MDL-DIMCONF-005"]["local_readiness"], "executable_draft")
        self.assertTrue(by_id["MDL-DIMCONF-005"]["executable"])
        self.assertEqual(by_id["MDL-DIMROLE-007"]["local_readiness"], "executable_draft")
        self.assertTrue(by_id["MDL-DIMROLE-007"]["executable"])
        self.assertEqual(by_id["MDL-DIMDEG-008"]["local_readiness"], "executable_draft")
        self.assertTrue(by_id["MDL-DIMDEG-008"]["executable"])
        self.assertEqual(by_id["MDL-BRIDGE-009"]["local_readiness"], "executable_draft")
        self.assertTrue(by_id["MDL-BRIDGE-009"]["executable"])
        self.assertEqual(by_id["MDL-AUX-010"]["local_readiness"], "executable_draft")
        self.assertTrue(by_id["MDL-AUX-010"]["executable"])
        self.assertEqual(by_id["MDL-PARAM-011"]["local_readiness"], "executable_draft")
        self.assertTrue(by_id["MDL-PARAM-011"]["executable"])
        self.assertEqual(by_id["MDL-FLAT-012"]["local_readiness"], "executable_draft")
        self.assertTrue(by_id["MDL-FLAT-012"]["executable"])
        self.assertEqual(by_id["MDL-MIXED-013"]["local_readiness"], "executable_draft")
        self.assertTrue(by_id["MDL-MIXED-013"]["executable"])
        self.assertEqual(by_id["MDL-ATTRREP-014"]["local_readiness"], "executable_draft")
        self.assertTrue(by_id["MDL-ATTRREP-014"]["executable"])
        self.assertEqual(by_id["ALT-METRIC-006"]["local_readiness"], "executable_draft")
        self.assertTrue(by_id["ALT-METRIC-006"]["executable"])
        self.assertEqual(by_id["ALT-SUMPCT-007"]["local_readiness"], "executable_draft")
        self.assertTrue(by_id["ALT-SUMPCT-007"]["executable"])
        self.assertEqual(by_id["ALT-AVGAVG-008"]["local_readiness"], "executable_draft")
        self.assertTrue(by_id["ALT-AVGAVG-008"]["executable"])
        self.assertEqual(by_id["ALT-MIXGRAIN-009"]["local_readiness"], "executable_draft")
        self.assertTrue(by_id["ALT-MIXGRAIN-009"]["executable"])

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

    def test_met_rate_intake_records_draft_only_authorization(self):
        intake = json.loads((PROJECT_ROOT / "artifacts/intake/MET-RATE-007.json").read_text(encoding="utf-8"))
        self.assertEqual(intake["local_readiness"], "executable_draft")
        self.assertTrue(intake["authorization"]["implementation_authorized"])
        self.assertEqual(intake["authorization"]["implementation_authorized_by"], "Chris")
        self.assertEqual(intake["authorization"]["required_gate"], "MET-RATE-007-DRAFT-CALIBRATION-001")
        self.assertFalse(intake["authorization"]["production_authorized"])
