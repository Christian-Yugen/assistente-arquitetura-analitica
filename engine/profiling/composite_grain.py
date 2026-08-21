"""Perfil transitório e agregado de pares para a GRN-COMP-001."""

from __future__ import annotations

import math
import unicodedata
from dataclasses import dataclass
from datetime import date, datetime
from typing import Iterable

from engine.profiling.missingness import missing_class

COMPOSITE_GRAIN_BASIS = "semantic_identifier_components_complete_joint_unique_min20_max10_v1"


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
class CompositePairProfile:
    left_position: int
    right_position: int
    observed_row_count: int
    complete_pair_row_count: int
    left_distinct_count: int
    right_distinct_count: int
    joint_distinct_count: int
    joint_uniqueness_ratio: float


@dataclass(frozen=True)
class CompositeGrainProfile:
    eligible_pair_count: int = 0
    examined_pair_count: int = 0
    pairs: tuple[CompositePairProfile, ...] = ()
    basis: str = COMPOSITE_GRAIN_BASIS


class CompositeGrainAccumulator:
    """Mantém somente assinaturas transitórias de até dez pares e as limpa ao finalizar."""

    def __init__(self, pairs: Iterable[tuple[int, int]]) -> None:
        self._pairs = tuple(pairs)
        self._observed = {pair: 0 for pair in self._pairs}
        self._complete = {pair: 0 for pair in self._pairs}
        self._left = {pair: set[tuple[str, str]]() for pair in self._pairs}
        self._right = {pair: set[tuple[str, str]]() for pair in self._pairs}
        self._joint = {pair: set[tuple[tuple[str, str], tuple[str, str]]]() for pair in self._pairs}

    def consume(self, row: tuple[object, ...]) -> None:
        for pair in self._pairs:
            left_position, right_position = pair
            self._observed[pair] += 1
            left, right = row[left_position], row[right_position]
            if missing_class(left) is not None or missing_class(right) is not None:
                continue
            left_signature, right_signature = _signature(left), _signature(right)
            if left_signature is None or right_signature is None:
                continue
            self._complete[pair] += 1
            self._left[pair].add(left_signature)
            self._right[pair].add(right_signature)
            self._joint[pair].add((left_signature, right_signature))

    def finalize(self, *, eligible_pair_count: int) -> CompositeGrainProfile:
        profiles = []
        for left_position, right_position in self._pairs:
            pair = (left_position, right_position)
            complete = self._complete[pair]
            profiles.append(CompositePairProfile(
                left_position=left_position,
                right_position=right_position,
                observed_row_count=self._observed[pair],
                complete_pair_row_count=complete,
                left_distinct_count=len(self._left[pair]),
                right_distinct_count=len(self._right[pair]),
                joint_distinct_count=len(self._joint[pair]),
                joint_uniqueness_ratio=round(len(self._joint[pair]) / complete, 8) if complete else 0.0,
            ))
        self._left.clear()
        self._right.clear()
        self._joint.clear()
        return CompositeGrainProfile(
            eligible_pair_count=eligible_pair_count,
            examined_pair_count=len(profiles),
            pairs=tuple(profiles),
        )
