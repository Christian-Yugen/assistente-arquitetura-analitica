import unittest

from engine.catalog import (
    RuleExecutionUnavailableError,
    category_caps,
    execute_registered_rule,
    executable_rule_count,
    get_rule_execution_record,
    load_official_catalog,
)
from engine.quality.numtext import CANONICAL_NUMERIC_TEXT_BASIS, NumericTextColumnProfile


class RuleCatalogTests(unittest.TestCase):
    def test_catalog_loads_the_complete_official_95_rule_source(self):
        catalog = load_official_catalog()
        self.assertEqual(len(catalog), 95)
        self.assertEqual(category_caps(), {"QLT": 15, "SEM": 15, "GRN": 10, "MDL": 20, "REL": 10, "MET": 15, "ALT": 10})
        self.assertEqual(catalog["QLT-CATVAR-008"]["title"], "Variações de categoria")
        self.assertEqual(catalog["ALT-LOWCONF-010"]["implementation_status"], "planned")

    def test_only_the_implemented_draft_rule_is_executable(self):
        profile = NumericTextColumnProfile("Valor", "text", 10, 8, 0.8, CANONICAL_NUMERIC_TEXT_BASIS)
        result = execute_registered_rule("QLT-NUMTEXT-007", profile)
        record = get_rule_execution_record("QLT-NUMTEXT-007")
        self.assertEqual(executable_rule_count(), 1)
        self.assertEqual(result[0]["rule_id"], "QLT-NUMTEXT-007")
        self.assertEqual(record.status, "executable_draft")
        self.assertEqual(record.title, "Números armazenados como texto")

    def test_baseline_reference_and_reserved_official_slots_cannot_execute(self):
        expected_statuses = {
            "QLT-BADDATE-006": "baseline_reference",
            "SEM-DATE-001": "reference_catalog_draft",
            "GRN-COMP-001": "reference_catalog_draft",
            "MDL-FACTPER-001": "reference_catalog_draft",
            "REL-ONEMANY-001": "reference_catalog_draft",
            "MET-COMPL-001": "reference_catalog_draft",
            "ALT-SENS-001": "reference_catalog_draft",
            "QLT-CATVAR-008": "reserved_definition",
            "MDL-UNDEFINED-020": "reserved_definition",
            "MET-DAX-015": "reserved_definition",
        }
        for rule_id, expected_status in expected_statuses.items():
            self.assertEqual(get_rule_execution_record(rule_id).status, expected_status, rule_id)
            with self.assertRaises(RuleExecutionUnavailableError, msg=rule_id):
                execute_registered_rule(rule_id, object())
        self.assertEqual(get_rule_execution_record("MDL-021").status, "unknown")
