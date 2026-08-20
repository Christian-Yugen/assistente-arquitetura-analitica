"""Fonte versionada do schema reconstruído a partir do DOCX aprovado da Fase 2."""

from __future__ import annotations

from copy import deepcopy

from engine.contracts.schema import DIAGNOSIS_ROOT_SCHEMA


RECONSTRUCTED_CONTRACT_ID = "PM-MVP-PBI-CON-001"
RECONSTRUCTED_CONTRACT_VERSION = "1.0.0-reconstructed.1"


def build_reconstructed_schema() -> dict[str, object]:
    schema = deepcopy(DIAGNOSIS_ROOT_SCHEMA)
    schema.update(
        {
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "$id": "https://assistente-arquitetura-analitica.local/contracts/PM-MVP-PBI-CON-001/1.0.0-reconstructed.1/diagnosis.schema.json",
            "title": "PM-MVP-PBI-CON-001 — Diagnóstico Reconstruído",
            "description": "Representação canônica operacional reconstruída a partir do Contrato JSON Oficial do Diagnóstico — Fase 2 v1.0.",
            "x_reconstruction": {
                "status": "approved_reconstructed_for_mvp_draft",
                "contract_id": RECONSTRUCTED_CONTRACT_ID,
                "version": RECONSTRUCTED_CONTRACT_VERSION,
                "source_document": "Contrato_JSON_Oficial_Diagnostico_Fase2_v1.0.docx",
                "source_sections": {
                    "root_and_analysis": "7.1",
                    "file": "7.2",
                    "summary": "7.3",
                    "sheets_and_columns": "7.4",
                    "proposed_model": "7.5",
                    "relationships": "7.6",
                    "metrics": "7.7",
                    "questions": "7.8",
                    "findings": "7.9",
                    "execution": "7.10",
                    "enumerations": "8",
                    "structural_validation": "9.1",
                    "cross_validation": "9.2",
                },
                "known_gaps": [
                    "O JSON Schema original e os modelos Pydantic originais não foram disponibilizados.",
                    "Estruturas aninhadas sem propriedades detalhadas no DOCX permanecem como objetos ou arrays tipados, sem taxonomia de negócio inventada.",
                ],
                "promotion_policy": "Approved for MVP draft validation only; production promotion remains blocked pending original-artifact recovery or independent contract review.",
            },
        }
    )
    return schema
