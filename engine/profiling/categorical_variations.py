"""Profiling agregado para a QLT-CATVAR-008 sem reter rótulos de categorias."""

from __future__ import annotations

import json
import re
import unicodedata
from collections import Counter, defaultdict
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Iterable


NORMALIZATION_BASIS = "technical_expanded_nfkd_casefold_punctuation_whitespace_v1"
MAX_DISTINCT_TEXT_VALUES = 100
DICTIONARY_PATH = Path(__file__).resolve().parents[2] / "artifacts/rules/QLT-CATVAR-008/provisional-domain-dictionary-v1.json"


class CategoricalVariationDictionaryError(ValueError):
    """Impede o uso silencioso de equivalências de domínio ainda não autorizadas."""


@dataclass(frozen=True)
class CategoricalVariationProfile:
    text_value_count: int = 0
    distinct_text_count: int = 0
    collision_group_count: int = 0
    affected_value_count: int = 0
    affected_value_ratio: float = 0.0
    max_variants_in_group: int = 0
    high_cardinality: bool = False
    normalization_basis: str = NORMALIZATION_BASIS
    dictionary_status: str = "empty_pending_domain_approval"
    dictionary_entry_count: int = 0


@lru_cache(maxsize=1)
def _load_dictionary_metadata() -> tuple[str, int]:
    payload = json.loads(DICTIONARY_PATH.read_text(encoding="utf-8"))
    mappings = payload.get("mappings")
    status = payload.get("status")
    if not isinstance(mappings, dict) or not isinstance(status, str):
        raise CategoricalVariationDictionaryError("Artefato de dicionário de domínio inválido.")
    if mappings:
        raise CategoricalVariationDictionaryError(
            "O dicionário de domínio contém entradas sem política versionada e gate específico."
        )
    return status, 0


def normalize_category_text(value: str) -> str:
    """Normaliza apenas diferenças técnicas; não trata sinônimos, pluralização ou abreviação."""

    decomposed = unicodedata.normalize("NFKD", value.strip())
    without_marks = "".join(character for character in decomposed if not unicodedata.combining(character))
    punctuation_as_space = re.sub(r"[\W_]+", " ", without_marks.casefold(), flags=re.UNICODE)
    return re.sub(r"\s+", " ", punctuation_as_space).strip()


def profile_categorical_variations(values: Iterable[object]) -> CategoricalVariationProfile:
    """Computa colisões de grafia em memória e retorna somente métricas agregadas."""

    dictionary_status, dictionary_entry_count = _load_dictionary_metadata()
    text_values = [value.strip() for value in values if isinstance(value, str) and value.strip()]
    raw_counts = Counter(text_values)
    normalized_variants: dict[str, set[str]] = defaultdict(set)
    normalized_counts: Counter[str] = Counter()
    for raw_value, count in raw_counts.items():
        normalized = normalize_category_text(raw_value)
        if not normalized:
            continue
        normalized_variants[normalized].add(raw_value)
        normalized_counts[normalized] += count

    collision_keys = [key for key, variants in normalized_variants.items() if len(variants) >= 2]
    affected_value_count = sum(normalized_counts[key] for key in collision_keys)
    distinct_text_count = len(raw_counts)
    return CategoricalVariationProfile(
        text_value_count=len(text_values),
        distinct_text_count=distinct_text_count,
        collision_group_count=len(collision_keys),
        affected_value_count=affected_value_count,
        affected_value_ratio=round(affected_value_count / len(text_values), 8) if text_values else 0.0,
        max_variants_in_group=max((len(normalized_variants[key]) for key in collision_keys), default=0),
        high_cardinality=distinct_text_count > MAX_DISTINCT_TEXT_VALUES,
        dictionary_status=dictionary_status,
        dictionary_entry_count=dictionary_entry_count,
    )
