"""GRN-EXPL-002: hipótese privada de chave explícita única por aba."""

from __future__ import annotations

from dataclasses import dataclass

from engine.profiling.explicit_key_grain import ExplicitKeyHeaderProfile


@dataclass(frozen=True)
class ExplicitKeyColumnProfile:
    header: ExplicitKeyHeaderProfile
    identifier_signal: bool
    sensitive_header: bool
    description_header: bool
    recognized_date_count: int
    physical_type: str
    non_missing_count: int
    distinct_non_missing_count: int
    formula_count: int


@dataclass(frozen=True)
class ExplicitKeySheetProfile:
    observed_row_count: int
    columns: tuple[ExplicitKeyColumnProfile, ...]
    basis: str = "single_closed_explicit_key_with_aggregate_uniqueness_v1"


def classify_explicit_key(profile: ExplicitKeySheetProfile) -> list[dict[str, object]]:
    """Emite somente uma hipótese agregada e bloqueante, sem coluna nem valores."""

    eligible = tuple(
        column
        for column in profile.columns
        if (
            column.header.header_eligible
            and not column.sensitive_header
            and not column.description_header
            and column.recognized_date_count == 0
            and column.physical_type in {"text", "numeric"}
        )
    )
    complete = tuple(column for column in eligible if column.non_missing_count == profile.observed_row_count)
    unique = tuple(
        column
        for column in complete
        if column.distinct_non_missing_count == profile.observed_row_count
    )
    formula_count = sum(column.formula_count for column in eligible)
    ambiguity_count = max(0, len(unique) - 1)

    if (
        profile.observed_row_count < 20
        or len(eligible) < 1
        or len(unique) != 1
        or formula_count != 0
        or ambiguity_count != 0
    ):
        return []

    return [{
        "rule_id": "GRN-EXPL-002",
        "grain_type": "explicit_key_candidate",
        "confidence": 0.85,
        "evidence": {
            "observed_row_count": profile.observed_row_count,
            "eligible_candidate_count": len(eligible),
            "candidate_complete_count": len(complete),
            "candidate_unique_count": len(unique),
            "candidate_formula_count": formula_count,
            "ambiguity_count": ambiguity_count,
            "basis": profile.basis,
        },
        "question": {
            "text": "Confirme se existe uma coluna explicitamente designada como identificador único de cada linha desta aba.",
            "reason": "A completude e a unicidade observadas são sinais técnicos e não confirmam a chave de negócio sem validação humana.",
            "question_type": "confirmation",
            "priority": "high",
            "blocking": True,
            "options": [],
        },
    }]


def classify_explicit_key_eligible_subset(
    profile: ExplicitKeySheetProfile,
    *,
    excluded_invalid_key_rows: int,
) -> list[dict[str, object]]:
    """Avalia um subconjunto elegível com contagens agregadas, sem apagar linhas.

    API opt-in: o pipeline não deve chamá-la antes de comprovar que as linhas
    excluídas são precisamente as que possuem chave inválida e que os demais
    agregados representam o mesmo subconjunto. Não substitui o passe completo.
    """
    if (
        isinstance(excluded_invalid_key_rows, bool)
        or not isinstance(excluded_invalid_key_rows, int)
        or excluded_invalid_key_rows < 0
        or excluded_invalid_key_rows >= profile.observed_row_count
    ):
        raise ValueError("invalid_eligible_subset_count")
    eligible_count = profile.observed_row_count - excluded_invalid_key_rows
    if excluded_invalid_key_rows == 0:
        return classify_explicit_key(profile)
    # Conservador: só aceita uma chave candidata e nulos exatamente iguais
    # às linhas excluídas. Não converte duplicidades em unicidade.
    candidates = [column for column in profile.columns if column.header.header_eligible and not column.sensitive_header and not column.description_header and column.recognized_date_count == 0 and column.physical_type in {"text", "numeric"}]
    if len(candidates) != 1:
        return []
    column = candidates[0]
    if column.non_missing_count != eligible_count or column.distinct_non_missing_count != eligible_count:
        return []
    reduced = ExplicitKeySheetProfile(
        observed_row_count=eligible_count,
        columns=(column,),
        basis="eligible_subset_null_key_exclusion_aggregate_v1",
    )
    results = classify_explicit_key(reduced)
    for result in results:
        result["evidence"]["original_observed_row_count"] = profile.observed_row_count
        result["evidence"]["excluded_invalid_key_row_count"] = excluded_invalid_key_rows
        result["evidence"]["eligible_row_count"] = eligible_count
    return results
