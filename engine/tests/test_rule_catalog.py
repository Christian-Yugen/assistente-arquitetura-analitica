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
from engine.granularity.entity_per_row import EntityPerRowSheetProfile
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
from engine.semantic.quantity import SemanticQuantityColumnProfile
from engine.profiling.numeric_text import infer_physical_type, profile_numeric_text
from engine.profiling.semantic_currency import profile_semantic_currency
from engine.profiling.semantic_percentage import profile_semantic_percentage
from engine.profiling.semantic_quantity import profile_semantic_quantity
from engine.profiling.semantic_target import profile_semantic_target
from engine.profiling.semantic_actual import profile_semantic_actual
from engine.profiling.semantic_sensitivity import profile_semantic_sensitivity
from engine.profiling.semantic_competence import profile_semantic_competence
from engine.profiling.semantic_description import profile_semantic_description
from engine.profiling.semantic_duration import profile_semantic_duration
from engine.profiling.semantic_status import profile_semantic_status
from engine.profiling.semantic_category import profile_semantic_category
from engine.profiling.semantic_location import profile_semantic_location
from engine.profiling.semantic_responsible import profile_semantic_responsible
from engine.semantic.currency import SemanticCurrencyColumnProfile
from engine.semantic.percentage import SemanticPercentageColumnProfile
from engine.semantic.target import SemanticTargetColumnProfile
from engine.semantic.actual import SemanticActualColumnProfile
from engine.semantic.sensitivity import SemanticSensitivityColumnProfile
from engine.semantic.competence import SemanticCompetenceColumnProfile
from engine.semantic.duration import SemanticDurationColumnProfile
from engine.semantic.description import SemanticDescriptionColumnProfile
from engine.semantic.status import SemanticStatusColumnProfile
from engine.semantic.category import SemanticCategoryColumnProfile
from engine.semantic.location import SemanticLocationColumnProfile
from engine.semantic.responsible import SemanticResponsibleColumnProfile
from engine.profiling.headers import HeadersProfile
from engine.quality.headers import HeadersSheetProfile
from engine.profiling.identifier_completeness import IdentifierCompletenessProfile
from engine.fact_dimension.fact_without_grain import FactWithoutDefinedGrainSheetProfile
from engine.fact_dimension.undefined_classification import UndefinedTableClassificationSheetProfile
from engine.quality.identifier_completeness import IdentifierCompletenessColumnProfile
from engine.fact_dimension.transactional import TransactionalFactSheetProfile
from engine.profiling.transactional_fact import TransactionalDateProfile
from engine.fact_dimension.standard_dimension import StandardDimensionSheetProfile
from engine.fact_dimension.calendar_dimension import CalendarDimensionSheetProfile
from engine.granularity.explicit_key import ExplicitKeyColumnProfile, ExplicitKeySheetProfile
from engine.granularity.event_per_row import EventPerRowSheetProfile
from engine.profiling.calendar_dimension import CalendarDateProfile
from engine.profiling.explicit_key_grain import profile_explicit_key_header


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
        quantity_values = list(range(10, 20))
        quantity_result = execute_registered_rule(
            "SEM-QTY-005",
            SemanticQuantityColumnProfile(
                "numeric",
                FormulaConsistencyProfile(formula_count=0),
                profile_numeric_text(quantity_values),
                profile_semantic_date(quantity_values),
                profile_semantic_quantity("qtd", quantity_values),
            ),
        )
        quantity_record = get_rule_execution_record("SEM-QTY-005")
        currency_values = [100.0 + index for index in range(10)]
        currency_result = execute_registered_rule(
            "SEM-CURR-006",
            SemanticCurrencyColumnProfile(
                "numeric",
                FormulaConsistencyProfile(formula_count=0),
                profile_numeric_text(currency_values),
                profile_semantic_date(currency_values),
                profile_semantic_currency("receita", currency_values, ["R$ #,##0.00"] * 10),
            ),
        )
        currency_record = get_rule_execution_record("SEM-CURR-006")
        percentage_values = [0.1] * 10
        percentage_result = execute_registered_rule(
            "SEM-PCT-007",
            SemanticPercentageColumnProfile(
                "numeric",
                FormulaConsistencyProfile(formula_count=0),
                profile_numeric_text(percentage_values),
                profile_semantic_date(percentage_values),
                profile_semantic_percentage("pct", percentage_values),
            ),
        )
        percentage_record = get_rule_execution_record("SEM-PCT-007")
        target_values = list(range(10, 20))
        target_result = execute_registered_rule(
            "SEM-TARGET-013",
            SemanticTargetColumnProfile(
                "numeric",
                FormulaConsistencyProfile(formula_count=0),
                profile_numeric_text(target_values),
                profile_semantic_date(target_values),
                profile_semantic_target("meta", target_values),
            ),
        )
        target_record = get_rule_execution_record("SEM-TARGET-013")
        actual_values = list(range(10, 20))
        actual_result = execute_registered_rule(
            "SEM-ACTUAL-014",
            SemanticActualColumnProfile(
                "numeric",
                FormulaConsistencyProfile(formula_count=0),
                profile_numeric_text(actual_values),
                profile_semantic_date(actual_values),
                profile_semantic_actual("realizado", actual_values),
            ),
        )
        actual_record = get_rule_execution_record("SEM-ACTUAL-014")
        sensitivity_result = execute_registered_rule(
            "SEM-SENS-015",
            SemanticSensitivityColumnProfile(
                profile_semantic_sensitivity(profile_semantic_identifier("CPF", ["__CATALOG_SYNTHETIC__"])),
            ),
        )
        sensitivity_record = get_rule_execution_record("SEM-SENS-015")
        competence_values = [f"2026-07-{day:02d}" for day in range(1, 11)]
        competence_result = execute_registered_rule(
            "SEM-COMP-002",
            SemanticCompetenceColumnProfile(
                FormulaConsistencyProfile(formula_count=0),
                profile_semantic_date(competence_values),
                profile_semantic_competence("data de competência"),
            ),
        )
        competence_record = get_rule_execution_record("SEM-COMP-002")
        description_values = [f"rotulo-{index:02d}" for index in range(1, 11)]
        description_result = execute_registered_rule(
            "SEM-DESC-004",
            SemanticDescriptionColumnProfile(
                infer_physical_type(description_values),
                FormulaConsistencyProfile(formula_count=0),
                profile_semantic_date(description_values),
                profile_semantic_identifier("descricao", description_values),
                profile_semantic_description("descricao"),
            ),
        )
        description_record = get_rule_execution_record("SEM-DESC-004")
        duration_values = list(range(1, 11))
        duration_result = execute_registered_rule(
            "SEM-DUR-008",
            SemanticDurationColumnProfile(
                infer_physical_type(duration_values),
                FormulaConsistencyProfile(formula_count=0),
                profile_numeric_text(duration_values),
                profile_semantic_date(duration_values),
                profile_semantic_duration("duração (horas)", duration_values),
            ),
        )
        duration_record = get_rule_execution_record("SEM-DUR-008")
        status_values = ["classe_a"] * 5 + ["classe_b"] * 5
        status_result = execute_registered_rule(
            "SEM-STATUS-009",
            SemanticStatusColumnProfile(
                infer_physical_type(status_values),
                FormulaConsistencyProfile(formula_count=0),
                profile_semantic_date(status_values),
                profile_semantic_identifier("status", status_values),
                profile_semantic_description("status"),
                profile_semantic_status("status", status_values),
            ),
        )
        status_record = get_rule_execution_record("SEM-STATUS-009")
        category_values = ["grupo_sintetico_a"] * 5 + ["grupo_sintetico_b"] * 5
        category_result = execute_registered_rule(
            "SEM-CAT-010",
            SemanticCategoryColumnProfile(
                infer_physical_type(category_values),
                FormulaConsistencyProfile(formula_count=0),
                profile_semantic_date(category_values),
                profile_semantic_identifier("categoria", category_values),
                profile_semantic_category("categoria", category_values),
            ),
        )
        category_record = get_rule_execution_record("SEM-CAT-010")
        location_values = ["local_privado_a"] * 5 + ["local_privado_b"] * 5
        location_result = execute_registered_rule(
            "SEM-LOC-011",
            SemanticLocationColumnProfile(
                infer_physical_type(location_values),
                FormulaConsistencyProfile(formula_count=0),
                profile_semantic_date(location_values),
                profile_semantic_identifier("cidade", location_values),
                profile_semantic_location("cidade", location_values),
            ),
        )
        location_record = get_rule_execution_record("SEM-LOC-011")
        responsible_values = ["responsavel_privado_a"] * 5 + ["responsavel_privado_b"] * 5
        responsible_result = execute_registered_rule(
            "SEM-RESP-012",
            SemanticResponsibleColumnProfile(
                infer_physical_type(responsible_values),
                FormulaConsistencyProfile(formula_count=0),
                profile_semantic_date(responsible_values),
                profile_semantic_identifier("responsavel", responsible_values),
                profile_semantic_responsible("responsavel", responsible_values),
            ),
        )
        responsible_record = get_rule_execution_record("SEM-RESP-012")
        explicit_key_result = execute_registered_rule(
            "GRN-EXPL-002",
            ExplicitKeySheetProfile(
                20,
                (ExplicitKeyColumnProfile(profile_explicit_key_header("ID"), True, False, False, 0, "numeric", 20, 20, 0),),
            ),
        )
        explicit_key_record = get_rule_execution_record("GRN-EXPL-002")
        event_result = execute_registered_rule(
            "GRN-EVENT-004",
            EventPerRowSheetProfile(20, 1, 1, 1, 0, 0, 0),
        )
        event_record = get_rule_execution_record("GRN-EVENT-004")
        entity_result = execute_registered_rule(
            "GRN-ENTITY-003",
            EntityPerRowSheetProfile(20, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0),
        )
        entity_record = get_rule_execution_record("GRN-ENTITY-003")
        fact_without_grain_result = execute_registered_rule(
            "MDL-FACTNOGRAIN-019",
            FactWithoutDefinedGrainSheetProfile(20, 1, 1, 0, 0, 0, 0, 0, 0),
        )
        fact_without_grain_record = get_rule_execution_record("MDL-FACTNOGRAIN-019")
        undefined_result = execute_registered_rule(
            "MDL-UNDEFINED-020",
            UndefinedTableClassificationSheetProfile(20, 2, 5, 0, 0, 0, 0, 0),
        )
        undefined_record = get_rule_execution_record("MDL-UNDEFINED-020")
        transactional_result = execute_registered_rule(
            "MDL-FACTTXN-002",
            TransactionalFactSheetProfile(20, True, (TransactionalDateProfile(20, 18),), 1),
        )
        dimension_result = execute_registered_rule(
            "MDL-DIMSTD-004",
            StandardDimensionSheetProfile(20, True, 1, 1, 0, 0),
        )
        calendar_dimension_result = execute_registered_rule(
            "MDL-DIMCAL-006",
            CalendarDimensionSheetProfile(20, True, (CalendarDateProfile(20, 20, 19),), 0),
        )
        self.assertEqual(executable_rule_count(), 63)
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
        self.assertEqual(quantity_result[0]["semantic_type"], "quantity_candidate")
        self.assertEqual(currency_result[0]["semantic_type"], "currency_candidate")
        self.assertEqual(percentage_result[0]["semantic_type"], "percentage_candidate")
        self.assertEqual(target_result[0]["semantic_type"], "target_or_forecast_candidate")
        self.assertEqual(actual_result[0]["semantic_type"], "actual_candidate")
        self.assertEqual(sensitivity_result[0]["sensitivity"], "personal_data_candidate")
        self.assertEqual(competence_result[0]["semantic_type"], "competence_date_candidate")
        self.assertEqual(description_result[0]["semantic_type"], "name_or_description_candidate")
        self.assertEqual(duration_result[0]["semantic_type"], "duration_candidate")
        self.assertEqual(status_result[0]["semantic_type"], "status_candidate")
        self.assertEqual(category_result[0]["semantic_type"], "category_candidate")
        self.assertEqual(location_result[0]["semantic_type"], "location_candidate")
        self.assertEqual(responsible_result[0]["semantic_type"], "responsible_candidate")
        self.assertEqual(explicit_key_result[0]["grain_type"], "explicit_key_candidate")
        self.assertEqual(event_result[0]["grain_type"], "event_per_row_candidate")
        self.assertEqual(fact_without_grain_result[0]["classification_type"], "fact_without_defined_grain_candidate")
        self.assertEqual(undefined_result[0]["classification_type"], "table_classification_undefined_candidate")
        self.assertEqual(transactional_result[0]["classification_type"], "fact_transactional_candidate")
        self.assertEqual(dimension_result[0]["classification_type"], "dimension_standard_candidate")
        self.assertEqual(calendar_dimension_result[0]["classification_type"], "dimension_calendar_candidate")
        self.assertEqual(record.status, "executable_draft")
        self.assertEqual(null_record.status, "executable_draft")
        self.assertEqual(identifier_record.status, "executable_draft")
        self.assertEqual(quantity_record.status, "executable_draft")
        self.assertEqual(currency_record.status, "executable_draft")
        self.assertEqual(percentage_record.status, "executable_draft")
        self.assertEqual(target_record.status, "executable_draft")
        self.assertEqual(actual_record.status, "executable_draft")
        self.assertEqual(sensitivity_record.status, "executable_draft")
        self.assertEqual(competence_record.status, "executable_draft")
        self.assertEqual(description_record.status, "executable_draft")
        self.assertEqual(duration_record.status, "executable_draft")
        self.assertEqual(status_record.status, "executable_draft")
        self.assertEqual(category_record.status, "executable_draft")
        self.assertEqual(location_record.status, "executable_draft")
        self.assertEqual(responsible_record.status, "executable_draft")
        self.assertEqual(explicit_key_record.status, "executable_draft")
        self.assertEqual(event_record.status, "executable_draft")
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
        self.assertEqual(get_rule_execution_record("MDL-FACTTXN-002").status, "executable_draft")
        self.assertEqual(fact_without_grain_record.status, "executable_draft")
        self.assertEqual(undefined_record.status, "executable_draft")
        self.assertEqual(get_rule_execution_record("MDL-DIMSTD-004").status, "executable_draft")
        self.assertEqual(get_rule_execution_record("MDL-DIMCAL-006").status, "executable_draft")
        self.assertEqual(get_rule_execution_record("REL-ONEMANY-001").status, "executable_draft")
        self.assertEqual(get_rule_execution_record("REL-NONUNIQ-002").status, "executable_draft")
        self.assertEqual(get_rule_execution_record("REL-ORPHAN-003").status, "executable_draft")
        self.assertEqual(get_rule_execution_record("REL-MANYMANY-004").status, "executable_draft")
        self.assertEqual(get_rule_execution_record("REL-FACTFACT-006").status, "executable_draft")
        self.assertEqual(get_rule_execution_record("REL-AMBIG-007").status, "executable_draft")
        self.assertEqual(get_rule_execution_record("REL-BIDIR-008").status, "executable_draft")
        self.assertEqual(get_rule_execution_record("REL-COMPKEY-009").status, "executable_draft")
        self.assertEqual(get_rule_execution_record("REL-CONFORMED-010").status, "executable_draft")
        self.assertEqual(get_rule_execution_record("MET-COMPL-001").status, "executable_draft")
        self.assertEqual(record.title, "Números armazenados como texto")

    def test_baseline_reference_and_reserved_official_slots_cannot_execute(self):
        expected_statuses = {
            "ALT-SENS-001": "reference_catalog_draft",
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
