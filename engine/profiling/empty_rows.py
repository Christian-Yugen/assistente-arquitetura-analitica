"""Profiling agregado de linhas vazias internas, sem reter posição ou conteúdo."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Sequence

from engine.profiling.missingness import row_has_meaningful_value


NORMALIZATION_BASIS = "missing_class_structural_null_blank_text_internal_blocks"


@dataclass(frozen=True)
class EmptyRowsProfile:
    """Somente métricas de blocos internos; linhas iniciais e finais são excluídas."""

    non_empty_row_count: int = 0
    empty_row_count: int = 0
    empty_row_ratio: float = 0.0
    empty_row_block_count: int = 0
    normalization_basis: str = NORMALIZATION_BASIS


class EmptyRowsAccumulator:
    """Mantém apenas contadores enquanto a aba é percorrida uma vez."""

    def __init__(self) -> None:
        self._seen_content = False
        self._pending_empty_count = 0
        self._non_empty_row_count = 0
        self._empty_row_count = 0
        self._empty_row_block_count = 0

    def consume(self, row: Sequence[object]) -> None:
        if row_has_meaningful_value(row):
            self._non_empty_row_count += 1
            if self._seen_content and self._pending_empty_count:
                self._empty_row_count += self._pending_empty_count
                self._empty_row_block_count += 1
            self._seen_content = True
            self._pending_empty_count = 0
            return
        if self._seen_content:
            self._pending_empty_count += 1

    def finalize(self) -> EmptyRowsProfile:
        denominator = self._non_empty_row_count + self._empty_row_count
        return EmptyRowsProfile(
            non_empty_row_count=self._non_empty_row_count,
            empty_row_count=self._empty_row_count,
            empty_row_ratio=round(self._empty_row_count / denominator, 8) if denominator else 0.0,
            empty_row_block_count=self._empty_row_block_count,
        )


def profile_empty_rows(rows: Iterable[Sequence[object]]) -> EmptyRowsProfile:
    accumulator = EmptyRowsAccumulator()
    for row in rows:
        accumulator.consume(row)
    return accumulator.finalize()
