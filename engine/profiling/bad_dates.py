"""Profiling agregado de datas textuais inválidas em gramáticas estritas aprovadas."""

from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import date, datetime
from typing import Iterable

from engine.profiling.missingness import missing_class


ISO_DATE_TEXT = re.compile(r"^\d{4}-\d{2}-\d{2}$")
BR_DATE_HYPHEN_TEXT = re.compile(r"^\d{2}-\d{2}-\d{4}$")
BR_DATE_SLASH_TEXT = re.compile(r"^\d{2}/\d{2}/\d{4}$")
NORMALIZATION_BASIS = "missingness_excluded__strict_iso_and_pt_br_date_text_v1"


@dataclass(frozen=True)
class BadDateProfile:
    """Contagens de candidatos estritos e falhas de calendário, sem valores ou posições."""

    strict_date_candidate_count: int = 0
    invalid_strict_date_count: int = 0
    invalid_strict_date_ratio: float = 0.0
    normalization_basis: str = NORMALIZATION_BASIS


class BadDateAccumulator:
    """Avalia somente as três gramáticas autorizadas enquanto descarta conteúdo após a contagem."""

    def __init__(self) -> None:
        self._strict_date_candidate_count = 0
        self._invalid_strict_date_count = 0

    def consume(self, value: object) -> None:
        if missing_class(value) is not None or isinstance(value, (date, datetime)) or not isinstance(value, str):
            return
        normalized = value.strip()
        parser = self._parser_for(normalized)
        if parser is None:
            return
        self._strict_date_candidate_count += 1
        try:
            parser(normalized)
        except ValueError:
            self._invalid_strict_date_count += 1

    @staticmethod
    def _parser_for(value: str):
        if ISO_DATE_TEXT.fullmatch(value):
            return date.fromisoformat
        if BR_DATE_HYPHEN_TEXT.fullmatch(value):
            return lambda candidate: datetime.strptime(candidate, "%d-%m-%Y").date()
        if BR_DATE_SLASH_TEXT.fullmatch(value):
            return lambda candidate: datetime.strptime(candidate, "%d/%m/%Y").date()
        return None

    def finalize(self) -> BadDateProfile:
        ratio = (
            round(self._invalid_strict_date_count / self._strict_date_candidate_count, 8)
            if self._strict_date_candidate_count
            else 0.0
        )
        return BadDateProfile(
            strict_date_candidate_count=self._strict_date_candidate_count,
            invalid_strict_date_count=self._invalid_strict_date_count,
            invalid_strict_date_ratio=ratio,
        )


def profile_bad_dates(values: Iterable[object]) -> BadDateProfile:
    accumulator = BadDateAccumulator()
    for value in values:
        accumulator.consume(value)
    return accumulator.finalize()
