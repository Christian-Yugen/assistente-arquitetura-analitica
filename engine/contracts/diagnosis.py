"""Fragmentos do contrato de diagnóstico produzidos pelo motor de regras."""

from __future__ import annotations

from datetime import UTC, datetime
from uuid import uuid4

CONTRACT_ID = "PM-MVP-PBI-CON-001"
SCHEMA_VERSION = "1.0.0"
RULE_VERSIONS = {
    "QLT-NUMTEXT-007": "1.0.0-draft",
    "QLT-NULL-001": "0.1.0-reconstructed.1",
}


def _timestamp() -> str:
    return datetime.now(UTC).isoformat().replace("+00:00", "Z")


def to_diagnosis_fragment(
    findings: list[dict[str, object]],
    *,
    sheet_id: str,
    column_id: str,
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
                "affected_entities": [
                    {"entity_type": "sheet", "entity_id": sheet_id},
                    {"entity_type": "column", "entity_id": column_id},
                ],
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
