"""Fragmentos do contrato de diagnóstico produzidos pelo motor de regras."""

from __future__ import annotations

from datetime import UTC, datetime
from uuid import uuid4

CONTRACT_ID = "PM-MVP-PBI-CON-001"
SCHEMA_VERSION = "1.0.0"
RULE_VERSIONS = {
    "QLT-NUMTEXT-007": "1.0.0-draft",
    "QLT-NULL-001": "0.1.0-reconstructed.1",
    "QLT-CATVAR-008": "0.1.0-provisional.1",
    "QLT-DUP-002": "0.1.0-reconstructed.1",
    "QLT-EMPTYCOL-003": "0.1.0-reconstructed.1",
    "QLT-EMPTYROW-004": "0.1.0-reconstructed.1",
    "QLT-MIXTYPE-005": "0.1.0-provisional.1",
    "QLT-BADDATE-006": "0.1.0-provisional.1",
    "QLT-WHITESPACE-009": "0.1.0-provisional.1",
    "QLT-TOTALROW-010": "0.1.0-provisional.1",
    "QLT-NEGATIVE-011": "0.1.0-provisional.1",
    "QLT-OUTLIER-012": "0.1.0-provisional.1",
    "QLT-FORMULA-013": "0.1.0-provisional.1",
    "QLT-HEADERS-014": "0.1.0-provisional.1",
    "QLT-IDMISS-015": "0.1.0-provisional.1",
    "SEM-DATE-001": "0.1.0-provisional.1",
    "SEM-COMP-002": "0.1.0-provisional.1",
    "SEM-DESC-004": "0.1.0-provisional.1",
    "SEM-DUR-008": "0.1.0-provisional.1",
    "SEM-STATUS-009": "0.1.0-provisional.1",
    "SEM-CAT-010": "0.1.0-provisional.1",
    "SEM-LOC-011": "0.1.0-provisional.1",
    "SEM-RESP-012": "0.1.0-provisional.1",
    "SEM-CURR-006": "0.1.0-provisional.1",
    "SEM-ID-003": "0.1.0-provisional.1",
    "SEM-QTY-005": "0.1.0-provisional.1",
    "SEM-PCT-007": "0.1.0-provisional.1",
    "SEM-TARGET-013": "0.1.0-provisional.1",
    "SEM-ACTUAL-014": "0.1.0-provisional.1",
    "SEM-SENS-015": "0.1.0-provisional.1",
    "GRN-COMP-001": "0.1.0-provisional.1",
    "GRN-ENTITY-003": "0.1.0-provisional.1",
    "GRN-EVENT-004": "0.1.0-provisional.1",
    "GRN-EXPL-002": "0.1.0-provisional.1",
    "MDL-FACTPER-001": "0.1.0-provisional.1",
    "MDL-FACTTXN-002": "0.1.0-provisional.1",
    "MDL-FACTNOGRAIN-019": "0.1.0-provisional.1",
    "MDL-DIMSTD-004": "0.1.0-provisional.1",
    "MDL-DIMCAL-006": "0.1.0-provisional.1",
    "MDL-UNDEFINED-020": "0.1.0-provisional.1",
    "REL-ONEMANY-001": "0.1.0-provisional.1",
    "REL-NONUNIQ-002": "0.1.0-provisional.1",
    "REL-ORPHAN-003": "0.1.0-provisional.1",
    "REL-MANYMANY-004": "0.1.0-provisional.1",
    "REL-FACTFACT-006": "0.1.0-provisional.1",
    "REL-AMBIG-007": "0.1.0-provisional.1",
    "REL-BIDIR-008": "0.1.0-provisional.1",
    "REL-COMPKEY-009": "0.1.0-provisional.1",
    "REL-CONFORMED-010": "0.1.0-provisional.1",
    "MET-COMPL-001": "0.1.0-provisional.1",
    "MET-SUM-002": "0.1.0-provisional.1",
    "MET-COUNT-003": "0.1.0-provisional.1",
    "MET-DCOUNT-004": "0.1.0-provisional.1",
    "MET-AVG-005": "0.1.0-provisional.1",
    "MET-MINMAX-006": "0.1.0-provisional.1",
    "MET-RATE-007": "0.1.0-provisional.1",
    "MET-ABSDELTA-008": "0.1.0-provisional.1",
    "MET-PCTDELTA-009": "0.1.0-provisional.1",
    "MET-RUNNING-010": "0.1.0-provisional.1",
    "MET-WAVG-011": "0.1.0-provisional.1",
    "MET-SEMIADD-012": "0.1.0-provisional.1",
    "MET-DOMAIN-013": "0.1.0-provisional.1",
    "MET-IMPOSS-014": "0.1.0-provisional.1",
    "MET-DAX-015": "0.1.0-provisional.1",
    "ALT-SENS-001": "0.1.0-provisional.1",
    "ALT-QUALITY-002": "0.1.0-provisional.1",
    "ALT-GRAIN-003": "0.1.0-provisional.1",
    "ALT-KEY-004": "0.1.0-provisional.1",
    "ALT-AMBIG-005": "0.1.0-provisional.1",
    "ALT-METRIC-006": "0.1.0-provisional.1",
    "ALT-SUMPCT-007": "0.1.0-provisional.1",
    "ALT-AVGAVG-008": "0.1.0-provisional.1",
}


def _timestamp() -> str:
    return datetime.now(UTC).isoformat().replace("+00:00", "Z")


def to_diagnosis_fragment(
    findings: list[dict[str, object]],
    *,
    sheet_id: str,
    column_id: str | None,
) -> dict[str, object]:
    """Converte findings internos em `findings` e `questions` rastreáveis do contrato raiz.

    O fragmento é deliberadamente agregado: ele preserva contagens, razões e a base técnica,
    mas nunca transporta valores de células para o contrato de saída.
    """

    created_at = _timestamp()
    contract_findings: list[dict[str, object]] = []
    contract_questions: list[dict[str, object]] = []

    for finding in findings:
        rule_id = str(finding["rule_id"])
        rule_version = RULE_VERSIONS.get(rule_id)
        if not rule_version:
            raise ValueError(f"Versão de regra não registrada para {rule_id}.")
        evidence = [
            {
                "code": item["code"],
                "effect": item["effect"],
                "observed": {
                    key: value
                    for key, value in item.items()
                    if key in {"observed_value", "observed_ratio"}
                },
                "expected_condition": item["expected_condition"],
            }
            for item in finding["evidence"]
        ]
        affected_entities = [{"entity_type": "sheet", "entity_id": sheet_id}]
        if column_id is not None:
            affected_entities.append({"entity_type": "column", "entity_id": column_id})
        contract_findings.append(
            {
                "finding_id": str(uuid4()),
                "category": finding["category"],
                "severity": finding["severity"],
                "status": "open",
                "title": finding["title"],
                "description": finding["description"],
                "evidence": evidence,
                "impact": finding["impact"],
                "recommendation": finding["recommendation"],
                "rule_id": rule_id,
                "rule_version": rule_version,
                "affected_entities": affected_entities,
                "created_at": created_at,
            }
        )

        if finding["question"]:
            question = finding["question"]
            contract_questions.append(
                {
                    "question_id": str(uuid4()),
                    "text": question["text"],
                    "reason": question["reason"],
                    "question_type": question["question_type"],
                    "priority": question["priority"],
                    "blocking": question["blocking"],
                    "status": "pending",
                    "options": question["options"],
                    "impact": {
                        "affected_modules": question["affected_modules"],
                        "affected_rule_ids": [finding["rule_id"]],
                        "affected_recommendation_ids": [],
                    },
                    "answer": None,
                    "created_at": created_at,
                }
            )

    return {
        "schema_version": SCHEMA_VERSION,
        "contract_id": CONTRACT_ID,
        "findings": contract_findings,
        "questions": contract_questions,
    }


def to_semantic_classification_fragment(classifications: list[dict[str, object]], *, sheet_id: str, column_id: str) -> dict[str, object]:
    """Projeta classificações agregadas sem valores brutos, cabeçalhos ou posições."""
    projected: list[dict[str, object]] = []
    questions: list[dict[str, object]] = []
    created_at = _timestamp()
    for classification in classifications:
        rule_id = str(classification["rule_id"])
        projected.append({"semantic_type": classification["semantic_type"], "confidence": classification["confidence"],
                          "evidence": classification["evidence"], "rule_id": rule_id,
                          "rule_version": RULE_VERSIONS[rule_id],
                          "affected_entities": [{"entity_type": "sheet", "entity_id": sheet_id}, {"entity_type": "column", "entity_id": column_id}]})
        question = classification["question"]
        questions.append({"question_id": str(uuid4()), "text": question["text"], "reason": question["reason"],
                          "question_type": question["question_type"], "priority": question["priority"], "blocking": question["blocking"],
                          "status": "pending", "options": question["options"],
                          "impact": {"affected_modules": ["semantic_typing"], "affected_rule_ids": [rule_id], "affected_recommendation_ids": []}, "answer": None, "created_at": created_at})
    return {"semantic_classifications": projected, "questions": questions}


def to_sensitivity_fragment(classifications: list[dict[str, object]], *, sheet_id: str, column_id: str) -> dict[str, object]:
    """Projeta candidatos de sensibilidade em coleção própria, sem dados brutos ou cabeçalhos."""
    projected: list[dict[str, object]] = []
    questions: list[dict[str, object]] = []
    created_at = _timestamp()
    for classification in classifications:
        rule_id = str(classification["rule_id"])
        rule_version = RULE_VERSIONS.get(rule_id)
        if not rule_version:
            raise ValueError(f"Versão de regra não registrada para {rule_id}.")
        projected.append({"sensitivity": classification["sensitivity"], "confidence": classification["confidence"],
                          "evidence": classification["evidence"], "rule_id": rule_id,
                          "rule_version": rule_version,
                          "affected_entities": [{"entity_type": "sheet", "entity_id": sheet_id}, {"entity_type": "column", "entity_id": column_id}]})
        question = classification["question"]
        questions.append({"question_id": str(uuid4()), "text": question["text"], "reason": question["reason"],
                          "question_type": question["question_type"], "priority": question["priority"], "blocking": question["blocking"],
                          "status": "pending", "options": question["options"],
                          "impact": {"affected_modules": ["sensitivity"], "affected_rule_ids": [rule_id], "affected_recommendation_ids": []}, "answer": None, "created_at": created_at})
    return {"sensitivity_classifications": projected, "questions": questions}


def to_grain_fragment(candidates: list[dict[str, object]], *, sheet_id: str) -> dict[str, object]:
    """Projeta uma hipótese de grão por aba com evidência exclusivamente agregada."""
    if not candidates:
        return {"grain": None, "questions": []}
    candidate = candidates[0]
    rule_id = str(candidate["rule_id"])
    question = candidate["question"]
    created_at = _timestamp()
    return {
        "grain": {
            "type": candidate["grain_type"], "confidence": candidate["confidence"],
            "evidence": candidate["evidence"], "rule_id": rule_id,
            "rule_version": RULE_VERSIONS[rule_id], "status": "hypothesis",
        },
        "questions": [{
            "question_id": str(uuid4()), "text": question["text"], "reason": question["reason"],
            "question_type": question["question_type"], "priority": question["priority"],
            "blocking": question["blocking"], "status": "pending", "options": question["options"],
            "impact": {"affected_modules": ["granularity"], "affected_rule_ids": [rule_id], "affected_recommendation_ids": []},
            "answer": None, "created_at": created_at,
        }],
    }


def to_table_classification_fragment(candidates: list[dict[str, object]], *, sheet_id: str) -> dict[str, object]:
    """Projeta uma classificação de tabela por aba e a confirmação humana correspondente."""
    if not candidates:
        return {"classification": None, "questions": []}
    candidate = candidates[0]
    created_at = _timestamp()
    return {
        "classification": {
            "type": candidate["classification_type"], "confidence": candidate["confidence"],
            "evidence": candidate["evidence"], "rule_id": str(candidate["rule_id"]),
            "rule_version": RULE_VERSIONS[str(candidate["rule_id"])], "status": "hypothesis",
        },
        "questions": [{
            "question_id": str(uuid4()), "text": candidate_question["text"], "reason": candidate_question["reason"],
            "question_type": candidate_question["question_type"], "priority": candidate_question["priority"],
            "blocking": candidate_question["blocking"], "status": "pending", "options": candidate_question["options"],
            "impact": {"affected_modules": ["fact_dimension"], "affected_rule_ids": [str(item["rule_id"])], "affected_recommendation_ids": []},
            "answer": None, "created_at": created_at,
        } for item in candidates for candidate_question in [item["question"]]],
    }


def to_relationship_fragment(
    candidates: list[dict[str, object]],
    *,
    source_sheet_id: str,
    target_sheet_id: str,
) -> dict[str, object]:
    """Projeta hipótese REL por IDs opacos de abas, com confirmação humana bloqueante."""

    relationships: list[dict[str, object]] = []
    questions: list[dict[str, object]] = []
    created_at = _timestamp()
    for candidate in candidates:
        rule_id = str(candidate["rule_id"])
        rule_version = RULE_VERSIONS.get(rule_id)
        if not rule_version:
            raise ValueError(f"Versão de regra não registrada para {rule_id}.")
        relationships.append(
            {
                "source": {"entity_type": "sheet", "entity_id": source_sheet_id},
                "target": {"entity_type": "sheet", "entity_id": target_sheet_id},
                "relationship_type": candidate["relationship_type"],
                "confidence": candidate["confidence"],
                "severity": candidate["severity"],
                "evidence": candidate["evidence"],
                "rule_id": rule_id,
                "rule_version": rule_version,
                "status": "hypothesis",
            }
        )
        question = candidate["question"]
        questions.append(
            {
                "question_id": str(uuid4()),
                "text": question["text"],
                "reason": question["reason"],
                "question_type": question["question_type"],
                "priority": question["priority"],
                "blocking": question["blocking"],
                "status": "pending",
                "options": question["options"],
                "impact": {
                    "affected_modules": ["relationships"],
                    "affected_rule_ids": [rule_id],
                    "affected_recommendation_ids": [],
                },
                "answer": None,
                "created_at": created_at,
            }
        )
    return {"relationships": relationships, "questions": questions}


def to_metric_fragment(candidates: list[dict[str, object]], *, sheet_id: str) -> dict[str, object]:
    """Projeta métricas conceituais por ID opaco de aba, sem valores, cabeçalhos ou DAX."""

    metrics: list[dict[str, object]] = []
    questions: list[dict[str, object]] = []
    created_at = _timestamp()
    for candidate in candidates:
        rule_id = str(candidate["rule_id"])
        rule_version = RULE_VERSIONS.get(rule_id)
        if not rule_version:
            raise ValueError(f"Versão de regra não registrada para {rule_id}.")
        metrics.append(
            {
                "scope": {"entity_type": "sheet", "entity_id": sheet_id},
                "metric_type": candidate["metric_type"],
                "confidence": candidate["confidence"],
                "severity": candidate["severity"],
                "conceptual_formula": candidate["conceptual_formula"],
                "evidence": candidate["evidence"],
                "rule_id": rule_id,
                "rule_version": rule_version,
                "status": "conceptual_review",
            }
        )
        question = candidate["question"]
        questions.append(
            {
                "question_id": str(uuid4()),
                "text": question["text"],
                "reason": question["reason"],
                "question_type": question["question_type"],
                "priority": question["priority"],
                "blocking": question["blocking"],
                "status": "pending",
                "options": question["options"],
                "impact": {"affected_modules": ["metric_suggestion"], "affected_rule_ids": [rule_id], "affected_recommendation_ids": []},
                "answer": None,
                "created_at": created_at,
            }
        )
    return {"metrics": metrics, "questions": questions}
