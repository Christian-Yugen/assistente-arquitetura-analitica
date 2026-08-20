"""Exemplos determinísticos para validação do contrato reconstruído, sem dados de cliente."""

from __future__ import annotations

from copy import deepcopy


IDS = {
    "analysis": "00000000-0000-4000-8000-000000000101",
    "project": "00000000-0000-4000-8000-000000000102",
    "owner": "00000000-0000-4000-8000-000000000103",
    "file": "00000000-0000-4000-8000-000000000104",
    "correlation": "00000000-0000-4000-8000-000000000105",
    "sheet": "00000000-0000-4000-8000-000000000106",
    "column": "00000000-0000-4000-8000-000000000107",
    "finding": "00000000-0000-4000-8000-000000000108",
    "question": "00000000-0000-4000-8000-000000000109",
}
TIMESTAMP = "2026-08-20T00:00:00Z"


def build_minimal_example() -> dict[str, object]:
    return {
        "schema_version": "1.0.0",
        "contract_id": "PM-MVP-PBI-CON-001",
        "analysis": {
            "analysis_id": IDS["analysis"],
            "project_id": IDS["project"],
            "owner_user_id": IDS["owner"],
            "version": 1,
            "supersedes_analysis_id": None,
            "project_name": "Exemplo de contrato",
            "domain": "generic",
            "objective": "Validar a estrutura do contrato reconstruído.",
            "business_questions": [],
            "status": "completed_with_warnings",
            "locale": "pt-BR",
            "terms_version": "1.0",
            "consented_at": TIMESTAMP,
            "created_at": TIMESTAMP,
            "updated_at": TIMESTAMP,
            "completed_at": TIMESTAMP,
            "overall_confidence": None,
            "assumptions": [],
            "limitations": ["Exemplo determinístico, sem dados de cliente."],
        },
        "file": {
            "file_id": IDS["file"],
            "original_name": "exemplo.xlsx",
            "extension": ".xlsx",
            "mime_type": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            "size_bytes": 1024,
            "sha256": "a" * 64,
            "workbook_readable": True,
            "sheet_count": 1,
            "analyzable_sheet_count": 1,
            "total_rows": 1,
            "total_columns": 1,
            "retention": {"status": "scheduled", "uploaded_at": TIMESTAMP, "delete_at": "2026-08-21T00:00:00Z", "deleted_at": None},
            "finding_ids": [],
        },
        "summary": {
            "quality_score": None,
            "completeness_ratio": 0.0,
            "counts": {"sheets": 1, "columns": 1, "facts": 0, "dimensions": 0, "relationships": 0, "metrics": 0, "risks": 0},
            "top_risk_finding_ids": [],
            "executive_summary": "Exemplo mínimo estruturalmente válido.",
            "next_recommended_action": "Não aplicável ao exemplo.",
        },
        "sheets": [
            {
                "sheet_id": IDS["sheet"],
                "name": "Aba exemplo",
                "position": 0,
                "visibility": "visible",
                "included_in_analysis": True,
                "analysis_status": "analyzed",
                "region": None,
                "row_count": 1,
                "column_count": 1,
                "quality_score": None,
                "grain": None,
                "classification": None,
                "columns": [
                    {
                        "column_id": IDS["column"],
                        "name": "Campo",
                        "position": 0,
                        "physical_type": "text",
                        "profile": {
                            "non_empty_value_count": 1,
                            "numeric_text_candidate_count": 0,
                            "numeric_text_candidate_ratio": 0.0,
                            "numeric_text_basis": "strict_canonical_numeric_string",
                            "numeric_text_ambiguity_count": 0,
                        },
                    }
                ],
                "finding_ids": [],
                "question_ids": [],
            }
        ],
        "proposed_model": {"status": "insufficient", "tables": [], "implementation_steps": [], "assumptions": [], "limitations": ["Exemplo contratual."], "confidence": None},
        "relationships": [],
        "metrics": [],
        "questions": [],
        "findings": [],
        "execution": {
            "correlation_id": IDS["correlation"],
            "status": "completed",
            "started_at": TIMESTAMP,
            "completed_at": TIMESTAMP,
            "duration_ms": 1,
            "engine_version": "0.1.0",
            "ruleset_version": "0.7.0-draft",
            "schema_version": "1.0.0",
            "confidence_methodology_version": "0.1.0",
            "partial_results": True,
            "modules": [{"module": "quality", "status": "completed", "duration_ms": 1}],
            "errors": [],
            "ai_usage": {"used": False, "providers": [], "fallback": "not_applicable"},
        },
    }


def build_complete_example() -> dict[str, object]:
    example = deepcopy(build_minimal_example())
    finding = {
        "finding_id": IDS["finding"],
        "category": "quality",
        "severity": "high",
        "status": "open",
        "title": "Exemplo de finding",
        "description": "Finding determinístico para validar referências.",
        "evidence": [{"code": "EVD-EXAMPLE", "effect": "negative", "observed": {"observed_value": 1}, "expected_condition": "value = 0"}],
        "impact": "Impacto de exemplo.",
        "recommendation": "Revisar o campo.",
        "rule_id": "QLT-NUMTEXT-007",
        "rule_version": "1.0.0-draft",
        "affected_entities": [
            {"entity_type": "sheet", "entity_id": IDS["sheet"]},
            {"entity_type": "column", "entity_id": IDS["column"]},
        ],
        "created_at": TIMESTAMP,
    }
    question = {
        "question_id": IDS["question"],
        "text": "O campo representa medida ou identificador?",
        "reason": "Validação de exemplo.",
        "question_type": "single_choice",
        "priority": "high",
        "blocking": True,
        "status": "pending",
        "options": [{"option_id": "measure", "label": "Medida"}],
        "impact": {"affected_modules": ["quality"], "affected_rule_ids": ["QLT-NUMTEXT-007"], "affected_recommendation_ids": []},
        "answer": None,
        "created_at": TIMESTAMP,
    }
    example["findings"] = [finding]
    example["questions"] = [question]
    example["file"]["finding_ids"] = [IDS["finding"]]  # type: ignore[index]
    example["summary"]["counts"]["risks"] = 1  # type: ignore[index]
    example["summary"]["top_risk_finding_ids"] = [IDS["finding"]]  # type: ignore[index]
    example["sheets"][0]["finding_ids"] = [IDS["finding"]]  # type: ignore[index]
    example["sheets"][0]["question_ids"] = [IDS["question"]]  # type: ignore[index]
    return example


def build_invalid_example() -> dict[str, object]:
    example = build_complete_example()
    example["unexpected_property"] = True
    return example
