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
from engine.profiling.empty_rows import EmptyRowsProfile
from engine.quality.empty_rows import EmptyRowsSheetProfile
from engine.profiling.mixed_types import MixedTypesProfile
from engine.quality.mixed_types import MixedTypesColumnProfile
from engine.profiling.bad_dates import BadDateProfile
from engine.quality.bad_dates import BadDateColumnProfile
from engine.profiling.whitespace import WhitespaceProfile
from engine.quality.whitespace import WhitespaceColumnProfile
from engine.profiling.total_rows import TotalRowsProfile
from engine.quality.total_rows import TotalRowsSheetProfile
from engine.profiling.negative_values import NegativeValuesProfile
from engine.quality.negative_values import NegativeValuesColumnProfile
from engine.profiling.outliers import OutlierProfile
from engine.quality.outliers import OutlierColumnProfile
from engine.profiling.formula_consistency import FormulaConsistencyProfile
from engine.quality.formula_consistency import FormulaConsistencyColumnProfile
from engine.profiling.semantic_date import profile_semantic_date
from engine.semantic.date_generic import SemanticDateColumnProfile
from engine.profiling.semantic_identifier import profile_semantic_identifier
from engine.semantic.identifier import SemanticIdentifierColumnProfile
from engine.profiling.headers import HeadersProfile
from engine.quality.headers import HeadersSheetProfile
from engine.profiling.identifier_completeness import IdentifierCompletenessProfile
from engine.quality.identifier_completeness import IdentifierCompletenessColumnProfile


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
        emptyrow_result = execute_registered_rule(
            "QLT-EMPTYROW-004",
            EmptyRowsSheetProfile("Aba 1", EmptyRowsProfile(3, 1, 0.25, 1)),
        )
        mixtype_result = execute_registered_rule(
            "QLT-MIXTYPE-005",
            MixedTypesColumnProfile("Campo", MixedTypesProfile(10, 0, 8, 2, 0, 0, 0)),
        )
        baddate_result = execute_registered_rule(
            "QLT-BADDATE-006",
            BadDateColumnProfile("Campo", BadDateProfile(10, 2, 0.2)),
        )
        whitespace_result = execute_registered_rule(
            "QLT-WHITESPACE-009",
            WhitespaceColumnProfile("Campo", WhitespaceProfile(20, 2, 1, 3, 0.15)),
        )
        totalrow_result = execute_registered_rule(
            "QLT-TOTALROW-010",
            TotalRowsSheetProfile("Aba 1", TotalRowsProfile(10, 1, 0.1)),
        )
        negative_result = execute_registered_rule(
            "QLT-NEGATIVE-011",
            NegativeValuesColumnProfile("Quantidade", NegativeValuesProfile(True, 20, 2, 0.1)),
        )
        outlier_result = execute_registered_rule(
            "QLT-OUTLIER-012",
            OutlierColumnProfile("Campo", OutlierProfile(True, 20, 20, 1, 2, 3, 0.15)),
        )
        formula_result = execute_registered_rule(
            "QLT-FORMULA-013",
            FormulaConsistencyColumnProfile("Campo", FormulaConsistencyProfile(True, 20, 18, 2, 0.1)),
        )
        headers_result = execute_registered_rule(
            "QLT-HEADERS-014",
            HeadersSheetProfile("Aba 1", HeadersProfile(4, 1, 0, 0, 0)),
        )
        idmiss_result = execute_registered_rule(
            "QLT-IDMISS-015",
            IdentifierCompletenessColumnProfile("ID", IdentifierCompletenessProfile(True, 20, 1, 19, 1, 2, 0.05, 0.1)),
        )
        record = get_rule_execution_record("QLT-NUMTEXT-007")
        null_record = get_rule_execution_record("QLT-NULL-001")
        catvar_record = get_rule_execution_record("QLT-CATVAR-008")
        duplicate_record = get_rule_execution_record("QLT-DUP-002")
        emptyrow_record = get_rule_execution_record("QLT-EMPTYROW-004")
        mixtype_record = get_rule_execution_record("QLT-MIXTYPE-005")
        baddate_record = get_rule_execution_record("QLT-BADDATE-006")
        whitespace_record = get_rule_execution_record("QLT-WHITESPACE-009")
        totalrow_record = get_rule_execution_record("QLT-TOTALROW-010")
        negative_record = get_rule_execution_record("QLT-NEGATIVE-011")
        outlier_record = get_rule_execution_record("QLT-OUTLIER-012")
        formula_record = get_rule_execution_record("QLT-FORMULA-013")
        headers_record = get_rule_execution_record("QLT-HEADERS-014")
        idmiss_record = get_rule_execution_record("QLT-IDMISS-015")
        semantic_result = execute_registered_rule("SEM-DATE-001", SemanticDateColumnProfile("Data", profile_semantic_date(["2026-01-01"] * 10)))
        semantic_record = get_rule_execution_record("SEM-DATE-001")
        identifier_result = execute_registered_rule("SEM-ID-003", SemanticIdentifierColumnProfile("numeric", 0, profile_semantic_identifier("codigo", range(1, 21))))
        identifier_record = get_rule_execution_record("SEM-ID-003")
        self.assertEqual(executable_rule_count(), 19)
        self.assertEqual(result[0]["rule_id"], "QLT-NUMTEXT-007")
        self.assertEqual(null_result[0]["rule_id"], "QLT-NULL-001")
        self.assertEqual(catvar_result[0]["rule_id"], "QLT-CATVAR-008")
        self.assertEqual(duplicate_result[0]["rule_id"], "QLT-DUP-002")
        self.assertEqual(emptyrow_result[0]["rule_id"], "QLT-EMPTYROW-004")
        self.assertEqual(mixtype_result[0]["rule_id"], "QLT-MIXTYPE-005")
        self.assertEqual(baddate_result[0]["rule_id"], "QLT-BADDATE-006")
        self.assertEqual(whitespace_result[0]["rule_id"], "QLT-WHITESPACE-009")
        self.assertEqual(totalrow_result[0]["rule_id"], "QLT-TOTALROW-010")
        self.assertEqual(negative_result[0]["rule_id"], "QLT-NEGATIVE-011")
        self.assertEqual(outlier_result[0]["rule_id"], "QLT-OUTLIER-012")
        self.assertEqual(formula_result[0]["rule_id"], "QLT-FORMULA-013")
        self.assertEqual(headers_result[0]["rule_id"], "QLT-HEADERS-014")
        self.assertEqual(idmiss_result[0]["rule_id"], "QLT-IDMISS-015")
        self.assertEqual(semantic_result[0]["semantic_type"], "date_generic")
        self.assertEqual(identifier_result[0]["semantic_type"], "identifier")
        self.assertEqual(record.status, "executable_draft")
        self.assertEqual(null_record.status, "executable_draft")
        self.assertEqual(identifier_record.status, "executable_draft")
        self.assertEqual(catvar_record.status, "executable_draft")
        self.assertEqual(duplicate_record.status, "executable_draft")
        self.assertEqual(emptyrow_record.status, "executable_draft")
        self.assertEqual(mixtype_record.status, "executable_draft")
        self.assertEqual(baddate_record.status, "executable_draft")
        self.assertEqual(whitespace_record.status, "executable_draft")
        self.assertEqual(totalrow_record.status, "executable_draft")
        self.assertEqual(negative_record.status, "executable_draft")
        self.assertEqual(outlier_record.status, "executable_draft")
        self.assertEqual(formula_record.status, "executable_draft")
        self.assertEqual(headers_record.status, "executable_draft")
        self.assertEqual(idmiss_record.status, "executable_draft")
        self.assertEqual(semantic_record.status, "executable_draft")
        self.assertEqual(get_rule_execution_record("GRN-COMP-001").status, "executable_draft")
        self.assertEqual(get_rule_execution_record("MDL-FACTPER-001").status, "executable_draft")
        self.assertEqual(record.title, "Números armazenados como texto")

    def test_baseline_reference_and_reserved_official_slots_cannot_execute(self):
        expected_statuses = {
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
