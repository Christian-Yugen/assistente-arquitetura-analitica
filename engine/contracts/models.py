"""Modelos Pydantic do contrato reconstruído e validações cruzadas documentadas."""

from __future__ import annotations

from datetime import datetime
from typing import Any, Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, model_validator


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class RetentionInfo(StrictModel):
    status: str
    uploaded_at: datetime
    delete_at: datetime
    deleted_at: datetime | None


class Analysis(StrictModel):
    analysis_id: UUID
    project_id: UUID
    owner_user_id: UUID
    version: int = Field(ge=1)
    supersedes_analysis_id: UUID | None
    project_name: str
    domain: Literal["generic", "sso", "hr"]
    objective: str
    business_questions: list[str]
    status: Literal["created", "uploaded", "validating", "profiling", "inferring", "awaiting_user", "reanalyzing", "completed", "completed_with_warnings", "failed", "deleted"]
    locale: Literal["pt-BR"]
    terms_version: str
    consented_at: datetime
    created_at: datetime
    updated_at: datetime
    completed_at: datetime | None
    overall_confidence: dict[str, Any] | None
    assumptions: list[str]
    limitations: list[str]


class FileInfo(StrictModel):
    file_id: UUID
    original_name: str
    extension: Literal[".xlsx"]
    mime_type: str
    size_bytes: int = Field(ge=0, le=26_214_400)
    sha256: str = Field(pattern=r"^[A-Fa-f0-9]{64}$")
    workbook_readable: bool
    sheet_count: int = Field(ge=0, le=10)
    analyzable_sheet_count: int = Field(ge=0, le=10)
    total_rows: int = Field(ge=0)
    total_columns: int = Field(ge=0)
    retention: RetentionInfo
    finding_ids: list[UUID]


class SummaryCounts(StrictModel):
    sheets: int = Field(ge=0)
    columns: int = Field(ge=0)
    facts: int = Field(ge=0)
    dimensions: int = Field(ge=0)
    relationships: int = Field(ge=0)
    metrics: int = Field(ge=0)
    risks: int = Field(ge=0)


class Summary(StrictModel):
    quality_score: float | None = Field(default=None, ge=0, le=100)
    completeness_ratio: float = Field(ge=0, le=1)
    counts: SummaryCounts
    top_risk_finding_ids: list[UUID] = Field(max_length=10)
    executive_summary: str
    next_recommended_action: str


class NumericTextProfile(StrictModel):
    non_empty_value_count: int = Field(ge=0)
    numeric_text_candidate_count: int = Field(ge=0)
    numeric_text_candidate_ratio: float = Field(ge=0, le=1)
    numeric_text_basis: str
    numeric_text_ambiguity_count: int = Field(ge=0)


class Column(StrictModel):
    column_id: UUID
    name: str
    position: int = Field(ge=0)
    physical_type: str
    profile: NumericTextProfile


class Sheet(StrictModel):
    sheet_id: UUID
    name: str
    position: int = Field(ge=0)
    visibility: Literal["visible", "hidden", "very_hidden"]
    included_in_analysis: bool
    analysis_status: Literal["analyzed", "warnings", "ignored", "not_analyzable", "failed"]
    region: dict[str, Any] | None
    row_count: int = Field(ge=0)
    column_count: int = Field(ge=0)
    quality_score: float | None = Field(default=None, ge=0, le=100)
    grain: dict[str, Any] | None
    classification: dict[str, Any] | None
    columns: list[Column]
    finding_ids: list[UUID]
    question_ids: list[UUID]


class ProposedModel(StrictModel):
    status: Literal["recommended", "probable", "hypothesis", "rejected", "insufficient"]
    tables: list[dict[str, Any]]
    implementation_steps: list[dict[str, Any]]
    assumptions: list[str]
    limitations: list[str]
    confidence: dict[str, Any] | None


class Evidence(StrictModel):
    code: str
    effect: str
    observed: dict[str, Any]
    expected_condition: str


class AffectedEntity(StrictModel):
    entity_type: str
    entity_id: str


class Finding(StrictModel):
    finding_id: UUID
    category: str
    severity: Literal["critical", "high", "medium", "low", "informational"]
    status: Literal["open", "acknowledged", "resolved", "accepted_risk"]
    title: str
    description: str
    evidence: list[Evidence]
    impact: str
    recommendation: str
    rule_id: str
    rule_version: str
    affected_entities: list[AffectedEntity]
    created_at: datetime


class QuestionImpact(StrictModel):
    affected_modules: list[str]
    affected_rule_ids: list[str]
    affected_recommendation_ids: list[str]


class Question(StrictModel):
    question_id: UUID
    text: str
    reason: str
    question_type: Literal["single_choice", "multiple_choice", "number", "short_text", "confirmation"]
    priority: Literal["low", "medium", "high", "critical"]
    blocking: bool
    status: Literal["pending", "answered", "skipped", "obsolete"]
    options: list[dict[str, Any]]
    impact: QuestionImpact
    answer: dict[str, Any] | None
    created_at: datetime

    @model_validator(mode="after")
    def answered_question_requires_answer(self):
        if self.status == "answered" and self.answer is None:
            raise ValueError("Question status=answered requires answer.")
        return self


class Execution(StrictModel):
    correlation_id: UUID
    status: str
    started_at: datetime
    completed_at: datetime | None
    duration_ms: int | None = Field(default=None, ge=0)
    engine_version: str
    ruleset_version: str
    schema_version: Literal["1.0.0"]
    confidence_methodology_version: str
    partial_results: bool
    modules: list[dict[str, Any]]
    errors: list[dict[str, Any]]
    ai_usage: dict[str, Any]


class ReconstructedDiagnosis(StrictModel):
    schema_version: Literal["1.0.0"]
    contract_id: Literal["PM-MVP-PBI-CON-001"]
    analysis: Analysis
    file: FileInfo
    summary: Summary
    sheets: list[Sheet]
    proposed_model: ProposedModel
    relationships: list[dict[str, Any]]
    metrics: list[dict[str, Any]]
    questions: list[Question]
    findings: list[Finding]
    execution: Execution

    @model_validator(mode="after")
    def validate_cross_references(self):
        if self.file.sheet_count != len(self.sheets):
            raise ValueError("file.sheet_count must equal sheets.length.")
        sheet_ids = {sheet.sheet_id for sheet in self.sheets}
        column_ids = {column.column_id for sheet in self.sheets for column in sheet.columns}
        finding_ids = {finding.finding_id for finding in self.findings}
        question_ids = {question.question_id for question in self.questions}

        if not set(self.file.finding_ids).issubset(finding_ids):
            raise ValueError("file.finding_ids must reference findings in the document.")
        if not set(self.summary.top_risk_finding_ids).issubset(finding_ids):
            raise ValueError("summary.top_risk_finding_ids must reference findings in the document.")
        for sheet in self.sheets:
            if not set(sheet.finding_ids).issubset(finding_ids) or not set(sheet.question_ids).issubset(question_ids):
                raise ValueError("Sheet finding_ids and question_ids must reference document entities.")
        for finding in self.findings:
            for entity in finding.affected_entities:
                if entity.entity_type == "sheet" and UUID(entity.entity_id) not in sheet_ids:
                    raise ValueError("Finding sheet lineage must reference an existing sheet.")
                if entity.entity_type == "column" and UUID(entity.entity_id) not in column_ids:
                    raise ValueError("Finding column lineage must reference an existing column.")
        return self
