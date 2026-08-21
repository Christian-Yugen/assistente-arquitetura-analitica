"""Schema estrutural do envelope PM-MVP-PBI-CON-001 usado pelo motor draft."""

from __future__ import annotations

from typing import Any


UUID = {"type": "string", "format": "uuid"}
TIMESTAMP = {"type": "string", "format": "date-time"}
NON_NEGATIVE_INTEGER = {"type": "integer", "minimum": 0}


def strict_object(properties: dict[str, Any], required: list[str]) -> dict[str, Any]:
    return {
        "type": "object",
        "additionalProperties": False,
        "properties": properties,
        "required": required,
    }


FINDING_SCHEMA = strict_object(
    {
        "finding_id": UUID,
        "category": {"type": "string"},
        "severity": {"enum": ["critical", "high", "medium", "low", "informational"]},
        "status": {"enum": ["open", "acknowledged", "resolved", "accepted_risk"]},
        "title": {"type": "string"},
        "description": {"type": "string"},
        "evidence": {
            "type": "array",
            "items": strict_object(
                {
                    "code": {"type": "string"},
                    "effect": {"type": "string"},
                    "observed": {"type": "object", "additionalProperties": True},
                    "expected_condition": {"type": "string"},
                },
                ["code", "effect", "observed", "expected_condition"],
            ),
        },
        "impact": {"type": "string"},
        "recommendation": {"type": "string"},
        "rule_id": {"type": "string"},
        "rule_version": {"type": "string"},
        "affected_entities": {
            "type": "array",
            "items": strict_object(
                {"entity_type": {"type": "string"}, "entity_id": {"type": "string"}},
                ["entity_type", "entity_id"],
            ),
        },
        "created_at": TIMESTAMP,
    },
    [
        "finding_id",
        "category",
        "severity",
        "status",
        "title",
        "description",
        "evidence",
        "impact",
        "recommendation",
        "rule_id",
        "rule_version",
        "affected_entities",
        "created_at",
    ],
)

QUESTION_SCHEMA = strict_object(
    {
        "question_id": UUID,
        "text": {"type": "string"},
        "reason": {"type": "string"},
        "question_type": {"enum": ["single_choice", "multiple_choice", "number", "short_text", "confirmation"]},
        "priority": {"enum": ["low", "medium", "high", "critical"]},
        "blocking": {"type": "boolean"},
        "status": {"enum": ["pending", "answered", "skipped", "obsolete"]},
        "options": {"type": "array"},
        "impact": strict_object(
            {
                "affected_modules": {"type": "array", "items": {"type": "string"}},
                "affected_rule_ids": {"type": "array", "items": {"type": "string"}},
                "affected_recommendation_ids": {"type": "array", "items": {"type": "string"}},
            },
            ["affected_modules", "affected_rule_ids", "affected_recommendation_ids"],
        ),
        "answer": {"type": ["object", "null"]},
        "created_at": TIMESTAMP,
    },
    ["question_id", "text", "reason", "question_type", "priority", "blocking", "status", "options", "impact", "answer", "created_at"],
)

SEMANTIC_CLASSIFICATION_SCHEMA = strict_object(
    {
        "semantic_type": {"type": "string"},
        "confidence": {"type": "number", "minimum": 0, "maximum": 1},
        "evidence": {"type": "object", "additionalProperties": True},
        "rule_id": {"type": "string"},
        "rule_version": {"type": "string"},
        "affected_entities": {
            "type": "array",
            "items": strict_object({"entity_type": {"type": "string"}, "entity_id": {"type": "string"}}, ["entity_type", "entity_id"]),
        },
    },
    ["semantic_type", "confidence", "evidence", "rule_id", "rule_version", "affected_entities"],
)

SENSITIVITY_CLASSIFICATION_SCHEMA = strict_object(
    {
        "sensitivity": {"type": "string"},
        "confidence": {"type": "number", "minimum": 0, "maximum": 1},
        "evidence": {"type": "object", "additionalProperties": True},
        "rule_id": {"type": "string"},
        "rule_version": {"type": "string"},
        "affected_entities": {
            "type": "array",
            "items": strict_object({"entity_type": {"type": "string"}, "entity_id": {"type": "string"}}, ["entity_type", "entity_id"]),
        },
    },
    ["sensitivity", "confidence", "evidence", "rule_id", "rule_version", "affected_entities"],
)

COLUMN_SCHEMA = strict_object(
    {
        "column_id": UUID,
        "name": {"type": "string"},
        "position": NON_NEGATIVE_INTEGER,
        "physical_type": {"type": "string"},
        "profile": strict_object(
            {
                "non_empty_value_count": NON_NEGATIVE_INTEGER,
                "numeric_text_candidate_count": NON_NEGATIVE_INTEGER,
                "numeric_text_candidate_ratio": {"type": "number", "minimum": 0, "maximum": 1},
                "numeric_text_basis": {"type": "string"},
                "numeric_text_ambiguity_count": NON_NEGATIVE_INTEGER,
            },
            ["non_empty_value_count", "numeric_text_candidate_count", "numeric_text_candidate_ratio", "numeric_text_basis", "numeric_text_ambiguity_count"],
        ),
    },
    ["column_id", "name", "position", "physical_type", "profile"],
)

SHEET_SCHEMA = strict_object(
    {
        "sheet_id": UUID,
        "name": {"type": "string"},
        "position": NON_NEGATIVE_INTEGER,
        "visibility": {"enum": ["visible", "hidden", "very_hidden"]},
        "included_in_analysis": {"type": "boolean"},
        "analysis_status": {"enum": ["analyzed", "warnings", "ignored", "not_analyzable", "failed"]},
        "region": {"type": ["object", "null"]},
        "row_count": NON_NEGATIVE_INTEGER,
        "column_count": NON_NEGATIVE_INTEGER,
        "quality_score": {"type": ["number", "null"], "minimum": 0, "maximum": 100},
        "grain": {"type": ["object", "null"]},
        "classification": {"type": ["object", "null"]},
        "columns": {"type": "array", "items": COLUMN_SCHEMA},
        "finding_ids": {"type": "array", "items": UUID},
        "question_ids": {"type": "array", "items": UUID},
    },
    ["sheet_id", "name", "position", "visibility", "included_in_analysis", "analysis_status", "region", "row_count", "column_count", "quality_score", "grain", "classification", "columns", "finding_ids", "question_ids"],
)

DIAGNOSIS_ROOT_SCHEMA = strict_object(
    {
        "schema_version": {"const": "1.0.0"},
        "contract_id": {"const": "PM-MVP-PBI-CON-001"},
        "analysis": strict_object(
            {
                "analysis_id": UUID,
                "project_id": UUID,
                "owner_user_id": UUID,
                "version": {"type": "integer", "minimum": 1},
                "supersedes_analysis_id": {"anyOf": [UUID, {"type": "null"}]},
                "project_name": {"type": "string"},
                "domain": {"enum": ["generic", "sso", "hr"]},
                "objective": {"type": "string"},
                "business_questions": {"type": "array", "items": {"type": "string"}},
                "status": {"enum": ["created", "uploaded", "validating", "profiling", "inferring", "awaiting_user", "reanalyzing", "completed", "completed_with_warnings", "failed", "deleted"]},
                "locale": {"const": "pt-BR"},
                "terms_version": {"type": "string"},
                "consented_at": TIMESTAMP,
                "created_at": TIMESTAMP,
                "updated_at": TIMESTAMP,
                "completed_at": {"type": ["string", "null"]},
                "overall_confidence": {"type": ["object", "null"]},
                "assumptions": {"type": "array", "items": {"type": "string"}},
                "limitations": {"type": "array", "items": {"type": "string"}},
            },
            ["analysis_id", "project_id", "owner_user_id", "version", "supersedes_analysis_id", "project_name", "domain", "objective", "business_questions", "status", "locale", "terms_version", "consented_at", "created_at", "updated_at", "completed_at", "overall_confidence", "assumptions", "limitations"],
        ),
        "file": strict_object(
            {
                "file_id": UUID,
                "original_name": {"type": "string"},
                "extension": {"const": ".xlsx"},
                "mime_type": {"type": "string"},
                "size_bytes": {"type": "integer", "minimum": 0, "maximum": 26214400},
                "sha256": {"type": "string", "pattern": "^[A-Fa-f0-9]{64}$"},
                "workbook_readable": {"type": "boolean"},
                "sheet_count": {"type": "integer", "minimum": 0, "maximum": 10},
                "analyzable_sheet_count": {"type": "integer", "minimum": 0, "maximum": 10},
                "total_rows": NON_NEGATIVE_INTEGER,
                "total_columns": NON_NEGATIVE_INTEGER,
                "retention": strict_object(
                    {"status": {"type": "string"}, "uploaded_at": TIMESTAMP, "delete_at": TIMESTAMP, "deleted_at": {"type": ["string", "null"]}},
                    ["status", "uploaded_at", "delete_at", "deleted_at"],
                ),
                "finding_ids": {"type": "array", "items": UUID},
            },
            ["file_id", "original_name", "extension", "mime_type", "size_bytes", "sha256", "workbook_readable", "sheet_count", "analyzable_sheet_count", "total_rows", "total_columns", "retention", "finding_ids"],
        ),
        "summary": strict_object(
            {
                "quality_score": {"type": ["number", "null"], "minimum": 0, "maximum": 100},
                "completeness_ratio": {"type": "number", "minimum": 0, "maximum": 1},
                "counts": strict_object(
                    {"sheets": NON_NEGATIVE_INTEGER, "columns": NON_NEGATIVE_INTEGER, "facts": NON_NEGATIVE_INTEGER, "dimensions": NON_NEGATIVE_INTEGER, "relationships": NON_NEGATIVE_INTEGER, "metrics": NON_NEGATIVE_INTEGER, "risks": NON_NEGATIVE_INTEGER},
                    ["sheets", "columns", "facts", "dimensions", "relationships", "metrics", "risks"],
                ),
                "top_risk_finding_ids": {"type": "array", "items": UUID, "maxItems": 10},
                "executive_summary": {"type": "string"},
                "next_recommended_action": {"type": "string"},
            },
            ["quality_score", "completeness_ratio", "counts", "top_risk_finding_ids", "executive_summary", "next_recommended_action"],
        ),
        "sheets": {"type": "array", "items": SHEET_SCHEMA},
        "proposed_model": strict_object(
            {"status": {"enum": ["recommended", "probable", "hypothesis", "rejected", "insufficient"]}, "tables": {"type": "array"}, "implementation_steps": {"type": "array"}, "assumptions": {"type": "array", "items": {"type": "string"}}, "limitations": {"type": "array", "items": {"type": "string"}}, "confidence": {"type": ["object", "null"]}},
            ["status", "tables", "implementation_steps", "assumptions", "limitations", "confidence"],
        ),
        "relationships": {"type": "array"},
        "metrics": {"type": "array"},
        "questions": {"type": "array", "items": QUESTION_SCHEMA},
        "findings": {"type": "array", "items": FINDING_SCHEMA},
        "semantic_classifications": {"type": "array", "items": SEMANTIC_CLASSIFICATION_SCHEMA},
        "sensitivity_classifications": {"type": "array", "items": SENSITIVITY_CLASSIFICATION_SCHEMA},
        "execution": strict_object(
            {"correlation_id": UUID, "status": {"type": "string"}, "started_at": TIMESTAMP, "completed_at": {"type": ["string", "null"]}, "duration_ms": {"type": ["integer", "null"], "minimum": 0}, "engine_version": {"type": "string"}, "ruleset_version": {"type": "string"}, "schema_version": {"const": "1.0.0"}, "confidence_methodology_version": {"type": "string"}, "partial_results": {"type": "boolean"}, "modules": {"type": "array", "items": strict_object({"module": {"type": "string"}, "status": {"type": "string"}, "duration_ms": NON_NEGATIVE_INTEGER}, ["module", "status", "duration_ms"])}, "errors": {"type": "array"}, "ai_usage": strict_object({"used": {"type": "boolean"}, "providers": {"type": "array", "items": {"type": "string"}}, "fallback": {"type": "string"}}, ["used", "providers", "fallback"])},
            ["correlation_id", "status", "started_at", "completed_at", "duration_ms", "engine_version", "ruleset_version", "schema_version", "confidence_methodology_version", "partial_results", "modules", "errors", "ai_usage"],
        ),
    },
    ["schema_version", "contract_id", "analysis", "file", "summary", "sheets", "proposed_model", "relationships", "metrics", "questions", "findings", "execution"],
)
