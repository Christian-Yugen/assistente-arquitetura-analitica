"""Executa o ruleset draft sobre contexto agregado e produz o objeto raiz canônico do diagnóstico."""

from __future__ import annotations

from dataclasses import dataclass
from time import perf_counter
from typing import Iterable, Literal

from engine.catalog import executable_rule_count, execute_registered_rule
from engine.contracts.diagnosis import CONTRACT_ID, SCHEMA_VERSION, _timestamp, to_diagnosis_fragment
from engine.contracts.execution_profile import DraftExecutionProfile, validate_governed_output
from engine.contracts.validation import validate_diagnosis_root
from engine.profiling.numeric_text import NumericTextProfile, infer_physical_type, profile_numeric_text
from engine.profiling.missingness import MissingnessProfile, profile_missingness
from engine.quality.numtext import NumericTextColumnProfile
from engine.quality.nulls import NullColumnProfile


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
    )


def execute_quality_diagnosis(columns: Iterable[ColumnAnalysisContext], *, metadata: DiagnosisMetadata) -> dict[str, object]:
    """Monta todos os blocos do contrato em estado partial sem fabricar recomendações de modelo."""

    profile = metadata.execution_profile
    started_at = _timestamp()
    started_clock = perf_counter()
    quality_findings = []
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
            quality_findings.append((column, finding))
        null_profile = NullColumnProfile(name=column.column_name, physical_type=column.physical_type, missingness=column.missingness)
        for finding in execute_registered_rule("QLT-NULL-001", null_profile):
            quality_findings.append((column, finding))

    findings: list[dict[str, object]] = []
    questions: list[dict[str, object]] = []
    question_ids_by_sheet: dict[str, list[str]] = {sheet_id: [] for sheet_id in grouped_columns}
    for column, finding in quality_findings:
        fragment = to_diagnosis_fragment([finding], sheet_id=column.sheet_id, column_id=column.column_id)
        findings.extend(fragment["findings"])  # type: ignore[arg-type]
        fragment_questions = fragment["questions"]  # type: ignore[assignment]
        questions.extend(fragment_questions)  # type: ignore[arg-type]
        question_ids_by_sheet[column.sheet_id].extend(question["question_id"] for question in fragment_questions)  # type: ignore[index, union-attr]

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
                "grain": None,
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
