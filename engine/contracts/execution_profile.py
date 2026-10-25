"""Perfil versionado de marcadores permitidos para resultados parciais do MVP draft."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path


PROFILE_PATH = Path(__file__).resolve().parents[2] / "artifacts/contracts/PM-MVP-PBI-CON-001/draft-execution-profile-v1.1.json"

REQUIRED_GOVERNED_OUTPUT_PATHS = frozenset(
    {
        "analysis.assumptions[0]",
        "analysis.limitations[0]",
        "summary.completeness_ratio",
        "summary.executive_summary",
        "summary.next_recommended_action",
        "proposed_model.status",
        "proposed_model.limitations[0]",
        "execution.status",
        "execution.engine_version",
        "execution.ruleset_version",
        "execution.confidence_methodology_version",
        "execution.modules[0].module",
        "execution.modules[0].status",
        "execution.ai_usage",
    }
)


@dataclass(frozen=True)
class DraftExecutionProfile:
    profile_id: str
    profile_version: str
    engine_version: str
    ruleset_version: str
    confidence_methodology_version: str
    catalog_target_rule_count: int
    execution_status: str
    module_name: str
    module_status: str
    ai_usage: dict[str, object]
    assumption: str
    limitation: str
    proposed_model_status_with_hypotheses: str
    proposed_model_status_without_hypotheses: str
    proposed_model_limitation_with_hypotheses: str
    proposed_model_limitation_without_hypotheses: str
    summary_template: str
    next_action_with_hypotheses: str
    next_action_without_hypotheses: str
    governed_output_paths: tuple[str, ...]


def load_authorized_draft_profile(path: Path = PROFILE_PATH) -> DraftExecutionProfile:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if payload["status"] != "authorized_for_mvp_draft" or payload["governance"]["production_ready"]:
        raise ValueError("Perfil de execução não está autorizado exclusivamente para modo draft.")
    markers = payload["partial_result_markers"]
    module = payload["module"]
    governed_output_paths = tuple(payload["governed_output_paths"])
    if frozenset(governed_output_paths) != REQUIRED_GOVERNED_OUTPUT_PATHS:
        raise ValueError("A allowlist do perfil draft não cobre exatamente todos os marcadores governados.")
    return DraftExecutionProfile(
        profile_id=payload["profile_id"],
        profile_version=payload["profile_version"],
        engine_version=payload["engine_version"],
        ruleset_version=payload["ruleset_version"],
        confidence_methodology_version=payload["confidence_methodology_version"],
        catalog_target_rule_count=payload["catalog_target_rule_count"],
        execution_status=payload["execution_status"],
        module_name=module["name"],
        module_status=module["status"],
        ai_usage=payload["ai_usage"],
        assumption=markers["assumption"],
        limitation=markers["limitation"],
        proposed_model_status_with_hypotheses=markers["proposed_model_status_with_hypotheses"],
        proposed_model_status_without_hypotheses=markers["proposed_model_status_without_hypotheses"],
        proposed_model_limitation_with_hypotheses=markers["proposed_model_limitation_with_hypotheses"],
        proposed_model_limitation_without_hypotheses=markers["proposed_model_limitation_without_hypotheses"],
        summary_template=markers["summary_template"],
        next_action_with_hypotheses=markers["next_action_with_hypotheses"],
        next_action_without_hypotheses=markers["next_action_without_hypotheses"],
        governed_output_paths=governed_output_paths,
    )


def _read_path(diagnosis: dict[str, object], path: str) -> object:
    current: object = diagnosis
    for segment in path.split("."):
        if "[" in segment:
            key, raw_index = segment.removesuffix("]").split("[")
            if not isinstance(current, dict):
                raise ValueError(f"Caminho inválido para marcador governado: {path}")
            current = current[key]
            if not isinstance(current, list):
                raise ValueError(f"Caminho não resolve para lista: {path}")
            current = current[int(raw_index)]
        else:
            if not isinstance(current, dict):
                raise ValueError(f"Caminho inválido para marcador governado: {path}")
            current = current[segment]
    return current


def expected_governed_output_values(
    diagnosis: dict[str, object], *, profile: DraftExecutionProfile, executed_rule_count: int
) -> dict[str, object]:
    sheets = diagnosis["sheets"]
    findings = diagnosis["findings"]
    questions = diagnosis["questions"]
    if not isinstance(sheets, list) or not isinstance(findings, list) or not isinstance(questions, list):
        raise ValueError("Diagnóstico parcial inválido para validar marcadores governados.")
    column_count = sum(sheet["column_count"] for sheet in sheets if isinstance(sheet, dict))
    proposed_model = diagnosis.get("proposed_model", {})
    relationships = diagnosis.get("relationships", [])
    metrics = diagnosis.get("metrics", [])
    grain_count = sum(1 for sheet in sheets if isinstance(sheet, dict) and sheet.get("grain") is not None)
    has_hypotheses = bool(
        (isinstance(proposed_model, dict) and proposed_model.get("tables"))
        or relationships
        or metrics
        or grain_count
    )
    fact_count = sum(
        1
        for table in proposed_model.get("tables", []) if isinstance(proposed_model, dict) and isinstance(table, dict)
        and str(table.get("table_type", "")).startswith("fact_")
    )
    dimension_count = sum(
        1
        for table in proposed_model.get("tables", []) if isinstance(proposed_model, dict) and isinstance(table, dict)
        and str(table.get("table_type", "")).startswith("dimension_")
    )
    return {
        "analysis.assumptions[0]": profile.assumption,
        "analysis.limitations[0]": profile.limitation,
        "summary.completeness_ratio": round(executed_rule_count / profile.catalog_target_rule_count, 8),
        "summary.executive_summary": profile.summary_template.format(sheet_count=len(sheets), column_count=column_count, finding_count=len(findings), fact_count=fact_count, dimension_count=dimension_count, grain_count=grain_count, relationship_count=len(relationships), metric_count=len(metrics)),
        "summary.next_recommended_action": profile.next_action_with_hypotheses if has_hypotheses else profile.next_action_without_hypotheses,
        "proposed_model.status": profile.proposed_model_status_with_hypotheses if has_hypotheses else profile.proposed_model_status_without_hypotheses,
        "proposed_model.limitations[0]": profile.proposed_model_limitation_with_hypotheses if has_hypotheses else profile.proposed_model_limitation_without_hypotheses,
        "execution.status": profile.execution_status,
        "execution.engine_version": profile.engine_version,
        "execution.ruleset_version": profile.ruleset_version,
        "execution.confidence_methodology_version": profile.confidence_methodology_version,
        "execution.modules[0].module": profile.module_name,
        "execution.modules[0].status": profile.module_status,
        "execution.ai_usage": profile.ai_usage,
    }


def validate_governed_output(
    diagnosis: dict[str, object], *, profile: DraftExecutionProfile, executed_rule_count: int
) -> None:
    expected = expected_governed_output_values(diagnosis, profile=profile, executed_rule_count=executed_rule_count)
    if set(expected) != set(profile.governed_output_paths):
        raise ValueError("A lista de valores esperados diverge da allowlist aprovada.")
    mismatches = {
        path: {"expected": value, "actual": _read_path(diagnosis, path)}
        for path, value in expected.items()
        if _read_path(diagnosis, path) != value
    }
    if mismatches:
        raise ValueError(f"Marcadores governados divergentes do perfil autorizado: {mismatches}")
