from __future__ import annotations

import unicodedata
from dataclasses import dataclass
from typing import Iterable


HEADERS_BASIS = "first_materialized_row_missing_duplicate_normalized_multilevel_horizontal_merge_v1"


@dataclass(frozen=True)
class HeadersProfile:
    header_column_count: int = 0
    missing_header_count: int = 0
    duplicate_normalized_group_count: int = 0
    duplicate_header_count: int = 0
    multilevel_candidate_count: int = 0
    basis: str = HEADERS_BASIS


def _value(cell: object) -> object:
    return getattr(cell, "value", cell)


def _data_type(cell: object) -> object:
    return getattr(cell, "data_type", None)


def _is_missing_header(cell: object) -> bool:
    value = _value(cell)
    return _data_type(cell) == "f" or value is None or (isinstance(value, str) and not value.strip())


def _normalized_text(cell: object) -> str | None:
    value = _value(cell)
    if not isinstance(value, str) or _data_type(cell) == "f":
        return None
    normalized = unicodedata.normalize("NFKC", value).strip().casefold()
    normalized = "".join(
        character for character in unicodedata.normalize("NFD", normalized) if unicodedata.category(character) != "Mn"
    )
    normalized = " ".join(normalized.split())
    return normalized or None


def _is_physical_nonempty(cell: object | None) -> bool:
    if cell is None:
        return False
    value = _value(cell)
    return value is not None and not (isinstance(value, str) and not value.strip())


def profile_headers(
    header_cells: Iterable[object],
    second_row_cells: Iterable[object] | None,
    merged_ranges: Iterable[tuple[int, int, int, int]],
) -> HeadersProfile:
    """Produz somente contagens agregadas; textos, coordenadas e ranges são descartados."""

    headers = tuple(header_cells)
    second_row = tuple(second_row_cells or ())
    normalized_counts: dict[str, int] = {}
    missing_header_count = 0
    for cell in headers:
        if _is_missing_header(cell):
            missing_header_count += 1
            continue
        normalized = _normalized_text(cell)
        if normalized is not None:
            normalized_counts[normalized] = normalized_counts.get(normalized, 0) + 1

    duplicate_groups = [count for count in normalized_counts.values() if count >= 2]
    multilevel_candidate_count = 0
    for min_col, min_row, max_col, _max_row in merged_ranges:
        if min_row != 1 or max_col - min_col + 1 < 2:
            continue
        occupied = sum(
            1
            for position in range(min_col - 1, max_col)
            if position < len(second_row) and _is_physical_nonempty(second_row[position])
        )
        if occupied >= 2:
            multilevel_candidate_count += 1

    return HeadersProfile(
        header_column_count=len(headers),
        missing_header_count=missing_header_count,
        duplicate_normalized_group_count=len(duplicate_groups),
        duplicate_header_count=sum(duplicate_groups),
        multilevel_candidate_count=multilevel_candidate_count,
    )
