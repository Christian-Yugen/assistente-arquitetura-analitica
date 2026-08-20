"""Validação estrutural e cruzada do envelope de diagnóstico draft."""

from __future__ import annotations

import json
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker

from engine.contracts.models import ReconstructedDiagnosis


CANONICAL_SCHEMA_PATH = (
    Path(__file__).resolve().parents[2] / "artifacts/contracts/PM-MVP-PBI-CON-001/diagnosis.schema.json"
)


def load_canonical_schema() -> dict[str, object]:
    if not CANONICAL_SCHEMA_PATH.exists():
        raise RuntimeError("Schema reconstruído ausente; execute engine/contracts/export_reconstructed_schema.py.")
    return json.loads(CANONICAL_SCHEMA_PATH.read_text(encoding="utf-8"))


def validate_diagnosis_root(diagnosis: dict[str, object]) -> None:
    validator = Draft202012Validator(load_canonical_schema(), format_checker=FormatChecker())
    errors = sorted(validator.iter_errors(diagnosis), key=lambda error: list(error.path))
    if errors:
        messages = "; ".join(error.message for error in errors)
        raise ValueError(f"Diagnóstico inválido para PM-MVP-PBI-CON-001: {messages}")

    ReconstructedDiagnosis.model_validate(diagnosis)
