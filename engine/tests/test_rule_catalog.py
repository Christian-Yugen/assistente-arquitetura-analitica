import unittest
from unittest.mock import patch

from engine.catalog import (
    DRAFT_RULE_AUTHORIZATIONS,
    RuleExecutionUnavailableError,
    category_caps,
    execute_registered_rule,
    executable_rule_count,
    get_rule_execution_record,
    load_official_catalog,
)
from engine.quality.numtext import CANONICAL_NUMERIC_TEXT_BASIS, NumericTextColumnProfile
from engine.profiling.missingness import MissingnessProfile
from engine.profiling.categorical_variations import profile_categorical_variations
from engine.quality.catvar import CategoricalVariationColumnProfile
from engine.quality.nulls import NullColumnProfile
from engine.profiling.duplicate_rows import DuplicateRowsProfile
from engine.quality.duplicates import DuplicateRowsSheetProfile
from engine.quality.registry import QUALITY_RULE_IMPLEMENTATIONS


class RuleCatalogTests(unittest.TestCase):
    def test_catalog_loads_the_complete_official_95_rule_source(self):
        catalog = load_official_catalog()
        self.assertEqual(len(catalog), 95)
        self.assertEqual(category_caps(), {"QLT": 15, "SEM": 15, "GRN": 10, "MDL": 20, "REL": 10, "MET": 15, "ALT": 10})
        self.assertEqual(catalog["QLT-CATVAR-008"]["title"], "Variações de categoria")
        self.assertEqual(catalog["ALT-LOWCONF-010"]["implementation_status"], "planned")

    def test_only_the_authorized_draft_rules_are_executable(self):
        profile = NumericTextColumnProfile("Valor", "text", 10, 8, 0.8, CANONICAL_NUMERIC_TEXT_BASIS)
        result = execute_registered_rule("QLT-NUMTEXT-007", profile)
        null_result = execute_registered_rule(
            "QLT-NULL-001",
            NullColumnProfile("Observação", "text", MissingnessProfile(20, 16, 4, 0, 0)),
        )
        catvar_result = execute_registered_rule(
            "QLT-CATVAR-008",
            CategoricalVariationColumnProfile("Região", "text", profile_categorical_variations(["Norte", "norte", "Sul"])),
        )
        duplicate_result = execute_registered_rule(
            "QLT-DUP-002",
            DuplicateRowsSheetProfile("Aba 1", DuplicateRowsProfile(20, 1, 4, 0.2, 4, "type_tagged_nfkc_trim_newlines")),
        )
        record = get_rule_execution_record("QLT-NUMTEXT-007")
        null_record = get_rule_execution_record("QLT-NULL-001")
        catvar_record = get_rule_execution_record("QLT-CATVAR-008")
        duplicate_record = get_rule_execution_record("QLT-DUP-002")
        self.assertEqual(executable_rule_count(), 5)
        self.assertEqual(result[0]["rule_id"], "QLT-NUMTEXT-007")
        self.assertEqual(null_result[0]["rule_id"], "QLT-NULL-001")
        self.assertEqual(catvar_result[0]["rule_id"], "QLT-CATVAR-008")
        self.assertEqual(duplicate_result[0]["rule_id"], "QLT-DUP-002")
        self.assertEqual(record.status, "executable_draft")
        self.assertEqual(null_record.status, "executable_draft")
        self.assertEqual(catvar_record.status, "executable_draft")
        self.assertEqual(duplicate_record.status, "executable_draft")
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
            "MDL-UNDEFINED-020": "reserved_definition",
            "MET-DAX-015": "reserved_definition",
        }
        for rule_id, expected_status in expected_statuses.items():
            self.assertEqual(get_rule_execution_record(rule_id).status, expected_status, rule_id)
            with self.assertRaises(RuleExecutionUnavailableError, msg=rule_id):
                execute_registered_rule(rule_id, object())
        self.assertEqual(get_rule_execution_record("MDL-021").status, "unknown")

    def test_registry_entry_without_explicit_draft_gate_remains_blocked(self):
        with patch.dict(DRAFT_RULE_AUTHORIZATIONS, {}, clear=True):
            record = get_rule_execution_record("QLT-DUP-002")
            self.assertEqual(record.status, "baseline_reference")
            with self.assertRaises(RuleExecutionUnavailableError):
                execute_registered_rule("QLT-DUP-002", object())
