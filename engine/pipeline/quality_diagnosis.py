"""Executa o ruleset draft sobre contexto agregado e produz o objeto raiz canônico do diagnóstico."""

from __future__ import annotations

from dataclasses import dataclass, field
from time import perf_counter
from typing import Iterable, Literal

from engine.catalog import executable_rule_count, execute_registered_rule, get_rule_execution_record
from engine.contracts.diagnosis import CONTRACT_ID, SCHEMA_VERSION, _timestamp, to_diagnosis_fragment, to_grain_fragment, to_semantic_classification_fragment
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
from engine.profiling.semantic_identifier import SemanticIdentifierProfile, profile_semantic_identifier
from engine.profiling.composite_grain import CompositeGrainProfile
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
from engine.semantic.identifier import SemanticIdentifierColumnProfile, classify_identifier
from engine.granularity.composite import CompositeGrainSheetProfile


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
    semantic_identifier: SemanticIdentifierProfile = field(default_factory=SemanticIdentifierProfile)
    composite_grain: CompositeGrainProfile = field(default_factory=CompositeGrainProfile)


def build_column_analysis_context(
    *, sheet_id: str, column_id: str, column_name: str, values: Iterable[object], sheet_name: str, sheet_position: int, sheet_visibility: Literal["visible", "hidden", "very_hidden"], column_position: int
) -> ColumnAnalysisContext:
    """Descarta valores brutos depois do profiling e preserva apenas métricas agregadas."""

    materialized_values = list(values)
    return ColumnAnalysisContext(
        sheet_id=sheet_id,
        sheet_name=sheet_name,
        sheet_position=sheet_position,
        sheet_visibility=sheet_visibility,
        column_id=column_id,
        column_name=column_name,
        column_position=column_position,
        physical_type=infer_physical_type(materialized_values),
        numeric_text=profile_numeric_text(materialized_values),
        missingness=profile_missingness(materialized_values),
        categorical_variations=profile_categorical_variations(materialized_values),
        mixed_types=profile_mixed_types(materialized_values),
        bad_dates=profile_bad_dates(materialized_values),
        whitespace=profile_whitespace(materialized_values),
        negative_values=profile_negative_values(column_name, materialized_values),
        outliers=profile_outliers(materialized_values),
        identifiers=profile_identifier_completeness(column_name, materialized_values),
        semantic_date=profile_semantic_date(materialized_values),
        semantic_identifier=profile_semantic_identifier(column_name, materialized_values),
    )


def execute_quality_diagnosis(columns: Iterable[ColumnAnalysisContext], *, metadata: DiagnosisMetadata) -> dict[str, object]:
    """Monta todos os blocos do contrato em estado partial sem fabricar recomendações de modelo."""

    profile = metadata.execution_profile
    started_at = _timestamp()
    started_clock = perf_counter()
    quality_findings: list[tuple[str, str | None, dict[str, object]]] = []
    semantic_candidates: list[tuple[str, str, list[dict[str, object]]]] = []
    grain_candidates: dict[str, list[dict[str, object]]] = {}
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
        if get_rule_execution_record("SEM-ID-003").status == "executable_draft":
            identifier_semantic_profile = SemanticIdentifierColumnProfile(
                physical_type=column.physical_type, formula_count=column.formulas.formula_count,
                semantic_identifier=column.semantic_identifier,
            )
            semantic_candidates.append((column.sheet_id, column.column_id, execute_registered_rule("SEM-ID-003", identifier_semantic_profile)))

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

    findings: list[dict[str, object]] = []
    questions: list[dict[str, object]] = []
    semantic_classifications: list[dict[str, object]] = []
    grains_by_sheet: dict[str, dict[str, object] | None] = {sheet_id: None for sheet_id in grouped_columns}
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
    for sheet_id, candidates in grain_candidates.items():
        fragment = to_grain_fragment(candidates, sheet_id=sheet_id)
        grains_by_sheet[sheet_id] = fragment["grain"]  # type: ignore[assignment]
        grain_questions = fragment["questions"]  # type: ignore[assignment]
        questions.extend(grain_questions)  # type: ignore[arg-type]
        question_ids_by_sheet[sheet_id].extend(question["question_id"] for question in grain_questions)  # type: ignore[index,union-attr]

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
                "classification": None,
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
            "counts": {"sheets": len(sheet_objects), "columns": sum(sheet["column_count"] for sheet in sheet_objects), "facts": 0, "dimensions": 0, "relationships": 0, "metrics": 0, "risks": len(findings)},
            "top_risk_finding_ids": [finding["finding_id"] for finding in findings[:10]],
            "executive_summary": profile.summary_template.format(sheet_count=len(sheet_objects), column_count=sum(sheet["column_count"] for sheet in sheet_objects), finding_count=len(findings)),
            "next_recommended_action": profile.next_action_with_questions if questions else profile.next_action_without_questions,
        },
        "sheets": sheet_objects,
        "proposed_model": {"status": profile.proposed_model_status, "tables": [], "implementation_steps": [], "assumptions": [], "limitations": [profile.proposed_model_limitation], "confidence": None},
        "relationships": [],
        "metrics": [],
        "questions": questions,
        "findings": findings,
        "semantic_classifications": semantic_classifications,
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
