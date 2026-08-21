"""Profiling agregado de espaços marginais e invisíveis explicitamente autorizados."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from engine.profiling.missingness import missing_class


MARGINAL_SPACE_CHARACTERS = frozenset({" ", "\u00a0"})
EXPLICIT_HIDDEN_CHARACTERS = frozenset({"\u200b", "\u200c", "\u200d", "\u2060", "\ufeff"})
NORMALIZATION_BASIS = "missingness_excluded__marginal_ascii_or_nbsp__explicit_zero_width_v1"


@dataclass(frozen=True)
class WhitespaceProfile:
    """Contagens agregadas de sinais textuais aprovados, sem valores ou posições."""

    non_blank_text_count: int = 0
    leading_or_trailing_space_count: int = 0
    hidden_character_count: int = 0
    affected_text_count: int = 0
    affected_text_ratio: float = 0.0
    normalization_basis: str = NORMALIZATION_BASIS


class WhitespaceAccumulator:
    """Acumula somente os sinais explícitos e descarta o texto após a contagem."""

    def __init__(self) -> None:
        self._non_blank_text_count = 0
        self._leading_or_trailing_space_count = 0
        self._hidden_character_count = 0
        self._affected_text_count = 0

    def consume(self, value: object) -> None:
        if missing_class(value) is not None or not isinstance(value, str):
            return
        self._non_blank_text_count += 1
        has_marginal_space = value[0] in MARGINAL_SPACE_CHARACTERS or value[-1] in MARGINAL_SPACE_CHARACTERS
        has_hidden_character = any(character in EXPLICIT_HIDDEN_CHARACTERS for character in value)
        if has_marginal_space:
            self._leading_or_trailing_space_count += 1
        if has_hidden_character:
            self._hidden_character_count += 1
        if has_marginal_space or has_hidden_character:
            self._affected_text_count += 1

    def finalize(self) -> WhitespaceProfile:
        ratio = round(self._affected_text_count / self._non_blank_text_count, 8) if self._non_blank_text_count else 0.0
        return WhitespaceProfile(
            non_blank_text_count=self._non_blank_text_count,
            leading_or_trailing_space_count=self._leading_or_trailing_space_count,
            hidden_character_count=self._hidden_character_count,
            affected_text_count=self._affected_text_count,
            affected_text_ratio=ratio,
        )


def profile_whitespace(values: Iterable[object]) -> WhitespaceProfile:
    accumulator = WhitespaceAccumulator()
    for value in values:
        accumulator.consume(value)
    return accumulator.finalize()
