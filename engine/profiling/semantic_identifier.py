"""Perfil agregado e privado para a SEM-ID-003."""

from __future__ import annotations

import math
import unicodedata
from collections import Counter
from dataclasses import dataclass
from datetime import date, datetime
from typing import Iterable

from engine.profiling.missingness import missing_class

SEMANTIC_IDENTIFIER_BASIS = "closed_header_signal_text_or_numeric_coverage90_distinct10_min20_v1"
ELIGIBLE_HEADERS = frozenset({"id", "codigo", "cod", "chave", "matricula", "numero", "num"})
SENSITIVE_HEADERS = frozenset({"cpf", "cnpj", "email", "e-mail", "nome", "telefone", "celular", "endereco", "endereço"})


def _normalize_header(value: str) -> str:
    decomposed = unicodedata.normalize("NFKD", unicodedata.normalize("NFKC", value))
    return " ".join("".join(char for char in decomposed if not unicodedata.combining(char)).casefold().split())


def _signature(value: object) -> tuple[str, str] | None:
    if isinstance(value, bool):
        return None
    if isinstance(value, str):
        return ("text", unicodedata.normalize("NFKC", value)) if not value.startswith("=") else None
    if isinstance(value, int):
        return ("integer", str(value))
    if isinstance(value, float):
        return ("float", repr(value)) if math.isfinite(value) else None
    if isinstance(value, datetime):
        return ("datetime", value.isoformat())
    if isinstance(value, date):
        return ("date", value.isoformat())
    return None


@dataclass(frozen=True)
class SemanticIdentifierProfile:
    observed_count: int = 0
    non_missing_count: int = 0
    distinct_non_missing_count: int = 0
    non_missing_ratio: float = 0.0
    distinct_ratio: float = 0.0
    header_signal: bool = False
    sensitive_header: bool = False
    basis: str = SEMANTIC_IDENTIFIER_BASIS


class SemanticIdentifierAccumulator:
    def __init__(self, header: str) -> None:
        normalized = _normalize_header(header)
        self._header_signal = normalized in ELIGIBLE_HEADERS
        self._sensitive_header = normalized in SENSITIVE_HEADERS
        self._observed = 0
        self._non_missing = 0
        self._signatures: Counter[tuple[str, str]] = Counter()

    def consume(self, value: object) -> None:
        self._observed += 1
        if missing_class(value) is not None:
            return
        self._non_missing += 1
        signature = _signature(value)
        if signature is not None:
            self._signatures[signature] += 1

    def finalize(self) -> SemanticIdentifierProfile:
        result = SemanticIdentifierProfile(
            observed_count=self._observed,
            non_missing_count=self._non_missing,
            distinct_non_missing_count=len(self._signatures),
            non_missing_ratio=round(self._non_missing / self._observed, 8) if self._observed else 0.0,
            distinct_ratio=round(len(self._signatures) / self._non_missing, 8) if self._non_missing else 0.0,
            header_signal=self._header_signal,
            sensitive_header=self._sensitive_header,
        )
        self._signatures.clear()
        return result


def profile_semantic_identifier(header: str, values: Iterable[object]) -> SemanticIdentifierProfile:
    accumulator = SemanticIdentifierAccumulator(header)
    for value in values:
        accumulator.consume(value)
    return accumulator.finalize()
