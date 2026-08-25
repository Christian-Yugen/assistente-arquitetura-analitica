"""Controle de execução do catálogo oficial de 95 regras sem ativar políticas não aprovadas."""

from __future__ import annotations

import json
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Callable, Literal

from engine.quality.registry import QUALITY_RULE_IMPLEMENTATIONS
from engine.semantic.registry import SEMANTIC_RULE_IMPLEMENTATIONS
from engine.granularity.registry import GRANULARITY_RULE_IMPLEMENTATIONS
from engine.fact_dimension.registry import FACT_DIMENSION_RULE_IMPLEMENTATIONS
from engine.relationships.registry import RELATIONSHIP_RULE_IMPLEMENTATIONS


OFFICIAL_BLUEPRINT_PATH = Path(__file__).resolve().parents[1] / "artifacts/catalogs/official-rule-blueprint-95.json"
CURRENT_QUALITY_BASELINE = {"QLT-NULL-001", "QLT-DUP-002", "QLT-EMPTYCOL-003", "QLT-EMPTYROW-004", "QLT-MIXTYPE-005", "QLT-BADDATE-006", "QLT-WHITESPACE-009"}
DRAFT_RULE_AUTHORIZATIONS = {
    "QLT-NUMTEXT-007": "G7.4-R1",
    "QLT-NULL-001": "QLT-NULL-RECONSTRUCTION-001",
    "QLT-CATVAR-008": "QLT-CATVAR-008-DRAFT-CALIBRATION-001",
    "QLT-DUP-002": "QLT-DUP-002-DRAFT-CALIBRATION-001",
    "QLT-EMPTYCOL-003": "QLT-EMPTYCOL-003-DRAFT-CALIBRATION-001",
    "QLT-EMPTYROW-004": "QLT-EMPTYROW-004-DRAFT-CALIBRATION-001",
    "QLT-MIXTYPE-005": "QLT-MIXTYPE-005-DRAFT-CALIBRATION-001",
    "QLT-BADDATE-006": "QLT-BADDATE-006-DRAFT-CALIBRATION-001",
    "QLT-WHITESPACE-009": "QLT-WHITESPACE-009-DRAFT-CALIBRATION-001",
    "QLT-TOTALROW-010": "QLT-TOTALROW-010-DRAFT-CALIBRATION-001",
    "QLT-NEGATIVE-011": "QLT-NEGATIVE-011-DRAFT-CALIBRATION-001",
    "QLT-OUTLIER-012": "QLT-OUTLIER-012-DRAFT-CALIBRATION-001",
    "QLT-FORMULA-013": "QLT-FORMULA-013-DRAFT-CALIBRATION-001",
    "QLT-HEADERS-014": "QLT-HEADERS-014-DRAFT-CALIBRATION-001",
    "QLT-IDMISS-015": "QLT-IDMISS-015-DRAFT-CALIBRATION-001",
    "SEM-DATE-001": "SEM-DATE-001-DRAFT-CALIBRATION-001",
    "SEM-ID-003": "SEM-ID-003-DRAFT-CALIBRATION-001",
    "SEM-QTY-005": "SEM-QTY-005-DRAFT-CALIBRATION-001",
    "SEM-CURR-006": "SEM-CURR-006-DRAFT-CALIBRATION-001",
    "SEM-PCT-007": "SEM-PCT-007-DRAFT-CALIBRATION-001",
    "SEM-TARGET-013": "SEM-TARGET-013-DRAFT-CALIBRATION-001",
    "SEM-ACTUAL-014": "SEM-ACTUAL-014-DRAFT-CALIBRATION-001",
    "SEM-SENS-015": "SEM-SENS-015-DRAFT-CALIBRATION-001",
    "SEM-COMP-002": "SEM-COMP-002-DRAFT-CALIBRATION-001",
    "SEM-DESC-004": "SEM-DESC-004-DRAFT-CALIBRATION-001",
    "SEM-DUR-008": "SEM-DUR-008-DRAFT-CALIBRATION-001",
    "SEM-STATUS-009": "SEM-STATUS-009-DRAFT-CALIBRATION-001",
    "SEM-CAT-010": "SEM-CAT-010-DRAFT-CALIBRATION-001",
    "SEM-LOC-011": "SEM-LOC-011-DRAFT-CALIBRATION-001",
    "SEM-RESP-012": "SEM-RESP-012-DRAFT-CALIBRATION-001",
    "GRN-COMP-001": "GRN-COMP-001-DRAFT-CALIBRATION-001",
    "GRN-EVENT-004": "GRN-EVENT-004-DRAFT-CALIBRATION-001",
    "GRN-ENTITY-003": "GRN-ENTITY-003-DRAFT-CALIBRATION-001",
    "GRN-EXPL-002": "GRN-EXPL-002-DRAFT-CALIBRATION-001",
    "MDL-FACTPER-001": "MDL-FACTPER-001-DRAFT-CALIBRATION-001",
    "MDL-FACTTXN-002": "MDL-FACTTXN-002-DRAFT-CALIBRATION-001",
    "MDL-FACTNOGRAIN-019": "MDL-FACTNOGRAIN-019-DRAFT-CALIBRATION-001",
    "MDL-UNDEFINED-020": "MDL-UNDEFINED-020-DRAFT-CALIBRATION-001",
    "MDL-DIMSTD-004": "MDL-DIMSTD-004-DRAFT-CALIBRATION-001",
    "MDL-DIMCAL-006": "MDL-DIMCAL-006-DRAFT-CALIBRATION-001",
    "REL-ONEMANY-001": "REL-ONEMANY-001-DRAFT-CALIBRATION-001",
    "REL-NONUNIQ-002": "REL-NONUNIQ-002-DRAFT-CALIBRATION-001",
}
RULE_IMPLEMENTATIONS = {
    **QUALITY_RULE_IMPLEMENTATIONS,
    **SEMANTIC_RULE_IMPLEMENTATIONS,
    **GRANULARITY_RULE_IMPLEMENTATIONS,
    **FACT_DIMENSION_RULE_IMPLEMENTATIONS,
    **RELATIONSHIP_RULE_IMPLEMENTATIONS,
}
RuleExecutionStatus = Literal["executable_draft", "baseline_reference", "reference_catalog_draft", "reserved_definition", "unknown"]


@dataclass(frozen=True)
class RuleExecutionRecord:
    rule_id: str
    status: RuleExecutionStatus
    reason: str
    title: str | None = None
    official_implementation_status: str | None = None


class RuleExecutionUnavailableError(RuntimeError):
    """Erguido quando uma regra não possui política executável aprovada neste repositório."""


@lru_cache(maxsize=1)
def load_official_catalog() -> dict[str, dict[str, object]]:
    payload = json.loads(OFFICIAL_BLUEPRINT_PATH.read_text(encoding="utf-8"))
    if payload["blueprint_id"] != "PM-MVP-PBI-RULE-BP-001" or payload["target_count"] != 95:
        raise ValueError("Blueprint oficial inválido para o executor.")
    return {rule["rule_id"]: rule for rule in payload["rules"]}


def category_caps() -> dict[str, int]:
    caps: dict[str, int] = {}
    for rule_id in load_official_catalog():
        namespace = rule_id.split("-", 1)[0]
        caps[namespace] = caps.get(namespace, 0) + 1
    return caps


def get_rule_execution_record(rule_id: str) -> RuleExecutionRecord:
    if rule_id in RULE_IMPLEMENTATIONS and rule_id in DRAFT_RULE_AUTHORIZATIONS:
        rule = load_official_catalog()[rule_id]
        gate_id = DRAFT_RULE_AUTHORIZATIONS[rule_id]
        return RuleExecutionRecord(rule_id, "executable_draft", f"Implementação e gate draft {gate_id} disponíveis.", rule["title"], rule["implementation_status"])

    rule = load_official_catalog().get(rule_id)
    if not rule:
        return RuleExecutionRecord(rule_id, "unknown", "ID fora do blueprint oficial de 95 regras.")
    if rule_id in CURRENT_QUALITY_BASELINE:
        return RuleExecutionRecord(rule_id, "baseline_reference", "Baseline de Qualidade referenciada; artefato canônico executável ainda não foi promovido neste motor.", rule["title"], rule["implementation_status"])
    if rule["implementation_status"] == "reference_implemented_draft":
        return RuleExecutionRecord(rule_id, "reference_catalog_draft", "Regra de referência da Fase 3A.1; requer implementação, testes e gate locais antes da execução.", rule["title"], rule["implementation_status"])
    return RuleExecutionRecord(rule_id, "reserved_definition", "Slot oficial planejado sem política, evidências, testes e gate de implementação aprovados.", rule["title"], rule["implementation_status"])


def execute_registered_rule(rule_id: str, payload: object) -> object:
    record = get_rule_execution_record(rule_id)
    if record.status != "executable_draft":
        raise RuleExecutionUnavailableError(f"{rule_id} não pode ser executada: {record.reason}")
    evaluator: Callable[[object], object] = RULE_IMPLEMENTATIONS[rule_id]  # type: ignore[assignment]
    return evaluator(payload)


def executable_rule_count() -> int:
    return len(set(RULE_IMPLEMENTATIONS) & set(DRAFT_RULE_AUTHORIZATIONS))
