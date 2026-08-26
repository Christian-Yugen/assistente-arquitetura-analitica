"""Executa o ruleset draft sobre contexto agregado e produz o objeto raiz canônico do diagnóstico."""

from __future__ import annotations

from dataclasses import dataclass, field
from time import perf_counter
from typing import Iterable, Literal

from engine.catalog import executable_rule_count, execute_registered_rule, get_rule_execution_record
from engine.metrics.completion import CompletionRateConceptProfile
from engine.metrics.sum import SumConceptProfile
from engine.metrics.count import CountConceptProfile
from engine.metrics.distinct_count import DistinctCountConceptProfile
from engine.metrics.average import AverageConceptProfile
from engine.metrics.minmax import MinMaxConceptProfile
from engine.metrics.rate import RateConceptProfile
from engine.metrics.absolute_delta import AbsoluteDeltaConceptProfile
from engine.metrics.percentage_delta import PercentageDeltaConceptProfile
from engine.metrics.running_total import RunningTotalConceptProfile
from engine.metrics.weighted_average import WeightedAverageConceptProfile
from engine.metrics.semiadditive import SemiadditiveConceptProfile
from engine.metrics.domain import DomainMetricConceptProfile
from engine.metrics.impossible import InsufficientMetricConceptProfile
from engine.metrics.dax import DaxTemplateConceptProfile
from engine.alerts.sensitivity import SensitiveDataRestrictionProfile
from engine.alerts.quality import CriticalQualityRiskProfile
from engine.alerts.grain import UndefinedGrainAlertProfile
from engine.alerts.key import InvalidKeyAlertProfile
from engine.alerts.ambiguity import StructuralAmbiguityAlertProfile
from engine.alerts.metric_risk import PotentiallyMisleadingMetricAlertProfile
from engine.alerts.percentage_sum import PercentageSumAlertProfile
from engine.alerts.average_of_averages import AverageOfAveragesAlertProfile
from engine.contracts.diagnosis import CONTRACT_ID, SCHEMA_VERSION, _timestamp, to_diagnosis_fragment, to_grain_fragment, to_metric_fragment, to_relationship_fragment, to_semantic_classification_fragment, to_sensitivity_fragment, to_table_classification_fragment
from engine.contracts.execution_profile import DraftExecutionProfile, validate_governed_output
from engine.contracts.validation import validate_diagnosis_root
from engine.profiling.numeric_text import NumericTextProfile, infer_physical_type, profile_numeric_text
from engine.profiling.missingness import MissingnessProfile, profile_missingness
from engine.profiling.categorical_variations import CategoricalVariationProfile, profile_categorical_variations
from engine.profiling.duplicate_rows import DuplicateRowsProfile
from engine.profiling.empty_rows import EmptyRowsProfile
from engine.profiling.mixed_types import MixedTypesProfile, profile_mixed_types
from engine.profiling.bad_dates import BadDateProfile, profile_bad_dates
from engine.profiling.whitespace import WhitespaceProfile, profile_whitespace
from engine.profiling.total_rows import TotalRowsProfile
from engine.profiling.negative_values import NegativeValuesProfile, profile_negative_values
from engine.profiling.outliers import OutlierProfile, profile_outliers
from engine.profiling.formula_consistency import FormulaConsistencyProfile
from engine.profiling.headers import HeadersProfile
from engine.profiling.identifier_completeness import IdentifierCompletenessProfile, profile_identifier_completeness
from engine.profiling.semantic_date import SemanticDateProfile, profile_semantic_date
from engine.profiling.semantic_competence import SemanticCompetenceProfile, profile_semantic_competence
from engine.profiling.semantic_description import SemanticDescriptionProfile, profile_semantic_description
from engine.profiling.semantic_duration import SemanticDurationProfile, profile_semantic_duration
from engine.profiling.semantic_status import SemanticStatusProfile, profile_semantic_status
from engine.profiling.semantic_category import SemanticCategoryProfile, profile_semantic_category
from engine.profiling.semantic_location import SemanticLocationProfile, profile_semantic_location
from engine.profiling.semantic_responsible import SemanticResponsibleProfile, profile_semantic_responsible
from engine.profiling.semantic_actual import SemanticActualProfile, profile_semantic_actual
from engine.profiling.semantic_currency import SemanticCurrencyProfile, profile_semantic_currency
from engine.profiling.semantic_identifier import SemanticIdentifierProfile, profile_semantic_identifier
from engine.profiling.semantic_percentage import SemanticPercentageProfile, profile_semantic_percentage
from engine.profiling.semantic_quantity import SemanticQuantityProfile, profile_semantic_quantity
from engine.profiling.semantic_sensitivity import profile_semantic_sensitivity
from engine.profiling.semantic_target import SemanticTargetProfile, profile_semantic_target
from engine.profiling.composite_grain import CompositeGrainProfile
from engine.profiling.entity_per_row_grain import EntityMarkerHeaderProfile, profile_entity_marker_header
from engine.profiling.event_per_row_grain import EventMarkerHeaderProfile, profile_event_marker_header
from engine.profiling.explicit_key_grain import ExplicitKeyHeaderProfile, profile_explicit_key_header
from engine.profiling.periodic_fact import PeriodicDateProfile, profile_periodic_date
from engine.profiling.transactional_fact import TransactionalDateProfile, profile_transactional_date
from engine.profiling.calendar_dimension import CalendarDateProfile, profile_calendar_date
from engine.quality.numtext import NumericTextColumnProfile
from engine.quality.nulls import NullColumnProfile
from engine.quality.catvar import CategoricalVariationColumnProfile
from engine.quality.duplicates import DuplicateRowsSheetProfile
from engine.quality.empty_columns import EmptyColumnProfile
from engine.quality.empty_rows import EmptyRowsSheetProfile
from engine.quality.mixed_types import MixedTypesColumnProfile
from engine.quality.bad_dates import BadDateColumnProfile
from engine.quality.whitespace import WhitespaceColumnProfile
from engine.quality.total_rows import TotalRowsSheetProfile
from engine.quality.negative_values import NegativeValuesColumnProfile
from engine.quality.outliers import OutlierColumnProfile
from engine.quality.formula_consistency import FormulaConsistencyColumnProfile
from engine.quality.headers import HeadersSheetProfile
from engine.quality.identifier_completeness import IdentifierCompletenessColumnProfile
from engine.semantic.date_generic import SemanticDateColumnProfile
from engine.semantic.competence import SemanticCompetenceColumnProfile
from engine.semantic.description import SemanticDescriptionColumnProfile
from engine.semantic.duration import SemanticDurationColumnProfile
from engine.semantic.status import SemanticStatusColumnProfile
from engine.semantic.category import SemanticCategoryColumnProfile
from engine.semantic.location import SemanticLocationColumnProfile
from engine.semantic.responsible import SemanticResponsibleColumnProfile
from engine.semantic.actual import SemanticActualColumnProfile
from engine.semantic.currency import SemanticCurrencyColumnProfile
from engine.semantic.identifier import SemanticIdentifierColumnProfile, classify_identifier
from engine.semantic.percentage import SemanticPercentageColumnProfile
from engine.semantic.quantity import SemanticQuantityColumnProfile
from engine.semantic.sensitivity import SemanticSensitivityColumnProfile
from engine.semantic.target import SemanticTargetColumnProfile
from engine.granularity.composite import CompositeGrainSheetProfile
from engine.granularity.entity_per_row import EntityPerRowSheetProfile
from engine.granularity.event_per_row import EventPerRowSheetProfile
from engine.granularity.explicit_key import ExplicitKeyColumnProfile, ExplicitKeySheetProfile
from engine.fact_dimension.periodic import PeriodicFactSheetProfile
from engine.fact_dimension.standard_dimension import StandardDimensionSheetProfile
from engine.fact_dimension.transactional import TransactionalFactSheetProfile
from engine.fact_dimension.calendar_dimension import CalendarDimensionSheetProfile
from engine.fact_dimension.fact_without_grain import FactWithoutDefinedGrainSheetProfile
from engine.fact_dimension.undefined_classification import UndefinedTableClassificationSheetProfile
from engine.profiling.relationship_pairs import CompositeRelationshipPairSignal, RelationshipPairSignal
from engine.relationships.one_to_many import OneToManyRelationshipPairProfile
from engine.relationships.non_unique_one_side import NonUniqueOneSideRelationshipPairProfile
from engine.relationships.orphan_reference import OrphanReferenceRelationshipPairProfile
from engine.relationships.many_to_many import ManyToManyRelationshipPairProfile
from engine.relationships.direct_fact import DirectFactRelationshipPairProfile
from engine.relationships.ambiguous_path import AmbiguousRelationshipPathPairProfile
from engine.relationships.bidirectional_filter import BidirectionalFilterReviewPairProfile
from engine.relationships.composite_key import CompositeRelationshipKeyPairProfile
from engine.relationships.conformed_dimension import ConformedDimensionPairProfile
from engine.metrics.completion import CompletionRateConceptProfile


@dataclass(frozen=True)
class DiagnosisMetadata:
    analysis_id: str
    project_id: str
    owner_user_id: str
    project_name: str
    objective: str
    file_id: str
    original_name: str
    file_size_bytes: int
    file_sha256: str
    file_mime_type: str
    workbook_readable: bool
    consented_at: str
    created_at: str
    uploaded_at: str
    retention_delete_at: str
    retention_status: str
    correlation_id: str
    terms_version: str
    domain: Literal["generic", "sso", "hr"]
    business_questions: tuple[str, ...]
    analysis_version: int
    supersedes_analysis_id: str | None
    execution_profile: DraftExecutionProfile


@dataclass(frozen=True)
class ColumnAnalysisContext:
    sheet_id: str
    sheet_name: str
    sheet_position: int
    sheet_visibility: Literal["visible", "hidden", "very_hidden"]
    column_id: str
    column_name: str
    column_position: int
    physical_type: str
    numeric_text: NumericTextProfile
    missingness: MissingnessProfile = MissingnessProfile()
    categorical_variations: CategoricalVariationProfile = field(default_factory=CategoricalVariationProfile)
    duplicate_rows: DuplicateRowsProfile = field(default_factory=DuplicateRowsProfile)
    empty_rows: EmptyRowsProfile = field(default_factory=EmptyRowsProfile)
    mixed_types: MixedTypesProfile = field(default_factory=MixedTypesProfile)
    bad_dates: BadDateProfile = field(default_factory=BadDateProfile)
    whitespace: WhitespaceProfile = field(default_factory=WhitespaceProfile)
    total_rows: TotalRowsProfile = field(default_factory=TotalRowsProfile)
    negative_values: NegativeValuesProfile = field(default_factory=NegativeValuesProfile)
    outliers: OutlierProfile = field(default_factory=OutlierProfile)
    formulas: FormulaConsistencyProfile = field(default_factory=FormulaConsistencyProfile)
    headers: HeadersProfile = field(default_factory=HeadersProfile)
    identifiers: IdentifierCompletenessProfile = field(default_factory=IdentifierCompletenessProfile)
    semantic_date: SemanticDateProfile = field(default_factory=SemanticDateProfile)
    semantic_competence: SemanticCompetenceProfile = field(default_factory=SemanticCompetenceProfile)
    semantic_description: SemanticDescriptionProfile = field(default_factory=SemanticDescriptionProfile)
    semantic_duration: SemanticDurationProfile = field(default_factory=SemanticDurationProfile)
    semantic_status: SemanticStatusProfile = field(default_factory=SemanticStatusProfile)
    semantic_category: SemanticCategoryProfile = field(default_factory=SemanticCategoryProfile)
    semantic_location: SemanticLocationProfile = field(default_factory=SemanticLocationProfile)
    semantic_responsible: SemanticResponsibleProfile = field(default_factory=SemanticResponsibleProfile)
    semantic_actual: SemanticActualProfile = field(default_factory=SemanticActualProfile)
    semantic_currency: SemanticCurrencyProfile = field(default_factory=SemanticCurrencyProfile)
    semantic_identifier: SemanticIdentifierProfile = field(default_factory=SemanticIdentifierProfile)
    semantic_percentage: SemanticPercentageProfile = field(default_factory=SemanticPercentageProfile)
    semantic_quantity: SemanticQuantityProfile = field(default_factory=SemanticQuantityProfile)
    semantic_target: SemanticTargetProfile = field(default_factory=SemanticTargetProfile)
    composite_grain: CompositeGrainProfile = field(default_factory=CompositeGrainProfile)
    entity_marker_header: EntityMarkerHeaderProfile = field(default_factory=EntityMarkerHeaderProfile)
    event_marker_header: EventMarkerHeaderProfile = field(default_factory=EventMarkerHeaderProfile)
    explicit_key_header: ExplicitKeyHeaderProfile = field(default_factory=ExplicitKeyHeaderProfile)
    periodic_date: PeriodicDateProfile = field(default_factory=PeriodicDateProfile)
    transactional_date: TransactionalDateProfile = field(default_factory=TransactionalDateProfile)
    calendar_date: CalendarDateProfile = field(default_factory=CalendarDateProfile)


def build_column_analysis_context(
    *, sheet_id: str, column_id: str, column_name: str, values: Iterable[object], sheet_name: str, sheet_position: int, sheet_visibility: Literal["visible", "hidden", "very_hidden"], column_position: int
) -> ColumnAnalysisContext:
    """Descarta valores brutos depois do profiling e preserva apenas métricas agregadas."""

    materialized_values = list(values)
    semantic_identifier = profile_semantic_identifier(column_name, materialized_values)
    semantic_status = profile_semantic_status(column_name, materialized_values)
    semantic_category = profile_semantic_category(column_name, materialized_values)
    semantic_location = profile_semantic_location(column_name, materialized_values)
    semantic_responsible = profile_semantic_responsible(column_name, materialized_values)
    entity_marker_header = profile_entity_marker_header(column_name)
    event_marker_header = profile_event_marker_header(column_name)
    explicit_key_header = profile_explicit_key_header(column_name)
    safe_column_name = (
        f"Campo sensível {column_position + 1}"
        if semantic_identifier.sensitive_header or semantic_status.header_eligible or semantic_category.header_eligible or semantic_location.header_eligible or semantic_responsible.header_eligible or entity_marker_header.header_eligible or event_marker_header.header_eligible or explicit_key_header.header_eligible
        else column_name
    )
    return ColumnAnalysisContext(
        sheet_id=sheet_id,
        sheet_name=sheet_name,
        sheet_position=sheet_position,
        sheet_visibility=sheet_visibility,
        column_id=column_id,
        column_name=safe_column_name,
        column_position=column_position,
        physical_type=infer_physical_type(materialized_values),
        numeric_text=profile_numeric_text(materialized_values),
        missingness=profile_missingness(materialized_values),
        categorical_variations=profile_categorical_variations(materialized_values),
        mixed_types=profile_mixed_types(materialized_values),
        bad_dates=profile_bad_dates(materialized_values),
        whitespace=profile_whitespace(materialized_values),
        negative_values=profile_negative_values(safe_column_name, materialized_values),
        outliers=profile_outliers(materialized_values),
        identifiers=profile_identifier_completeness(safe_column_name, materialized_values),
        semantic_date=profile_semantic_date(materialized_values),
        semantic_competence=profile_semantic_competence(column_name),
        semantic_description=profile_semantic_description(column_name),
        semantic_duration=profile_semantic_duration(column_name, materialized_values),
        semantic_status=semantic_status,
        semantic_category=semantic_category,
        semantic_location=semantic_location,
        semantic_responsible=semantic_responsible,
        semantic_actual=profile_semantic_actual(column_name, materialized_values),
        semantic_currency=profile_semantic_currency(column_name, materialized_values),
        semantic_identifier=semantic_identifier,
        semantic_percentage=profile_semantic_percentage(column_name, materialized_values),
        semantic_quantity=profile_semantic_quantity(column_name, materialized_values),
        semantic_target=profile_semantic_target(column_name, materialized_values),
        entity_marker_header=entity_marker_header,
        event_marker_header=event_marker_header,
        explicit_key_header=explicit_key_header,
        periodic_date=profile_periodic_date(materialized_values),
        transactional_date=profile_transactional_date(materialized_values),
        calendar_date=profile_calendar_date(materialized_values),
    )


def execute_quality_diagnosis(
    columns: Iterable[ColumnAnalysisContext],
    *,
    metadata: DiagnosisMetadata,
    relationship_pair_signals: Iterable[RelationshipPairSignal] = (),
    composite_relationship_pair_signals: Iterable[CompositeRelationshipPairSignal] = (),
) -> dict[str, object]:
    """Monta todos os blocos do contrato em estado partial sem fabricar recomendações de modelo."""

    profile = metadata.execution_profile
    relationship_pair_signals = tuple(relationship_pair_signals)
    composite_relationship_pair_signals = tuple(composite_relationship_pair_signals)
    started_at = _timestamp()
    started_clock = perf_counter()
    quality_findings: list[tuple[str, str | None, dict[str, object]]] = []
    semantic_candidates: list[tuple[str, str, list[dict[str, object]]]] = []
    sensitivity_candidates: list[tuple[str, str, list[dict[str, object]]]] = []
    grain_candidates: dict[str, list[dict[str, object]]] = {}
    table_candidates: dict[str, list[dict[str, object]]] = {}
    grouped_columns: dict[str, list[ColumnAnalysisContext]] = {}
    for column in columns:
        grouped_columns.setdefault(column.sheet_id, []).append(column)
        column_profile = NumericTextColumnProfile(
            name=column.column_name,
            physical_type=column.physical_type,  # type: ignore[arg-type]
            non_empty_value_count=column.numeric_text.non_empty_value_count,
            numeric_text_candidate_count=column.numeric_text.numeric_text_candidate_count,
            numeric_text_candidate_ratio=column.numeric_text.numeric_text_candidate_ratio,
            numeric_text_basis=column.numeric_text.numeric_text_basis,
            numeric_text_ambiguity_count=column.numeric_text.numeric_text_ambiguity_count,
        )
        for finding in execute_registered_rule("QLT-NUMTEXT-007", column_profile):
            quality_findings.append((column.sheet_id, column.column_id, finding))
        null_profile = NullColumnProfile(name=column.column_name, physical_type=column.physical_type, missingness=column.missingness)
        for finding in execute_registered_rule("QLT-NULL-001", null_profile):
            quality_findings.append((column.sheet_id, column.column_id, finding))
        categorical_variation_profile = CategoricalVariationColumnProfile(
            name=column.column_name,
            physical_type=column.physical_type,
            variations=column.categorical_variations,
        )
        for finding in execute_registered_rule("QLT-CATVAR-008", categorical_variation_profile):
            quality_findings.append((column.sheet_id, column.column_id, finding))
        empty_column_profile = EmptyColumnProfile(name=column.column_name, missingness=column.missingness)
        if get_rule_execution_record("QLT-EMPTYCOL-003").status == "executable_draft":
            for finding in execute_registered_rule("QLT-EMPTYCOL-003", empty_column_profile):
                quality_findings.append((column.sheet_id, column.column_id, finding))
        mixed_types_profile = MixedTypesColumnProfile(name=column.column_name, mixed_types=column.mixed_types)
        if get_rule_execution_record("QLT-MIXTYPE-005").status == "executable_draft":
            for finding in execute_registered_rule("QLT-MIXTYPE-005", mixed_types_profile):
                quality_findings.append((column.sheet_id, column.column_id, finding))
        bad_date_profile = BadDateColumnProfile(name=column.column_name, bad_dates=column.bad_dates)
        if get_rule_execution_record("QLT-BADDATE-006").status == "executable_draft":
            for finding in execute_registered_rule("QLT-BADDATE-006", bad_date_profile):
                quality_findings.append((column.sheet_id, column.column_id, finding))
        whitespace_profile = WhitespaceColumnProfile(name=column.column_name, whitespace=column.whitespace)
        if get_rule_execution_record("QLT-WHITESPACE-009").status == "executable_draft":
            for finding in execute_registered_rule("QLT-WHITESPACE-009", whitespace_profile):
                quality_findings.append((column.sheet_id, column.column_id, finding))
        negative_values_profile = NegativeValuesColumnProfile(name=column.column_name, negative_values=column.negative_values)
        if get_rule_execution_record("QLT-NEGATIVE-011").status == "executable_draft":
            for finding in execute_registered_rule("QLT-NEGATIVE-011", negative_values_profile):
                quality_findings.append((column.sheet_id, column.column_id, finding))
        outlier_profile = OutlierColumnProfile(name=column.column_name, outliers=column.outliers)
        if get_rule_execution_record("QLT-OUTLIER-012").status == "executable_draft":
            for finding in execute_registered_rule("QLT-OUTLIER-012", outlier_profile):
                quality_findings.append((column.sheet_id, column.column_id, finding))
        formula_profile = FormulaConsistencyColumnProfile(name=column.column_name, formulas=column.formulas)
        if get_rule_execution_record("QLT-FORMULA-013").status == "executable_draft":
            for finding in execute_registered_rule("QLT-FORMULA-013", formula_profile):
                quality_findings.append((column.sheet_id, column.column_id, finding))
        identifier_profile = IdentifierCompletenessColumnProfile(name=column.column_name, identifiers=column.identifiers)
        if get_rule_execution_record("QLT-IDMISS-015").status == "executable_draft":
            for finding in execute_registered_rule("QLT-IDMISS-015", identifier_profile):
                quality_findings.append((column.sheet_id, column.column_id, finding))
        if get_rule_execution_record("SEM-DATE-001").status == "executable_draft":
            semantic_profile = SemanticDateColumnProfile(name=column.column_name, semantic_date=column.semantic_date)
            semantic_candidates.append((column.sheet_id, column.column_id, execute_registered_rule("SEM-DATE-001", semantic_profile)))
        if get_rule_execution_record("SEM-COMP-002").status == "executable_draft":
            competence_semantic_profile = SemanticCompetenceColumnProfile(
                formulas=column.formulas,
                semantic_date=column.semantic_date,
                semantic_competence=column.semantic_competence,
            )
            semantic_candidates.append((column.sheet_id, column.column_id, execute_registered_rule("SEM-COMP-002", competence_semantic_profile)))
        if get_rule_execution_record("SEM-DESC-004").status == "executable_draft":
            description_semantic_profile = SemanticDescriptionColumnProfile(
                physical_type=column.physical_type,
                formulas=column.formulas,
                semantic_date=column.semantic_date,
                semantic_identifier=column.semantic_identifier,
                semantic_description=column.semantic_description,
            )
            semantic_candidates.append((column.sheet_id, column.column_id, execute_registered_rule("SEM-DESC-004", description_semantic_profile)))
        if get_rule_execution_record("SEM-STATUS-009").status == "executable_draft":
            status_semantic_profile = SemanticStatusColumnProfile(
                physical_type=column.physical_type,
                formulas=column.formulas,
                semantic_date=column.semantic_date,
                semantic_identifier=column.semantic_identifier,
                semantic_description=column.semantic_description,
                semantic_status=column.semantic_status,
            )
            semantic_candidates.append((column.sheet_id, column.column_id, execute_registered_rule("SEM-STATUS-009", status_semantic_profile)))
        if get_rule_execution_record("SEM-CAT-010").status == "executable_draft":
            category_semantic_profile = SemanticCategoryColumnProfile(
                physical_type=column.physical_type,
                formulas=column.formulas,
                semantic_date=column.semantic_date,
                semantic_identifier=column.semantic_identifier,
                semantic_category=column.semantic_category,
            )
            semantic_candidates.append((column.sheet_id, column.column_id, execute_registered_rule("SEM-CAT-010", category_semantic_profile)))
        if get_rule_execution_record("SEM-LOC-011").status == "executable_draft":
            location_semantic_profile = SemanticLocationColumnProfile(
                physical_type=column.physical_type,
                formulas=column.formulas,
                semantic_date=column.semantic_date,
                semantic_identifier=column.semantic_identifier,
                semantic_location=column.semantic_location,
            )
            semantic_candidates.append((column.sheet_id, column.column_id, execute_registered_rule("SEM-LOC-011", location_semantic_profile)))
        if get_rule_execution_record("SEM-RESP-012").status == "executable_draft":
            responsible_semantic_profile = SemanticResponsibleColumnProfile(
                physical_type=column.physical_type,
                formulas=column.formulas,
                semantic_date=column.semantic_date,
                semantic_identifier=column.semantic_identifier,
                semantic_responsible=column.semantic_responsible,
            )
            semantic_candidates.append((column.sheet_id, column.column_id, execute_registered_rule("SEM-RESP-012", responsible_semantic_profile)))
        if get_rule_execution_record("SEM-DUR-008").status == "executable_draft":
            duration_semantic_profile = SemanticDurationColumnProfile(
                physical_type=column.physical_type,
                formulas=column.formulas,
                numeric_text=column.numeric_text,
                semantic_date=column.semantic_date,
                semantic_duration=column.semantic_duration,
            )
            semantic_candidates.append((column.sheet_id, column.column_id, execute_registered_rule("SEM-DUR-008", duration_semantic_profile)))
        if get_rule_execution_record("SEM-ID-003").status == "executable_draft":
            identifier_semantic_profile = SemanticIdentifierColumnProfile(
                physical_type=column.physical_type, formula_count=column.formulas.formula_count,
                semantic_identifier=column.semantic_identifier,
            )
            semantic_candidates.append((column.sheet_id, column.column_id, execute_registered_rule("SEM-ID-003", identifier_semantic_profile)))
        if get_rule_execution_record("SEM-QTY-005").status == "executable_draft":
            quantity_semantic_profile = SemanticQuantityColumnProfile(
                physical_type=column.physical_type,
                formulas=column.formulas,
                numeric_text=column.numeric_text,
                semantic_date=column.semantic_date,
                semantic_quantity=column.semantic_quantity,
            )
            semantic_candidates.append((column.sheet_id, column.column_id, execute_registered_rule("SEM-QTY-005", quantity_semantic_profile)))
        if get_rule_execution_record("SEM-PCT-007").status == "executable_draft":
            percentage_semantic_profile = SemanticPercentageColumnProfile(
                physical_type=column.physical_type,
                formulas=column.formulas,
                numeric_text=column.numeric_text,
                semantic_date=column.semantic_date,
                semantic_percentage=column.semantic_percentage,
            )
            semantic_candidates.append((column.sheet_id, column.column_id, execute_registered_rule("SEM-PCT-007", percentage_semantic_profile)))
        if get_rule_execution_record("SEM-CURR-006").status == "executable_draft":
            currency_semantic_profile = SemanticCurrencyColumnProfile(
                physical_type=column.physical_type,
                formulas=column.formulas,
                numeric_text=column.numeric_text,
                semantic_date=column.semantic_date,
                semantic_currency=column.semantic_currency,
            )
            semantic_candidates.append((column.sheet_id, column.column_id, execute_registered_rule("SEM-CURR-006", currency_semantic_profile)))
        if get_rule_execution_record("SEM-TARGET-013").status == "executable_draft":
            target_semantic_profile = SemanticTargetColumnProfile(
                physical_type=column.physical_type,
                formulas=column.formulas,
                numeric_text=column.numeric_text,
                semantic_date=column.semantic_date,
                semantic_target=column.semantic_target,
            )
            semantic_candidates.append((column.sheet_id, column.column_id, execute_registered_rule("SEM-TARGET-013", target_semantic_profile)))
        if get_rule_execution_record("SEM-ACTUAL-014").status == "executable_draft":
            actual_semantic_profile = SemanticActualColumnProfile(
                physical_type=column.physical_type,
                formulas=column.formulas,
                numeric_text=column.numeric_text,
                semantic_date=column.semantic_date,
                semantic_actual=column.semantic_actual,
            )
            semantic_candidates.append((column.sheet_id, column.column_id, execute_registered_rule("SEM-ACTUAL-014", actual_semantic_profile)))
        if get_rule_execution_record("SEM-SENS-015").status == "executable_draft":
            sensitivity_profile = SemanticSensitivityColumnProfile(
                semantic_sensitivity=profile_semantic_sensitivity(column.semantic_identifier),
            )
            sensitivity_candidates.append((column.sheet_id, column.column_id, execute_registered_rule("SEM-SENS-015", sensitivity_profile)))

    for sheet_id, sheet_columns in grouped_columns.items():
        representative = sheet_columns[0]
        duplicate_profile = DuplicateRowsSheetProfile(name=representative.sheet_name, duplicates=representative.duplicate_rows)
        for finding in execute_registered_rule("QLT-DUP-002", duplicate_profile):
            quality_findings.append((sheet_id, None, finding))
        empty_rows_profile = EmptyRowsSheetProfile(name=representative.sheet_name, empty_rows=representative.empty_rows)
        if get_rule_execution_record("QLT-EMPTYROW-004").status == "executable_draft":
            for finding in execute_registered_rule("QLT-EMPTYROW-004", empty_rows_profile):
                quality_findings.append((sheet_id, None, finding))
        total_rows_profile = TotalRowsSheetProfile(name=representative.sheet_name, total_rows=representative.total_rows)
        if get_rule_execution_record("QLT-TOTALROW-010").status == "executable_draft":
            for finding in execute_registered_rule("QLT-TOTALROW-010", total_rows_profile):
                quality_findings.append((sheet_id, None, finding))
        headers_profile = HeadersSheetProfile(name=representative.sheet_name, headers=representative.headers)
        if get_rule_execution_record("QLT-HEADERS-014").status == "executable_draft":
            for finding in execute_registered_rule("QLT-HEADERS-014", headers_profile):
                quality_findings.append((sheet_id, None, finding))
        if get_rule_execution_record("GRN-COMP-001").status == "executable_draft":
            identifier_positions = frozenset(
                column.column_position for column in sheet_columns
                if classify_identifier(SemanticIdentifierColumnProfile(
                    physical_type=column.physical_type,
                    formula_count=column.formulas.formula_count,
                    semantic_identifier=column.semantic_identifier,
                )) and column.semantic_identifier.distinct_ratio != 1.0
            )
            grain_candidates[sheet_id] = execute_registered_rule("GRN-COMP-001", CompositeGrainSheetProfile(
                composite_grain=representative.composite_grain,
                semantic_identifier_component_positions=identifier_positions,
            ))
        if get_rule_execution_record("GRN-EXPL-002").status == "executable_draft":
            observed_row_count = max(column.missingness.observed_cell_count for column in sheet_columns)
            explicit_key_candidates = execute_registered_rule(
                "GRN-EXPL-002",
                ExplicitKeySheetProfile(
                    observed_row_count=observed_row_count,
                    columns=tuple(
                        ExplicitKeyColumnProfile(
                            header=column.explicit_key_header,
                            identifier_signal=column.semantic_identifier.header_signal,
                            sensitive_header=column.semantic_identifier.sensitive_header,
                            description_header=column.semantic_description.header_eligible,
                            recognized_date_count=column.semantic_date.recognized_date_count,
                            physical_type=column.physical_type,
                            non_missing_count=column.missingness.non_missing_cell_count,
                            distinct_non_missing_count=column.semantic_identifier.distinct_non_missing_count,
                            formula_count=column.formulas.formula_count,
                        )
                        for column in sheet_columns
                    ),
                ),
            )
            if explicit_key_candidates:
                grain_candidates[sheet_id] = explicit_key_candidates + grain_candidates.get(sheet_id, [])
        if get_rule_execution_record("GRN-EVENT-004").status == "executable_draft":
            observed_row_count = max(column.missingness.observed_cell_count for column in sheet_columns)
            explicit_key_candidate_count = sum(
                1
                for candidate in grain_candidates.get(sheet_id, [])
                if candidate["rule_id"] == "GRN-EXPL-002"
                and candidate["grain_type"] == "explicit_key_candidate"
            )
            event_header_eligible_count = sum(
                1 for column in sheet_columns if column.event_marker_header.header_eligible
            )
            excluded_event_marker_count = sum(
                1
                for column in sheet_columns
                if column.event_marker_header.header_eligible
                and (
                    column.physical_type != "text"
                    or column.semantic_identifier.sensitive_header
                    or column.semantic_description.header_eligible
                    or column.semantic_date.recognized_date_count != 0
                    or column.formulas.formula_count != 0
                )
            )
            event_marker_formula_count = sum(
                column.formulas.formula_count
                for column in sheet_columns
                if column.event_marker_header.header_eligible
            )
            non_competence_date_candidate_count = sum(
                1
                for column in sheet_columns
                if (
                    column.semantic_date.non_missing_count >= 10
                    and column.semantic_date.recognized_date_ratio == 1.0
                    and not column.semantic_competence.header_eligible
                    and column.formulas.formula_count == 0
                )
            )
            ambiguity_count = max(
                0,
                event_header_eligible_count - 1,
                explicit_key_candidate_count - 1,
                non_competence_date_candidate_count - 1,
            )
            event_per_row_candidates = execute_registered_rule(
                "GRN-EVENT-004",
                EventPerRowSheetProfile(
                    observed_row_count=observed_row_count,
                    event_header_eligible_count=event_header_eligible_count,
                    explicit_key_candidate_count=explicit_key_candidate_count,
                    non_competence_date_candidate_count=non_competence_date_candidate_count,
                    excluded_event_marker_count=excluded_event_marker_count,
                    event_marker_formula_count=event_marker_formula_count,
                    ambiguity_count=ambiguity_count,
                ),
            )
            if event_per_row_candidates:
                grain_candidates[sheet_id] = event_per_row_candidates + grain_candidates.get(sheet_id, [])
        if get_rule_execution_record("GRN-ENTITY-003").status == "executable_draft":
            observed_row_count = max(column.missingness.observed_cell_count for column in sheet_columns)
            explicit_key_candidate_count = sum(
                1
                for candidate in grain_candidates.get(sheet_id, [])
                if candidate["rule_id"] == "GRN-EXPL-002"
                and candidate["grain_type"] == "explicit_key_candidate"
            )
            entity_header_eligible_count = sum(
                1 for column in sheet_columns if column.entity_marker_header.header_eligible
            )
            descriptive_attribute_candidate_count = sum(
                1
                for candidate_sheet_id, _, candidates in semantic_candidates
                if candidate_sheet_id == sheet_id
                for candidate in candidates
                if candidate.get("semantic_type") in {
                    "name_or_description_candidate",
                    "category_candidate",
                    "location_candidate",
                    "status_candidate",
                }
            )
            non_competence_date_candidate_count = sum(
                1
                for candidate_sheet_id, _, candidates in semantic_candidates
                if candidate_sheet_id == sheet_id
                for candidate in candidates
                if candidate.get("semantic_type") == "date_generic"
            )
            event_candidate_count = sum(
                1
                for candidate in grain_candidates.get(sheet_id, [])
                if candidate["rule_id"] == "GRN-EVENT-004"
                and candidate["grain_type"] == "event_per_row_candidate"
            )
            measure_candidate_count = sum(
                1
                for candidate_sheet_id, _, candidates in semantic_candidates
                if candidate_sheet_id == sheet_id
                for candidate in candidates
                if candidate.get("semantic_type") in {
                    "actual_candidate",
                    "currency_candidate",
                    "percentage_candidate",
                    "quantity_candidate",
                    "target_or_forecast_candidate",
                }
            )
            sensitive_candidate_count = sum(
                1
                for candidate_sheet_id, _, candidates in sensitivity_candidates
                if candidate_sheet_id == sheet_id
                for candidate in candidates
                if candidate.get("sensitivity") == "personal_data_candidate"
            )
            excluded_entity_marker_count = sum(
                1
                for column in sheet_columns
                if column.entity_marker_header.header_eligible
                and (
                    column.physical_type != "text"
                    or column.formulas.formula_count != 0
                    or column.semantic_identifier.sensitive_header
                )
            )
            entity_marker_formula_count = sum(
                column.formulas.formula_count
                for column in sheet_columns
                if column.entity_marker_header.header_eligible
            )
            ambiguity_count = max(
                0,
                entity_header_eligible_count - 1,
                explicit_key_candidate_count - 1,
            )
            entity_per_row_candidates = execute_registered_rule(
                "GRN-ENTITY-003",
                EntityPerRowSheetProfile(
                    observed_row_count=observed_row_count,
                    entity_header_eligible_count=entity_header_eligible_count,
                    explicit_key_candidate_count=explicit_key_candidate_count,
                    descriptive_attribute_candidate_count=descriptive_attribute_candidate_count,
                    non_competence_date_candidate_count=non_competence_date_candidate_count,
                    event_candidate_count=event_candidate_count,
                    measure_candidate_count=measure_candidate_count,
                    sensitive_candidate_count=sensitive_candidate_count,
                    excluded_entity_marker_count=excluded_entity_marker_count,
                    entity_marker_formula_count=entity_marker_formula_count,
                    ambiguity_count=ambiguity_count,
                ),
            )
            if entity_per_row_candidates:
                grain_candidates[sheet_id] = entity_per_row_candidates + grain_candidates.get(sheet_id, [])
        if get_rule_execution_record("MDL-FACTPER-001").status == "executable_draft":
            table_candidates[sheet_id] = execute_registered_rule("MDL-FACTPER-001", PeriodicFactSheetProfile(
                observed_row_count=max(column.missingness.observed_cell_count for column in sheet_columns),
                grain_available=bool(grain_candidates.get(sheet_id)),
                periodic_dates=tuple(
                    column.periodic_date for column in sheet_columns
                    if column.semantic_date.recognized_date_ratio == 1.0
                ),
                eligible_measure_column_count=sum(
                    1 for column in sheet_columns
                    if column.physical_type == "numeric" and column.formulas.formula_count == 0
                ),
            ))
        if get_rule_execution_record("MDL-FACTTXN-002").status == "executable_draft":
            table_candidates.setdefault(sheet_id, []).extend(execute_registered_rule(
                "MDL-FACTTXN-002",
                TransactionalFactSheetProfile(
                    observed_row_count=max(column.missingness.observed_cell_count for column in sheet_columns),
                    grain_available=bool(grain_candidates.get(sheet_id)),
                    transactional_dates=tuple(
                        column.transactional_date for column in sheet_columns
                        if column.semantic_date.recognized_date_ratio == 1.0
                    ),
                    eligible_measure_column_count=sum(
                        1 for column in sheet_columns
                        if column.physical_type == "numeric" and column.formulas.formula_count == 0
                    ),
                ),
            ))
        if get_rule_execution_record("MDL-DIMSTD-004").status == "executable_draft":
            table_candidates.setdefault(sheet_id, []).extend(execute_registered_rule(
                "MDL-DIMSTD-004",
                StandardDimensionSheetProfile(
                    observed_row_count=max(column.missingness.observed_cell_count for column in sheet_columns),
                    grain_available=bool(grain_candidates.get(sheet_id)),
                    individually_unique_identifier_count=sum(
                        1 for column in sheet_columns
                        if classify_identifier(SemanticIdentifierColumnProfile(
                            physical_type=column.physical_type,
                            formula_count=column.formulas.formula_count,
                            semantic_identifier=column.semantic_identifier,
                        ))
                        and column.semantic_identifier.non_missing_ratio == 1.0
                        and column.semantic_identifier.distinct_ratio == 1.0
                    ),
                    descriptive_attribute_count=sum(
                        1 for column in sheet_columns
                        if column.physical_type == "text"
                        and column.formulas.formula_count == 0
                        and not column.semantic_identifier.sensitive_header
                        and not classify_identifier(SemanticIdentifierColumnProfile(
                            physical_type=column.physical_type,
                            formula_count=column.formulas.formula_count,
                            semantic_identifier=column.semantic_identifier,
                        ))
                        and column.semantic_date.recognized_date_ratio != 1.0
                        and 0.05 <= column.semantic_identifier.distinct_ratio <= 0.90
                    ),
                    eligible_measure_column_count=sum(
                        1 for column in sheet_columns
                        if column.physical_type == "numeric" and column.formulas.formula_count == 0
                    ),
                    fully_recognized_temporal_column_count=sum(
                        1 for column in sheet_columns
                        if column.semantic_date.recognized_date_ratio == 1.0
                    ),
                ),
            ))
        if get_rule_execution_record("MDL-DIMCAL-006").status == "executable_draft":
            table_candidates.setdefault(sheet_id, []).extend(execute_registered_rule(
                "MDL-DIMCAL-006",
                CalendarDimensionSheetProfile(
                    observed_row_count=max(column.missingness.observed_cell_count for column in sheet_columns),
                    grain_available=bool(grain_candidates.get(sheet_id)),
                    calendar_dates=tuple(
                        column.calendar_date for column in sheet_columns
                        if column.semantic_date.recognized_date_ratio == 1.0
                    ),
                    eligible_measure_column_count=sum(
                        1 for column in sheet_columns
                        if column.physical_type == "numeric" and column.formulas.formula_count == 0
                    ),
                ),
            ))
        if get_rule_execution_record("MDL-FACTNOGRAIN-019").status == "executable_draft":
            fact_signal_types = {
                "actual_candidate",
                "currency_candidate",
                "percentage_candidate",
                "quantity_candidate",
                "target_or_forecast_candidate",
            }
            fact_signal_sets = tuple(
                frozenset(
                    str(candidate["semantic_type"])
                    for candidate in candidates
                    if candidate.get("semantic_type") in fact_signal_types
                )
                for candidate_sheet_id, _, candidates in semantic_candidates
                if candidate_sheet_id == sheet_id
            )
            fact_signal_count = sum(len(signal_set) for signal_set in fact_signal_sets)
            fact_signal_ambiguity_count = sum(
                1 for signal_set in fact_signal_sets if len(signal_set) > 1
            )
            dimensional_candidate_count = sum(
                1
                for candidate in table_candidates.get(sheet_id, [])
                if str(candidate.get("classification_type", "")).startswith("dimension_")
            )
            sensitive_candidate_count = sum(
                1
                for candidate_sheet_id, _, candidates in sensitivity_candidates
                if candidate_sheet_id == sheet_id
                for candidate in candidates
                if candidate.get("sensitivity") == "personal_data_candidate"
            ) + sum(
                1 for column in sheet_columns if column.semantic_identifier.sensitive_header
            )
            incompatible_temporal_signal_count = sum(
                1
                for column in sheet_columns
                if 0.0 < column.semantic_date.recognized_date_ratio < 1.0
            )
            table_candidates.setdefault(sheet_id, []).extend(execute_registered_rule(
                "MDL-FACTNOGRAIN-019",
                FactWithoutDefinedGrainSheetProfile(
                    observed_row_count=max(column.missingness.observed_cell_count for column in sheet_columns),
                    eligible_numeric_measure_count=sum(
                        1 for column in sheet_columns
                        if column.physical_type == "numeric" and column.formulas.formula_count == 0
                    ),
                    fact_signal_count=fact_signal_count,
                    active_grain_hypothesis_count=len(grain_candidates.get(sheet_id, [])),
                    dimensional_candidate_count=dimensional_candidate_count,
                    formula_column_count=sum(
                        column.formulas.formula_count for column in sheet_columns
                    ),
                    sensitive_candidate_count=sensitive_candidate_count,
                    incompatible_temporal_signal_count=incompatible_temporal_signal_count,
                    ambiguity_count=fact_signal_ambiguity_count,
                ),
            ))
        if get_rule_execution_record("MDL-UNDEFINED-020").status == "executable_draft":
            closed_table_classifier_ids = (
                "MDL-FACTPER-001",
                "MDL-FACTTXN-002",
                "MDL-DIMSTD-004",
                "MDL-DIMCAL-006",
                "MDL-FACTNOGRAIN-019",
            )
            positive_classification_types = frozenset(
                str(candidate.get("classification_type", ""))
                for candidate in table_candidates.get(sheet_id, [])
                if candidate.get("classification_type")
            )
            residual_sensitive_candidate_count = sum(
                1
                for candidate_sheet_id, _, candidates in sensitivity_candidates
                if candidate_sheet_id == sheet_id
                for candidate in candidates
                if candidate.get("sensitivity") == "personal_data_candidate"
            ) + sum(
                1 for column in sheet_columns if column.semantic_identifier.sensitive_header
            )
            classification_conflict_count = max(0, len(positive_classification_types) - 1)
            table_candidates.setdefault(sheet_id, []).extend(execute_registered_rule(
                "MDL-UNDEFINED-020",
                UndefinedTableClassificationSheetProfile(
                    observed_row_count=max(column.missingness.observed_cell_count for column in sheet_columns),
                    physical_column_count=len(sheet_columns),
                    evaluated_table_classifier_count=sum(
                        1
                        for rule_id in closed_table_classifier_ids
                        if get_rule_execution_record(rule_id).status == "executable_draft"
                    ),
                    positive_table_classification_count=len(positive_classification_types),
                    classification_conflict_count=classification_conflict_count,
                    formula_column_count=sum(column.formulas.formula_count for column in sheet_columns),
                    sensitive_candidate_count=residual_sensitive_candidate_count,
                    classification_ambiguity_count=classification_conflict_count,
                ),
            ))

    relationship_candidates: list[tuple[str, str, list[dict[str, object]]]] = []
    relationship_rule_statuses = {
        "REL-ONEMANY-001": get_rule_execution_record("REL-ONEMANY-001").status,
        "REL-NONUNIQ-002": get_rule_execution_record("REL-NONUNIQ-002").status,
        "REL-ORPHAN-003": get_rule_execution_record("REL-ORPHAN-003").status,
        "REL-MANYMANY-004": get_rule_execution_record("REL-MANYMANY-004").status,
        "REL-FACTFACT-006": get_rule_execution_record("REL-FACTFACT-006").status,
        "REL-AMBIG-007": get_rule_execution_record("REL-AMBIG-007").status,
        "REL-BIDIR-008": get_rule_execution_record("REL-BIDIR-008").status,
        "REL-COMPKEY-009": get_rule_execution_record("REL-COMPKEY-009").status,
        "REL-CONFORMED-010": get_rule_execution_record("REL-CONFORMED-010").status,
    }
    metric_rule_statuses = {
        "MET-COMPL-001": get_rule_execution_record("MET-COMPL-001").status,
        "MET-SUM-002": get_rule_execution_record("MET-SUM-002").status,
        "MET-COUNT-003": get_rule_execution_record("MET-COUNT-003").status,
        "MET-DCOUNT-004": get_rule_execution_record("MET-DCOUNT-004").status,
        "MET-AVG-005": get_rule_execution_record("MET-AVG-005").status,
        "MET-MINMAX-006": get_rule_execution_record("MET-MINMAX-006").status,
        "MET-RATE-007": get_rule_execution_record("MET-RATE-007").status,
        "MET-ABSDELTA-008": get_rule_execution_record("MET-ABSDELTA-008").status,
        "MET-PCTDELTA-009": get_rule_execution_record("MET-PCTDELTA-009").status,
        "MET-RUNNING-010": get_rule_execution_record("MET-RUNNING-010").status,
        "MET-WAVG-011": get_rule_execution_record("MET-WAVG-011").status,
        "MET-SEMIADD-012": get_rule_execution_record("MET-SEMIADD-012").status,
        "MET-DOMAIN-013": get_rule_execution_record("MET-DOMAIN-013").status,
        "MET-IMPOSS-014": get_rule_execution_record("MET-IMPOSS-014").status,
        "MET-DAX-015": get_rule_execution_record("MET-DAX-015").status,
    }
    alert_rule_statuses = {
        "ALT-SENS-001": get_rule_execution_record("ALT-SENS-001").status,
        "ALT-QUALITY-002": get_rule_execution_record("ALT-QUALITY-002").status,
        "ALT-GRAIN-003": get_rule_execution_record("ALT-GRAIN-003").status,
        "ALT-KEY-004": get_rule_execution_record("ALT-KEY-004").status,
        "ALT-AMBIG-005": get_rule_execution_record("ALT-AMBIG-005").status,
        "ALT-METRIC-006": get_rule_execution_record("ALT-METRIC-006").status,
        "ALT-SUMPCT-007": get_rule_execution_record("ALT-SUMPCT-007").status,
        "ALT-AVGAVG-008": get_rule_execution_record("ALT-AVGAVG-008").status,
    }
    if "executable_draft" in relationship_rule_statuses.values():
        classification_types_by_sheet = {
            sheet_id: frozenset(
                str(candidate.get("classification_type", ""))
                for candidate in candidates
                if candidate.get("classification_type")
            )
            for sheet_id, candidates in table_candidates.items()
        }
        sensitive_sheet_ids = {
            sheet_id
            for sheet_id, _, candidates in sensitivity_candidates
            if any(candidate.get("sensitivity") == "personal_data_candidate" for candidate in candidates)
        } | {
            sheet_id
            for sheet_id, sheet_columns in grouped_columns.items()
            if any(column.semantic_identifier.sensitive_header for column in sheet_columns)
        }
        source_key_counts = {
            sheet_id: len(
                {
                    signal.source_column_id
                    for signal in relationship_pair_signals
                    if signal.source_sheet_id == sheet_id
                    and signal.source_complete
                    and signal.source_unique
                    and not signal.source_or_target_sensitive
                    and not signal.source_or_target_has_formula
                }
            )
            for sheet_id in grouped_columns
        }
        target_reference_counts = {
            sheet_id: len(
                {
                    signal.target_column_id
                    for signal in relationship_pair_signals
                    if signal.target_sheet_id == sheet_id
                    and signal.target_complete
                    and not signal.target_unique
                    and not signal.source_or_target_sensitive
                    and not signal.source_or_target_has_formula
                }
            )
            for sheet_id in grouped_columns
        }
        non_unique_source_key_counts = {
            sheet_id: len(
                {
                    signal.source_column_id
                    for signal in relationship_pair_signals
                    if signal.source_sheet_id == sheet_id
                    and signal.source_complete
                    and not signal.source_unique
                    and signal.source_distinct_count < signal.source_non_missing_count
                    and not signal.source_or_target_sensitive
                    and not signal.source_or_target_has_formula
                }
            )
            for sheet_id in grouped_columns
        }
        complete_target_reference_counts = {
            sheet_id: len(
                {
                    signal.target_column_id
                    for signal in relationship_pair_signals
                    if signal.target_sheet_id == sheet_id
                    and signal.target_complete
                    and not signal.source_or_target_sensitive
                    and not signal.source_or_target_has_formula
                }
            )
            for sheet_id in grouped_columns
        }
        eligible_direction_counts = {
            (source_sheet_id, target_sheet_id): sum(
                1
                for signal in relationship_pair_signals
                if signal.source_sheet_id == source_sheet_id
                and signal.target_sheet_id == target_sheet_id
                and signal.source_complete
                and signal.source_unique
                and signal.target_complete
                and not signal.target_unique
                and signal.referential_coverage_ratio == 1.0
                and not signal.source_or_target_sensitive
                and not signal.source_or_target_has_formula
            )
            for source_sheet_id in grouped_columns
            for target_sheet_id in grouped_columns
            if source_sheet_id != target_sheet_id
        }
        non_unique_direction_counts = {
            (source_sheet_id, target_sheet_id): sum(
                1
                for signal in relationship_pair_signals
                if signal.source_sheet_id == source_sheet_id
                and signal.target_sheet_id == target_sheet_id
                and signal.source_complete
                and not signal.source_unique
                and signal.source_distinct_count < signal.source_non_missing_count
                and signal.target_complete
                and signal.referential_coverage_ratio == 1.0
                and not signal.source_or_target_sensitive
                and not signal.source_or_target_has_formula
            )
            for source_sheet_id in grouped_columns
            for target_sheet_id in grouped_columns
            if source_sheet_id != target_sheet_id
        }
        orphan_direction_counts = {
            (source_sheet_id, target_sheet_id): sum(
                1
                for signal in relationship_pair_signals
                if signal.source_sheet_id == source_sheet_id
                and signal.target_sheet_id == target_sheet_id
                and signal.source_complete
                and signal.source_unique
                and signal.target_complete
                and not signal.target_unique
                and 0.0 < signal.referential_coverage_ratio < 1.0
                and signal.uncovered_reference_distinct_count > 0
                and not signal.source_or_target_sensitive
                and not signal.source_or_target_has_formula
            )
            for source_sheet_id in grouped_columns
            for target_sheet_id in grouped_columns
            if source_sheet_id != target_sheet_id
        }
        many_to_many_direction_counts = {
            (source_sheet_id, target_sheet_id): sum(
                1
                for signal in relationship_pair_signals
                if signal.source_sheet_id == source_sheet_id
                and signal.target_sheet_id == target_sheet_id
                and signal.source_complete
                and not signal.source_unique
                and signal.source_distinct_count < signal.source_non_missing_count
                and signal.target_complete
                and not signal.target_unique
                and signal.target_distinct_count < signal.target_non_missing_count
                and signal.referential_coverage_ratio == 1.0
                and not signal.source_or_target_sensitive
                and not signal.source_or_target_has_formula
            )
            for source_sheet_id in grouped_columns
            for target_sheet_id in grouped_columns
            if source_sheet_id != target_sheet_id
        }
        simple_key_pair_directions = {
            (signal.source_sheet_id, signal.target_sheet_id)
            for signal in relationship_pair_signals
            if signal.source_complete
            and signal.source_unique
            and signal.target_complete
            and not signal.target_unique
            and signal.referential_coverage_ratio == 1.0
            and not signal.source_or_target_sensitive
            and not signal.source_or_target_has_formula
        }
        connected_fact_counts_by_dimension = {
            source_sheet_id: len({
                signal.target_sheet_id
                for signal in relationship_pair_signals
                if signal.source_sheet_id == source_sheet_id
                and signal.source_complete
                and signal.source_unique
                and signal.target_complete
                and not signal.target_unique
                and signal.referential_coverage_ratio == 1.0
                and eligible_direction_counts[(signal.source_sheet_id, signal.target_sheet_id)] == 1
                and not signal.source_or_target_sensitive
                and not signal.source_or_target_has_formula
                and "dimension_standard_candidate" in classification_types_by_sheet.get(signal.source_sheet_id, frozenset())
                and bool({"fact_transactional_candidate", "fact_periodic_candidate"} & classification_types_by_sheet.get(signal.target_sheet_id, frozenset()))
            })
            for source_sheet_id in grouped_columns
        }
        emitted_ambiguous_relationship_pairs: set[tuple[str, str]] = set()
        for signal in relationship_pair_signals:
            source_types = classification_types_by_sheet.get(signal.source_sheet_id, frozenset())
            target_types = classification_types_by_sheet.get(signal.target_sheet_id, frozenset())
            source_conflict_count = max(0, len(source_types) - 1)
            target_conflict_count = max(0, len(target_types) - 1)
            common_profile = {
                "source_standard_dimension_candidate": "dimension_standard_candidate" in source_types,
                "target_fact_candidate": bool({"fact_transactional_candidate", "fact_periodic_candidate"} & target_types),
                "source_calendar_dimension_candidate": "dimension_calendar_candidate" in source_types,
                "source_or_target_undefined_candidate": "table_classification_undefined_candidate" in source_types | target_types,
                "source_or_target_fact_without_grain_candidate": "fact_without_defined_grain_candidate" in source_types | target_types,
                "source_or_target_classification_conflict": source_conflict_count > 0 or target_conflict_count > 0,
                "source_or_target_sensitive": signal.source_or_target_sensitive or signal.source_sheet_id in sensitive_sheet_ids or signal.target_sheet_id in sensitive_sheet_ids,
                "source_or_target_has_formula": signal.source_or_target_has_formula,
                "self_reference": signal.source_sheet_id == signal.target_sheet_id,
                "dimension_key_complete": signal.source_complete,
                "fact_reference_complete": signal.target_complete,
                "referential_coverage_ratio": signal.referential_coverage_ratio,
                "has_one_to_one_pattern": signal.source_complete and signal.source_unique and signal.target_complete and signal.target_unique and signal.referential_coverage_ratio == 1.0,
                "has_many_to_many_pattern": not signal.source_unique and not signal.target_unique,
                "ambiguity_count": source_conflict_count + target_conflict_count,
            }
            if relationship_rule_statuses["REL-ONEMANY-001"] == "executable_draft":
                one_to_many_profile = OneToManyRelationshipPairProfile(
                    **common_profile,
                    eligible_dimension_key_count=source_key_counts[signal.source_sheet_id],
                    eligible_fact_reference_count=target_reference_counts[signal.target_sheet_id],
                    dimension_key_unique=signal.source_unique,
                    fact_reference_unique=signal.target_unique,
                    eligible_direction_count=eligible_direction_counts[(signal.source_sheet_id, signal.target_sheet_id)],
                )
                candidate = execute_registered_rule("REL-ONEMANY-001", one_to_many_profile)
                if candidate:
                    relationship_candidates.append((signal.source_sheet_id, signal.target_sheet_id, [candidate]))
            if relationship_rule_statuses["REL-NONUNIQ-002"] == "executable_draft":
                non_unique_profile = NonUniqueOneSideRelationshipPairProfile(
                    **common_profile,
                    eligible_dimension_key_count=non_unique_source_key_counts[signal.source_sheet_id],
                    eligible_fact_reference_count=complete_target_reference_counts[signal.target_sheet_id],
                    dimension_key_unique=signal.source_unique,
                    dimension_key_duplicate_count=max(0, signal.source_non_missing_count - signal.source_distinct_count),
                    eligible_direction_count=non_unique_direction_counts[(signal.source_sheet_id, signal.target_sheet_id)],
                )
                candidate = execute_registered_rule("REL-NONUNIQ-002", non_unique_profile)
                if candidate:
                    relationship_candidates.append((signal.source_sheet_id, signal.target_sheet_id, [candidate]))
            if relationship_rule_statuses["REL-ORPHAN-003"] == "executable_draft":
                orphan_profile = OrphanReferenceRelationshipPairProfile(
                    **common_profile,
                    eligible_dimension_key_count=source_key_counts[signal.source_sheet_id],
                    eligible_fact_reference_count=target_reference_counts[signal.target_sheet_id],
                    dimension_key_unique=signal.source_unique,
                    fact_reference_unique=signal.target_unique,
                    uncovered_reference_distinct_count=signal.uncovered_reference_distinct_count,
                    eligible_direction_count=orphan_direction_counts[(signal.source_sheet_id, signal.target_sheet_id)],
                )
                candidate = execute_registered_rule("REL-ORPHAN-003", orphan_profile)
                if candidate:
                    relationship_candidates.append((signal.source_sheet_id, signal.target_sheet_id, [candidate]))
            if relationship_rule_statuses["REL-MANYMANY-004"] == "executable_draft":
                many_to_many_profile = ManyToManyRelationshipPairProfile(
                    **common_profile,
                    eligible_dimension_key_count=non_unique_source_key_counts[signal.source_sheet_id],
                    eligible_fact_reference_count=target_reference_counts[signal.target_sheet_id],
                    dimension_key_unique=signal.source_unique,
                    fact_reference_unique=signal.target_unique,
                    eligible_direction_count=many_to_many_direction_counts[(signal.source_sheet_id, signal.target_sheet_id)],
                )
                candidate = execute_registered_rule("REL-MANYMANY-004", many_to_many_profile)
                if candidate:
                    relationship_candidates.append((signal.source_sheet_id, signal.target_sheet_id, [candidate]))
            if relationship_rule_statuses["REL-FACTFACT-006"] == "executable_draft":
                direct_fact_profile = DirectFactRelationshipPairProfile(
                    source_fact_candidate=bool({"fact_transactional_candidate", "fact_periodic_candidate"} & source_types),
                    target_fact_candidate=bool({"fact_transactional_candidate", "fact_periodic_candidate"} & target_types),
                    source_or_target_dimension_candidate=bool(
                        {"dimension_standard_candidate", "dimension_calendar_candidate"} & (source_types | target_types)
                    ),
                    source_or_target_undefined_candidate=common_profile["source_or_target_undefined_candidate"],
                    source_or_target_fact_without_grain_candidate=common_profile["source_or_target_fact_without_grain_candidate"],
                    source_or_target_classification_conflict=common_profile["source_or_target_classification_conflict"],
                    source_or_target_sensitive=common_profile["source_or_target_sensitive"],
                    source_or_target_has_formula=common_profile["source_or_target_has_formula"],
                    self_reference=common_profile["self_reference"],
                    eligible_source_key_count=source_key_counts[signal.source_sheet_id],
                    eligible_target_reference_count=target_reference_counts[signal.target_sheet_id],
                    source_key_complete=signal.source_complete,
                    source_key_unique=signal.source_unique,
                    target_reference_complete=signal.target_complete,
                    target_reference_unique=signal.target_unique,
                    referential_coverage_ratio=signal.referential_coverage_ratio,
                    eligible_direction_count=eligible_direction_counts[(signal.source_sheet_id, signal.target_sheet_id)],
                    has_one_to_one_pattern=common_profile["has_one_to_one_pattern"],
                    has_many_to_many_pattern=common_profile["has_many_to_many_pattern"],
                    ambiguity_count=common_profile["ambiguity_count"],
                )
                candidate = execute_registered_rule("REL-FACTFACT-006", direct_fact_profile)
                if candidate:
                    relationship_candidates.append((signal.source_sheet_id, signal.target_sheet_id, [candidate]))
            pair_key = (signal.source_sheet_id, signal.target_sheet_id)
            if (
                relationship_rule_statuses["REL-AMBIG-007"] == "executable_draft"
                and pair_key not in emitted_ambiguous_relationship_pairs
            ):
                ambiguous_profile = AmbiguousRelationshipPathPairProfile(
                    source_standard_dimension_candidate=common_profile["source_standard_dimension_candidate"],
                    target_fact_candidate=common_profile["target_fact_candidate"],
                    source_or_target_calendar_dimension_candidate=bool(
                        "dimension_calendar_candidate" in source_types | target_types
                    ),
                    source_or_target_undefined_candidate=common_profile["source_or_target_undefined_candidate"],
                    source_or_target_fact_without_grain_candidate=common_profile["source_or_target_fact_without_grain_candidate"],
                    source_or_target_classification_conflict=common_profile["source_or_target_classification_conflict"],
                    source_or_target_sensitive=common_profile["source_or_target_sensitive"],
                    source_or_target_has_formula=common_profile["source_or_target_has_formula"],
                    self_reference=common_profile["self_reference"],
                    eligible_source_key_count=source_key_counts[signal.source_sheet_id],
                    eligible_target_reference_count=target_reference_counts[signal.target_sheet_id],
                    source_key_complete=signal.source_complete,
                    source_key_unique=signal.source_unique,
                    target_reference_complete=signal.target_complete,
                    target_reference_unique=signal.target_unique,
                    referential_coverage_ratio=signal.referential_coverage_ratio,
                    eligible_direction_count=eligible_direction_counts[pair_key],
                    has_one_to_one_pattern=common_profile["has_one_to_one_pattern"],
                    has_many_to_many_pattern=common_profile["has_many_to_many_pattern"],
                    ambiguity_count=common_profile["ambiguity_count"],
                )
                candidate = execute_registered_rule("REL-AMBIG-007", ambiguous_profile)
                if candidate:
                    relationship_candidates.append((signal.source_sheet_id, signal.target_sheet_id, [candidate]))
                    emitted_ambiguous_relationship_pairs.add(pair_key)
            if relationship_rule_statuses["REL-BIDIR-008"] == "executable_draft":
                bidirectional_filter_profile = BidirectionalFilterReviewPairProfile(
                    **common_profile,
                    eligible_dimension_key_count=source_key_counts[signal.source_sheet_id],
                    eligible_fact_reference_count=target_reference_counts[signal.target_sheet_id],
                    dimension_key_unique=signal.source_unique,
                    fact_reference_unique=signal.target_unique,
                    eligible_direction_count=eligible_direction_counts[pair_key],
                )
                candidate = execute_registered_rule("REL-BIDIR-008", bidirectional_filter_profile)
                if candidate:
                    relationship_candidates.append((signal.source_sheet_id, signal.target_sheet_id, [candidate]))
            if relationship_rule_statuses["REL-CONFORMED-010"] == "executable_draft":
                conformed_profile = ConformedDimensionPairProfile(
                    **common_profile,
                    eligible_dimension_key_count=source_key_counts[signal.source_sheet_id],
                    eligible_fact_reference_count=target_reference_counts[signal.target_sheet_id],
                    dimension_key_unique=signal.source_unique,
                    fact_reference_unique=signal.target_unique,
                    eligible_direction_count=eligible_direction_counts[pair_key],
                    connected_fact_count=connected_fact_counts_by_dimension[signal.source_sheet_id],
                )
                candidate = execute_registered_rule("REL-CONFORMED-010", conformed_profile)
                if candidate:
                    relationship_candidates.append((signal.source_sheet_id, signal.target_sheet_id, [candidate]))
        if relationship_rule_statuses["REL-COMPKEY-009"] == "executable_draft":
            for signal in composite_relationship_pair_signals:
                source_types = classification_types_by_sheet.get(signal.source_sheet_id, frozenset())
                target_types = classification_types_by_sheet.get(signal.target_sheet_id, frozenset())
                source_conflict_count = max(0, len(source_types) - 1)
                target_conflict_count = max(0, len(target_types) - 1)
                composite_profile = CompositeRelationshipKeyPairProfile(
                    source_standard_dimension_candidate="dimension_standard_candidate" in source_types,
                    target_fact_candidate=bool({"fact_transactional_candidate", "fact_periodic_candidate"} & target_types),
                    source_calendar_dimension_candidate="dimension_calendar_candidate" in source_types,
                    source_or_target_undefined_candidate="table_classification_undefined_candidate" in source_types | target_types,
                    source_or_target_fact_without_grain_candidate="fact_without_defined_grain_candidate" in source_types | target_types,
                    source_or_target_classification_conflict=source_conflict_count > 0 or target_conflict_count > 0,
                    source_or_target_sensitive=(
                        signal.source_or_target_sensitive
                        or signal.source_sheet_id in sensitive_sheet_ids
                        or signal.target_sheet_id in sensitive_sheet_ids
                    ),
                    source_or_target_has_formula=signal.source_or_target_has_formula,
                    self_reference=signal.source_sheet_id == signal.target_sheet_id,
                    eligible_composite_key_pair_count=signal.eligible_composite_key_pair_count,
                    eligible_composite_reference_pair_count=signal.eligible_composite_reference_pair_count,
                    has_eligible_simple_key=(signal.source_sheet_id, signal.target_sheet_id) in simple_key_pair_directions,
                    composite_key_complete=signal.composite_key_complete,
                    composite_key_unique=signal.composite_key_unique,
                    composite_reference_complete=signal.composite_reference_complete,
                    composite_reference_unique=signal.composite_reference_unique,
                    referential_coverage_ratio=signal.referential_coverage_ratio,
                    eligible_direction_count=signal.eligible_direction_count,
                    has_one_to_one_pattern=signal.has_one_to_one_pattern,
                    has_many_to_many_pattern=signal.has_many_to_many_pattern,
                    ambiguity_count=source_conflict_count + target_conflict_count,
                )
                candidate = execute_registered_rule("REL-COMPKEY-009", composite_profile)
                if candidate:
                    relationship_candidates.append((signal.source_sheet_id, signal.target_sheet_id, [candidate]))

    metric_candidates: list[tuple[str, list[dict[str, object]]]] = []
    if "executable_draft" in metric_rule_statuses.values():
        for sheet_id, sheet_columns in grouped_columns.items():
            status_candidate_count = sum(
                1
                for candidate_sheet_id, _, candidates in semantic_candidates
                if candidate_sheet_id == sheet_id
                for candidate in candidates
                if candidate.get("semantic_type") == "status_candidate"
            )
            grain_rule_ids = {
                str(candidate["rule_id"])
                for candidate in grain_candidates.get(sheet_id, [])
                if candidate.get("rule_id") in {"GRN-COMP-001", "GRN-EVENT-004", "GRN-ENTITY-003", "GRN-EXPL-002"}
            }
            classification_types = {
                str(candidate["classification_type"])
                for candidate in table_candidates.get(sheet_id, [])
                if candidate.get("classification_type")
            }
            metric_profile = CompletionRateConceptProfile(
                row_count=max(column.missingness.observed_cell_count for column in sheet_columns),
                physical_column_count=len(sheet_columns),
                status_candidate_count=status_candidate_count,
                has_defined_grain=bool(grain_rule_ids),
                grain_ambiguity_count=max(0, len(grain_rule_ids) - 1),
                has_undefined_classification="table_classification_undefined_candidate" in classification_types,
                has_fact_without_grain="fact_without_defined_grain_candidate" in classification_types,
                classification_conflict_count=max(0, len(classification_types) - 1),
                has_sensitive_signal=any(
                    candidate.get("sensitivity") == "personal_data_candidate"
                    for candidate_sheet_id, _, candidates in sensitivity_candidates
                    if candidate_sheet_id == sheet_id
                    for candidate in candidates
                ),
                has_formula_signal=any(column.formulas.formula_count > 0 for column in sheet_columns),
            )
            candidate = execute_registered_rule("MET-COMPL-001", metric_profile)
            if candidate:
                metric_candidates.append((sheet_id, [candidate]))
            if metric_rule_statuses["MET-SUM-002"] == "executable_draft":
                summable_candidate_count = sum(
                    1
                    for candidate_sheet_id, _, candidates in semantic_candidates
                    if candidate_sheet_id == sheet_id
                    for candidate in candidates
                    if candidate.get("semantic_type") in {"quantity_candidate", "currency_candidate"}
                )
                sum_profile = SumConceptProfile(
                    row_count=max(column.missingness.observed_cell_count for column in sheet_columns),
                    physical_column_count=len(sheet_columns),
                    summable_candidate_count=summable_candidate_count,
                    has_defined_grain=bool(grain_rule_ids), grain_ambiguity_count=max(0, len(grain_rule_ids) - 1),
                    has_undefined_classification="table_classification_undefined_candidate" in classification_types,
                    has_fact_without_grain="fact_without_defined_grain_candidate" in classification_types,
                    classification_conflict_count=max(0, len(classification_types) - 1),
                    has_sensitive_signal=any(candidate.get("sensitivity") == "personal_data_candidate" for candidate_sheet_id, _, candidates in sensitivity_candidates if candidate_sheet_id == sheet_id for candidate in candidates),
                    has_formula_signal=any(column.formulas.formula_count > 0 for column in sheet_columns),
                )
                candidate = execute_registered_rule("MET-SUM-002", sum_profile)
                if candidate:
                    metric_candidates.append((sheet_id, [candidate]))
            if metric_rule_statuses["MET-COUNT-003"] == "executable_draft":
                entity_candidate_count = sum(1 for candidate_sheet_id, _, candidates in semantic_candidates if candidate_sheet_id == sheet_id for candidate in candidates if candidate.get("semantic_type") == "identifier_candidate")
                count_profile = CountConceptProfile(row_count=max(column.missingness.observed_cell_count for column in sheet_columns), physical_column_count=len(sheet_columns), entity_candidate_count=entity_candidate_count, has_defined_grain=bool(grain_rule_ids), grain_ambiguity_count=max(0, len(grain_rule_ids) - 1), has_undefined_classification="table_classification_undefined_candidate" in classification_types, has_fact_without_grain="fact_without_defined_grain_candidate" in classification_types, classification_conflict_count=max(0, len(classification_types) - 1), has_sensitive_signal=any(candidate.get("sensitivity") == "personal_data_candidate" for candidate_sheet_id, _, candidates in sensitivity_candidates if candidate_sheet_id == sheet_id for candidate in candidates), has_formula_signal=any(column.formulas.formula_count > 0 for column in sheet_columns))
                candidate = execute_registered_rule("MET-COUNT-003", count_profile)
                if candidate:
                    metric_candidates.append((sheet_id, [candidate]))
            if metric_rule_statuses["MET-DCOUNT-004"] == "executable_draft":
                entity_candidate_count = sum(1 for candidate_sheet_id, _, candidates in semantic_candidates if candidate_sheet_id == sheet_id for candidate in candidates if candidate.get("semantic_type") == "identifier_candidate")
                distinct_count_profile = DistinctCountConceptProfile(row_count=max(column.missingness.observed_cell_count for column in sheet_columns), physical_column_count=len(sheet_columns), entity_candidate_count=entity_candidate_count, has_defined_grain=bool(grain_rule_ids), grain_ambiguity_count=max(0, len(grain_rule_ids) - 1), has_undefined_classification="table_classification_undefined_candidate" in classification_types, has_fact_without_grain="fact_without_defined_grain_candidate" in classification_types, classification_conflict_count=max(0, len(classification_types) - 1), has_sensitive_signal=any(candidate.get("sensitivity") == "personal_data_candidate" for candidate_sheet_id, _, candidates in sensitivity_candidates if candidate_sheet_id == sheet_id for candidate in candidates), has_formula_signal=any(column.formulas.formula_count > 0 for column in sheet_columns))
                candidate = execute_registered_rule("MET-DCOUNT-004", distinct_count_profile)
                if candidate:
                    metric_candidates.append((sheet_id, [candidate]))
            if metric_rule_statuses["MET-AVG-005"] == "executable_draft":
                summable_candidate_count = sum(1 for candidate_sheet_id, _, candidates in semantic_candidates if candidate_sheet_id == sheet_id for candidate in candidates if candidate.get("semantic_type") in {"quantity_candidate", "currency_candidate"})
                average_profile = AverageConceptProfile(row_count=max(column.missingness.observed_cell_count for column in sheet_columns), physical_column_count=len(sheet_columns), summable_candidate_count=summable_candidate_count, has_defined_grain=bool(grain_rule_ids), grain_ambiguity_count=max(0, len(grain_rule_ids) - 1), has_undefined_classification="table_classification_undefined_candidate" in classification_types, has_fact_without_grain="fact_without_defined_grain_candidate" in classification_types, classification_conflict_count=max(0, len(classification_types) - 1), has_sensitive_signal=any(candidate.get("sensitivity") == "personal_data_candidate" for candidate_sheet_id, _, candidates in sensitivity_candidates if candidate_sheet_id == sheet_id for candidate in candidates), has_formula_signal=any(column.formulas.formula_count > 0 for column in sheet_columns))
                candidate = execute_registered_rule("MET-AVG-005", average_profile)
                if candidate:
                    metric_candidates.append((sheet_id, [candidate]))
            if metric_rule_statuses["MET-MINMAX-006"] == "executable_draft":
                summable_candidate_count = sum(1 for candidate_sheet_id, _, candidates in semantic_candidates if candidate_sheet_id == sheet_id for candidate in candidates if candidate.get("semantic_type") in {"quantity_candidate", "currency_candidate"})
                minmax_profile = MinMaxConceptProfile(row_count=max(column.missingness.observed_cell_count for column in sheet_columns), physical_column_count=len(sheet_columns), summable_candidate_count=summable_candidate_count, has_defined_grain=bool(grain_rule_ids), grain_ambiguity_count=max(0, len(grain_rule_ids) - 1), has_undefined_classification="table_classification_undefined_candidate" in classification_types, has_fact_without_grain="fact_without_defined_grain_candidate" in classification_types, classification_conflict_count=max(0, len(classification_types) - 1), has_sensitive_signal=any(candidate.get("sensitivity") == "personal_data_candidate" for candidate_sheet_id, _, candidates in sensitivity_candidates if candidate_sheet_id == sheet_id for candidate in candidates), has_formula_signal=any(column.formulas.formula_count > 0 for column in sheet_columns))
                candidate = execute_registered_rule("MET-MINMAX-006", minmax_profile)
                if candidate:
                    metric_candidates.append((sheet_id, [candidate]))
            if metric_rule_statuses["MET-RATE-007"] == "executable_draft":
                semantic_types = [candidate.get("semantic_type") for candidate_sheet_id, _, candidates in semantic_candidates if candidate_sheet_id == sheet_id for candidate in candidates]
                rate_profile = RateConceptProfile(row_count=max(column.missingness.observed_cell_count for column in sheet_columns), physical_column_count=len(sheet_columns), numerator_candidate_count=semantic_types.count("quantity_candidate"), denominator_candidate_count=semantic_types.count("target_or_forecast_candidate"), has_defined_grain=bool(grain_rule_ids), grain_ambiguity_count=max(0, len(grain_rule_ids) - 1), has_undefined_classification="table_classification_undefined_candidate" in classification_types, has_fact_without_grain="fact_without_defined_grain_candidate" in classification_types, classification_conflict_count=max(0, len(classification_types) - 1), has_sensitive_signal=any(candidate.get("sensitivity") == "personal_data_candidate" for candidate_sheet_id, _, candidates in sensitivity_candidates if candidate_sheet_id == sheet_id for candidate in candidates) or any(column.semantic_identifier.sensitive_header for column in sheet_columns), has_formula_signal=any(column.formulas.formula_count > 0 for column in sheet_columns))
                candidate = execute_registered_rule("MET-RATE-007", rate_profile)
                if candidate:
                    metric_candidates.append((sheet_id, [candidate]))
            if metric_rule_statuses["MET-ABSDELTA-008"] == "executable_draft":
                semantic_types = [candidate.get("semantic_type") for candidate_sheet_id, _, candidates in semantic_candidates if candidate_sheet_id == sheet_id for candidate in candidates]
                absolute_delta_profile = AbsoluteDeltaConceptProfile(row_count=max(column.missingness.observed_cell_count for column in sheet_columns), physical_column_count=len(sheet_columns), actual_candidate_count=semantic_types.count("actual_candidate"), baseline_candidate_count=semantic_types.count("target_or_forecast_candidate"), has_defined_grain=bool(grain_rule_ids), grain_ambiguity_count=max(0, len(grain_rule_ids) - 1), has_undefined_classification="table_classification_undefined_candidate" in classification_types, has_fact_without_grain="fact_without_defined_grain_candidate" in classification_types, classification_conflict_count=max(0, len(classification_types) - 1), has_sensitive_signal=any(candidate.get("sensitivity") == "personal_data_candidate" for candidate_sheet_id, _, candidates in sensitivity_candidates if candidate_sheet_id == sheet_id for candidate in candidates) or any(column.semantic_identifier.sensitive_header for column in sheet_columns), has_formula_signal=any(column.formulas.formula_count > 0 for column in sheet_columns))
                candidate = execute_registered_rule("MET-ABSDELTA-008", absolute_delta_profile)
                if candidate:
                    metric_candidates.append((sheet_id, [candidate]))
            if metric_rule_statuses["MET-PCTDELTA-009"] == "executable_draft":
                semantic_types = [candidate.get("semantic_type") for candidate_sheet_id, _, candidates in semantic_candidates if candidate_sheet_id == sheet_id for candidate in candidates]
                percentage_delta_profile = PercentageDeltaConceptProfile(row_count=max(column.missingness.observed_cell_count for column in sheet_columns), physical_column_count=len(sheet_columns), actual_candidate_count=semantic_types.count("actual_candidate"), baseline_candidate_count=semantic_types.count("target_or_forecast_candidate"), baseline_zero_value_count=sum(column.semantic_target.zero_value_count for column in sheet_columns if column.semantic_target.header_eligible), has_defined_grain=bool(grain_rule_ids), grain_ambiguity_count=max(0, len(grain_rule_ids) - 1), has_undefined_classification="table_classification_undefined_candidate" in classification_types, has_fact_without_grain="fact_without_defined_grain_candidate" in classification_types, classification_conflict_count=max(0, len(classification_types) - 1), has_sensitive_signal=any(candidate.get("sensitivity") == "personal_data_candidate" for candidate_sheet_id, _, candidates in sensitivity_candidates if candidate_sheet_id == sheet_id for candidate in candidates) or any(column.semantic_identifier.sensitive_header for column in sheet_columns), has_formula_signal=any(column.formulas.formula_count > 0 for column in sheet_columns))
                candidate = execute_registered_rule("MET-PCTDELTA-009", percentage_delta_profile)
                if candidate:
                    metric_candidates.append((sheet_id, [candidate]))
            if metric_rule_statuses["MET-RUNNING-010"] == "executable_draft":
                semantic_types = [candidate.get("semantic_type") for candidate_sheet_id, _, candidates in semantic_candidates if candidate_sheet_id == sheet_id for candidate in candidates]
                running_total_profile = RunningTotalConceptProfile(row_count=max(column.missingness.observed_cell_count for column in sheet_columns), physical_column_count=len(sheet_columns), measure_candidate_count=semantic_types.count("quantity_candidate") + semantic_types.count("currency_candidate"), temporal_order_candidate_count=semantic_types.count("date_generic"), temporal_order_duplicate_count=sum(max(0, column.semantic_date.recognized_date_count - column.semantic_date.distinct_recognized_date_count) for column in sheet_columns if column.semantic_date.non_missing_count >= 10 and column.semantic_date.recognized_date_ratio == 1.0), has_defined_grain=bool(grain_rule_ids), grain_ambiguity_count=max(0, len(grain_rule_ids) - 1), has_undefined_classification="table_classification_undefined_candidate" in classification_types, has_fact_without_grain="fact_without_defined_grain_candidate" in classification_types, classification_conflict_count=max(0, len(classification_types) - 1), has_sensitive_signal=any(candidate.get("sensitivity") == "personal_data_candidate" for candidate_sheet_id, _, candidates in sensitivity_candidates if candidate_sheet_id == sheet_id for candidate in candidates) or any(column.semantic_identifier.sensitive_header for column in sheet_columns), has_formula_signal=any(column.formulas.formula_count > 0 for column in sheet_columns))
                candidate = execute_registered_rule("MET-RUNNING-010", running_total_profile)
                if candidate:
                    metric_candidates.append((sheet_id, [candidate]))
            if metric_rule_statuses["MET-WAVG-011"] == "executable_draft":
                semantic_types = [candidate.get("semantic_type") for candidate_sheet_id, _, candidates in semantic_candidates if candidate_sheet_id == sheet_id for candidate in candidates]
                weighted_average_profile = WeightedAverageConceptProfile(row_count=max(column.missingness.observed_cell_count for column in sheet_columns), physical_column_count=len(sheet_columns), measure_candidate_count=semantic_types.count("currency_candidate"), weight_candidate_count=semantic_types.count("quantity_candidate"), nonpositive_weight_count=sum(column.semantic_quantity.nonpositive_value_count for column in sheet_columns if column.semantic_quantity.header_eligible), has_defined_grain=bool(grain_rule_ids), grain_ambiguity_count=max(0, len(grain_rule_ids) - 1), has_undefined_classification="table_classification_undefined_candidate" in classification_types, has_fact_without_grain="fact_without_defined_grain_candidate" in classification_types, classification_conflict_count=max(0, len(classification_types) - 1), has_sensitive_signal=any(candidate.get("sensitivity") == "personal_data_candidate" for candidate_sheet_id, _, candidates in sensitivity_candidates if candidate_sheet_id == sheet_id for candidate in candidates) or any(column.semantic_identifier.sensitive_header for column in sheet_columns), has_formula_signal=any(column.formulas.formula_count > 0 for column in sheet_columns))
                candidate = execute_registered_rule("MET-WAVG-011", weighted_average_profile)
                if candidate:
                    metric_candidates.append((sheet_id, [candidate]))
            if metric_rule_statuses["MET-SEMIADD-012"] == "executable_draft":
                semantic_types = [candidate.get("semantic_type") for candidate_sheet_id, _, candidates in semantic_candidates if candidate_sheet_id == sheet_id for candidate in candidates]
                semiadditive_profile = SemiadditiveConceptProfile(row_count=max(column.missingness.observed_cell_count for column in sheet_columns), physical_column_count=len(sheet_columns), potential_balance_candidate_count=semantic_types.count("currency_candidate") + semantic_types.count("quantity_candidate"), temporal_order_candidate_count=semantic_types.count("date_generic"), temporal_order_duplicate_count=sum(max(0, column.semantic_date.recognized_date_count - column.semantic_date.distinct_recognized_date_count) for column in sheet_columns if column.semantic_date.non_missing_count >= 10 and column.semantic_date.recognized_date_ratio == 1.0), has_defined_grain=bool(grain_rule_ids), grain_ambiguity_count=max(0, len(grain_rule_ids) - 1), has_undefined_classification="table_classification_undefined_candidate" in classification_types, has_fact_without_grain="fact_without_defined_grain_candidate" in classification_types, classification_conflict_count=max(0, len(classification_types) - 1), has_sensitive_signal=any(candidate.get("sensitivity") == "personal_data_candidate" for candidate_sheet_id, _, candidates in sensitivity_candidates if candidate_sheet_id == sheet_id for candidate in candidates) or any(column.semantic_identifier.sensitive_header for column in sheet_columns), has_formula_signal=any(column.formulas.formula_count > 0 for column in sheet_columns))
                candidate = execute_registered_rule("MET-SEMIADD-012", semiadditive_profile)
                if candidate:
                    metric_candidates.append((sheet_id, [candidate]))
            if metric_rule_statuses["MET-DOMAIN-013"] == "executable_draft":
                domain_metric_profile = DomainMetricConceptProfile(row_count=max(column.missingness.observed_cell_count for column in sheet_columns), physical_column_count=len(sheet_columns), domain_signal_candidate_count=0, has_defined_grain=bool(grain_rule_ids), grain_ambiguity_count=max(0, len(grain_rule_ids) - 1), has_undefined_classification="table_classification_undefined_candidate" in classification_types, has_fact_without_grain="fact_without_defined_grain_candidate" in classification_types, classification_conflict_count=max(0, len(classification_types) - 1), has_sensitive_signal=any(candidate.get("sensitivity") == "personal_data_candidate" for candidate_sheet_id, _, candidates in sensitivity_candidates if candidate_sheet_id == sheet_id for candidate in candidates) or any(column.semantic_identifier.sensitive_header for column in sheet_columns), has_formula_signal=any(column.formulas.formula_count > 0 for column in sheet_columns))
                candidate = execute_registered_rule("MET-DOMAIN-013", domain_metric_profile)
                if candidate:
                    metric_candidates.append((sheet_id, [candidate]))
            if metric_rule_statuses["MET-IMPOSS-014"] == "executable_draft":
                semantic_types = [candidate.get("semantic_type") for candidate_sheet_id, _, candidates in semantic_candidates if candidate_sheet_id == sheet_id for candidate in candidates]
                insufficient_metric_profile = InsufficientMetricConceptProfile(row_count=max(column.missingness.observed_cell_count for column in sheet_columns), physical_column_count=len(sheet_columns), eligible_measure_candidate_count=sum(semantic_types.count(metric_type) for metric_type in ("quantity_candidate", "currency_candidate", "actual_candidate", "target_or_forecast_candidate")), has_defined_grain=bool(grain_rule_ids), grain_ambiguity_count=max(0, len(grain_rule_ids) - 1), has_undefined_classification="table_classification_undefined_candidate" in classification_types, has_fact_without_grain="fact_without_defined_grain_candidate" in classification_types, classification_conflict_count=max(0, len(classification_types) - 1), has_sensitive_signal=any(candidate.get("sensitivity") == "personal_data_candidate" for candidate_sheet_id, _, candidates in sensitivity_candidates if candidate_sheet_id == sheet_id for candidate in candidates) or any(column.semantic_identifier.sensitive_header for column in sheet_columns), has_formula_signal=any(column.formulas.formula_count > 0 for column in sheet_columns))
                candidate = execute_registered_rule("MET-IMPOSS-014", insufficient_metric_profile)
                if candidate:
                    metric_candidates.append((sheet_id, [candidate]))
            if metric_rule_statuses["MET-DAX-015"] == "executable_draft":
                dax_template_profile = DaxTemplateConceptProfile(row_count=max(column.missingness.observed_cell_count for column in sheet_columns), physical_column_count=len(sheet_columns), confirmed_conceptual_formula_count=0, human_confirmation_count=0, has_defined_grain=bool(grain_rule_ids), grain_ambiguity_count=max(0, len(grain_rule_ids) - 1), has_undefined_classification="table_classification_undefined_candidate" in classification_types, has_fact_without_grain="fact_without_defined_grain_candidate" in classification_types, classification_conflict_count=max(0, len(classification_types) - 1), has_sensitive_signal=any(candidate.get("sensitivity") == "personal_data_candidate" for candidate_sheet_id, _, candidates in sensitivity_candidates if candidate_sheet_id == sheet_id for candidate in candidates) or any(column.semantic_identifier.sensitive_header for column in sheet_columns), has_formula_signal=any(column.formulas.formula_count > 0 for column in sheet_columns))
                candidate = execute_registered_rule("MET-DAX-015", dax_template_profile)
                if candidate:
                    metric_candidates.append((sheet_id, [candidate]))

    if alert_rule_statuses["ALT-SENS-001"] == "executable_draft":
        for sheet_id, column_id, candidates in sensitivity_candidates:
            sensitivity_signal_candidate_count = sum(candidate.get("sensitivity") == "personal_data_candidate" for candidate in candidates)
            alert_candidate = execute_registered_rule(
                "ALT-SENS-001",
                SensitiveDataRestrictionProfile(
                    sensitivity_signal_candidate_count=sensitivity_signal_candidate_count,
                    sensitivity_conflict_count=max(0, sensitivity_signal_candidate_count - 1),
                ),
            )
            if alert_candidate:
                quality_findings.append((sheet_id, column_id, alert_candidate))

    if alert_rule_statuses["ALT-QUALITY-002"] == "executable_draft":
        quality_rule_findings = [
            finding
            for _, _, finding in quality_findings
            if str(finding.get("rule_id", "")).startswith("QLT-")
        ]
        quality_alert_candidate = execute_registered_rule(
            "ALT-QUALITY-002",
            CriticalQualityRiskProfile(
                high_quality_finding_count=sum(finding.get("severity") == "high" for finding in quality_rule_findings),
                distinct_quality_rule_count=len({str(finding.get("rule_id")) for finding in quality_rule_findings}),
                analyzed_sheet_count=len(grouped_columns),
            ),
        )
        if quality_alert_candidate:
            quality_findings.append(("model", "model", quality_alert_candidate))

    if alert_rule_statuses["ALT-GRAIN-003"] == "executable_draft":
        grain_alert_candidate = execute_registered_rule(
            "ALT-GRAIN-003",
            UndefinedGrainAlertProfile(
                # Não há fonte independente autorizada para sinal de grão indefinido.
                # O pipeline permanece fail-closed e não deriva o sinal de conteúdo privado.
                undefined_grain_signal_count=0,
                confirmed_grain_count=sum(bool(candidates) for candidates in grain_candidates.values()),
            ),
        )
        if grain_alert_candidate:
            quality_findings.append(("model", "model", grain_alert_candidate))

    if alert_rule_statuses["ALT-KEY-004"] == "executable_draft":
        key_alert_candidate = execute_registered_rule(
            "ALT-KEY-004",
            InvalidKeyAlertProfile(
                # Não há fonte independente autorizada para sinal de chave inválida.
                # O pipeline permanece fail-closed e não deriva o sinal de conteúdo privado.
                invalid_key_signal_count=0,
            ),
        )
        if key_alert_candidate:
            quality_findings.append(("model", "model", key_alert_candidate))

    if alert_rule_statuses["ALT-AMBIG-005"] == "executable_draft":
        ambiguity_alert_candidate = execute_registered_rule(
            "ALT-AMBIG-005",
            StructuralAmbiguityAlertProfile(
                # Não há fonte independente autorizada para ambiguidade estrutural.
                # O pipeline permanece fail-closed e não deriva o sinal de conteúdo privado.
                structural_ambiguity_signal_count=0,
            ),
        )
        if ambiguity_alert_candidate:
            quality_findings.append(("model", "model", ambiguity_alert_candidate))

    if alert_rule_statuses["ALT-METRIC-006"] == "executable_draft":
        metric_risk_alert_candidate = execute_registered_rule(
            "ALT-METRIC-006",
            PotentiallyMisleadingMetricAlertProfile(
                # Não há fonte independente autorizada para risco de interpretação de métrica.
                # O pipeline permanece fail-closed e não deriva o sinal de conteúdo privado.
                independent_metric_risk_signal_count=0,
            ),
        )
        if metric_risk_alert_candidate:
            quality_findings.append(("model", "model", metric_risk_alert_candidate))

    if alert_rule_statuses["ALT-SUMPCT-007"] == "executable_draft":
        percentage_sum_alert_candidate = execute_registered_rule(
            "ALT-SUMPCT-007",
            PercentageSumAlertProfile(
                # Não há fonte independente autorizada para risco na soma de percentuais.
                # O pipeline permanece fail-closed e não deriva o sinal de conteúdo privado.
                independent_percentage_sum_risk_signal_count=0,
            ),
        )
        if percentage_sum_alert_candidate:
            quality_findings.append(("model", "model", percentage_sum_alert_candidate))

    if alert_rule_statuses["ALT-AVGAVG-008"] == "executable_draft":
        average_of_averages_alert_candidate = execute_registered_rule(
            "ALT-AVGAVG-008",
            AverageOfAveragesAlertProfile(
                # Não há fonte independente autorizada para risco em média de médias.
                # O pipeline permanece fail-closed e não deriva o sinal de conteúdo privado.
                independent_average_of_averages_risk_signal_count=0,
            ),
        )
        if average_of_averages_alert_candidate:
            quality_findings.append(("model", "model", average_of_averages_alert_candidate))

    findings: list[dict[str, object]] = []
    questions: list[dict[str, object]] = []
    semantic_classifications: list[dict[str, object]] = []
    sensitivity_classifications: list[dict[str, object]] = []
    relationships: list[dict[str, object]] = []
    metrics: list[dict[str, object]] = []
    grains_by_sheet: dict[str, dict[str, object] | None] = {sheet_id: None for sheet_id in grouped_columns}
    classifications_by_sheet: dict[str, dict[str, object] | None] = {sheet_id: None for sheet_id in grouped_columns}
    question_ids_by_sheet: dict[str, list[str]] = {sheet_id: [] for sheet_id in grouped_columns}
    for sheet_id, column_id, finding in quality_findings:
        fragment = to_diagnosis_fragment([finding], sheet_id=sheet_id, column_id=column_id)
        findings.extend(fragment["findings"])  # type: ignore[arg-type]
        fragment_questions = fragment["questions"]  # type: ignore[assignment]
        questions.extend(fragment_questions)  # type: ignore[arg-type]
        question_ids_by_sheet[sheet_id].extend(question["question_id"] for question in fragment_questions)  # type: ignore[index, union-attr]
    for sheet_id, column_id, candidates in semantic_candidates:
        fragment = to_semantic_classification_fragment(candidates, sheet_id=sheet_id, column_id=column_id)
        semantic_classifications.extend(fragment["semantic_classifications"])  # type: ignore[arg-type]
        semantic_questions = fragment["questions"]  # type: ignore[assignment]
        questions.extend(semantic_questions)  # type: ignore[arg-type]
        question_ids_by_sheet[sheet_id].extend(question["question_id"] for question in semantic_questions)  # type: ignore[index,union-attr]
    for sheet_id, column_id, candidates in sensitivity_candidates:
        fragment = to_sensitivity_fragment(candidates, sheet_id=sheet_id, column_id=column_id)
        sensitivity_classifications.extend(fragment["sensitivity_classifications"])  # type: ignore[arg-type]
        sensitivity_questions = fragment["questions"]  # type: ignore[assignment]
        questions.extend(sensitivity_questions)  # type: ignore[arg-type]
        question_ids_by_sheet[sheet_id].extend(question["question_id"] for question in sensitivity_questions)  # type: ignore[index,union-attr]
    for sheet_id, candidates in grain_candidates.items():
        fragment = to_grain_fragment(candidates, sheet_id=sheet_id)
        grains_by_sheet[sheet_id] = fragment["grain"]  # type: ignore[assignment]
        grain_questions = fragment["questions"]  # type: ignore[assignment]
        questions.extend(grain_questions)  # type: ignore[arg-type]
        question_ids_by_sheet[sheet_id].extend(question["question_id"] for question in grain_questions)  # type: ignore[index,union-attr]
    for sheet_id, candidates in table_candidates.items():
        fragment = to_table_classification_fragment(candidates, sheet_id=sheet_id)
        classifications_by_sheet[sheet_id] = fragment["classification"]  # type: ignore[assignment]
        table_questions = fragment["questions"]  # type: ignore[assignment]
        questions.extend(table_questions)  # type: ignore[arg-type]
        question_ids_by_sheet[sheet_id].extend(question["question_id"] for question in table_questions)  # type: ignore[index,union-attr]
    for source_sheet_id, target_sheet_id, candidates in relationship_candidates:
        fragment = to_relationship_fragment(
            candidates,
            source_sheet_id=source_sheet_id,
            target_sheet_id=target_sheet_id,
        )
        relationships.extend(fragment["relationships"])  # type: ignore[arg-type]
        relationship_questions = fragment["questions"]  # type: ignore[assignment]
        questions.extend(relationship_questions)  # type: ignore[arg-type]
        for question in relationship_questions:  # type: ignore[union-attr]
            question_ids_by_sheet[source_sheet_id].append(question["question_id"])
            question_ids_by_sheet[target_sheet_id].append(question["question_id"])
    for sheet_id, candidates in metric_candidates:
        fragment = to_metric_fragment(candidates, sheet_id=sheet_id)
        metrics.extend(fragment["metrics"])  # type: ignore[arg-type]
        metric_questions = fragment["questions"]  # type: ignore[assignment]
        questions.extend(metric_questions)  # type: ignore[arg-type]
        question_ids_by_sheet[sheet_id].extend(question["question_id"] for question in metric_questions)  # type: ignore[index,union-attr]

    finding_ids_by_sheet: dict[str, list[str]] = {sheet_id: [] for sheet_id in grouped_columns}
    for finding in findings:
        sheet_id = finding["affected_entities"][0]["entity_id"]  # type: ignore[index]
        finding_ids_by_sheet[sheet_id].append(finding["finding_id"])  # type: ignore[index]
    analysis_status = "awaiting_user" if questions else "completed_with_warnings"
    execution_completed_at = _timestamp()
    analysis_completed_at = execution_completed_at if analysis_status.startswith("completed") else None
    execution_duration_ms = round((perf_counter() - started_clock) * 1000)
    sheet_objects = []
    for sheet_id, sheet_columns in grouped_columns.items():
        representative = sheet_columns[0]
        row_count = max(column.missingness.observed_cell_count for column in sheet_columns)
        sheet_objects.append(
            {
                "sheet_id": sheet_id,
                "name": representative.sheet_name,
                "position": representative.sheet_position,
                "visibility": representative.sheet_visibility,
                "included_in_analysis": True,
                "analysis_status": "warnings" if finding_ids_by_sheet[sheet_id] else "analyzed",
                "region": None,
                "row_count": row_count,
                "column_count": len(sheet_columns),
                "quality_score": None,
                "grain": grains_by_sheet[sheet_id],
                "classification": classifications_by_sheet[sheet_id],
                "columns": [
                    {
                        "column_id": column.column_id,
                        "name": column.column_name,
                        "position": column.column_position,
                        "physical_type": column.physical_type,
                        "profile": {
                            "non_empty_value_count": column.numeric_text.non_empty_value_count,
                            "numeric_text_candidate_count": column.numeric_text.numeric_text_candidate_count,
                            "numeric_text_candidate_ratio": column.numeric_text.numeric_text_candidate_ratio,
                            "numeric_text_basis": column.numeric_text.numeric_text_basis,
                            "numeric_text_ambiguity_count": column.numeric_text.numeric_text_ambiguity_count,
                        },
                    }
                    for column in sheet_columns
                ],
                "finding_ids": finding_ids_by_sheet[sheet_id],
                "question_ids": question_ids_by_sheet[sheet_id],
            }
        )

    diagnosis: dict[str, object] = {
        "schema_version": SCHEMA_VERSION,
        "contract_id": CONTRACT_ID,
        "analysis": {
            "analysis_id": metadata.analysis_id,
            "project_id": metadata.project_id,
            "owner_user_id": metadata.owner_user_id,
            "version": metadata.analysis_version,
            "supersedes_analysis_id": metadata.supersedes_analysis_id,
            "project_name": metadata.project_name,
            "domain": metadata.domain,
            "objective": metadata.objective,
            "business_questions": list(metadata.business_questions),
            "status": analysis_status,
            "locale": "pt-BR",
            "terms_version": metadata.terms_version,
            "consented_at": metadata.consented_at,
            "created_at": metadata.created_at,
            "updated_at": execution_completed_at,
            "completed_at": analysis_completed_at,
            "overall_confidence": None,
            "assumptions": [profile.assumption],
            "limitations": [profile.limitation],
        },
        "file": {
            "file_id": metadata.file_id,
            "original_name": metadata.original_name,
            "extension": ".xlsx",
            "mime_type": metadata.file_mime_type,
            "size_bytes": metadata.file_size_bytes,
            "sha256": metadata.file_sha256,
            "workbook_readable": metadata.workbook_readable,
            "sheet_count": len(sheet_objects),
            "analyzable_sheet_count": len(sheet_objects),
            "total_rows": sum(sheet["row_count"] for sheet in sheet_objects),
            "total_columns": sum(sheet["column_count"] for sheet in sheet_objects),
            "retention": {"status": metadata.retention_status, "uploaded_at": metadata.uploaded_at, "delete_at": metadata.retention_delete_at, "deleted_at": None},
            "finding_ids": [],
        },
        "summary": {
            "quality_score": None,
            "completeness_ratio": round(executable_rule_count() / profile.catalog_target_rule_count, 8),
            "counts": {"sheets": len(sheet_objects), "columns": sum(sheet["column_count"] for sheet in sheet_objects), "facts": 0, "dimensions": 0, "relationships": len(relationships), "metrics": len(metrics), "risks": len(findings)},
            "top_risk_finding_ids": [finding["finding_id"] for finding in findings[:10]],
            "executive_summary": profile.summary_template.format(sheet_count=len(sheet_objects), column_count=sum(sheet["column_count"] for sheet in sheet_objects), finding_count=len(findings)),
            "next_recommended_action": profile.next_action_with_questions if questions else profile.next_action_without_questions,
        },
        "sheets": sheet_objects,
        "proposed_model": {"status": profile.proposed_model_status, "tables": [], "implementation_steps": [], "assumptions": [], "limitations": [profile.proposed_model_limitation], "confidence": None},
        "relationships": relationships,
        "metrics": metrics,
        "questions": questions,
        "findings": findings,
        "semantic_classifications": semantic_classifications,
        "sensitivity_classifications": sensitivity_classifications,
        "execution": {
            "correlation_id": metadata.correlation_id,
            "status": profile.execution_status,
            "started_at": started_at,
            "completed_at": execution_completed_at,
            "duration_ms": execution_duration_ms,
            "engine_version": profile.engine_version,
            "ruleset_version": profile.ruleset_version,
            "schema_version": SCHEMA_VERSION,
            "confidence_methodology_version": profile.confidence_methodology_version,
            "partial_results": True,
            "modules": [{"module": profile.module_name, "status": profile.module_status, "duration_ms": execution_duration_ms}],
            "errors": [],
            "ai_usage": profile.ai_usage,
        },
    }
    validate_diagnosis_root(diagnosis)
    validate_governed_output(
        diagnosis,
        profile=profile,
        executed_rule_count=executable_rule_count(),
    )
    return diagnosis
