from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class AccumulatedSnapshotProfile:
    """Somente sinais independentes e agregados; nunca snapshot, saldo ou conteúdo de workbook."""
    independent_accumulated_snapshot_signal_count: int = 0
    confirmed_accumulated_snapshot_count: int = 0
    structural_conflict_count: int = 0
    sensitive_signal_count: int = 0
    contract_error_count: int = 0


def classify_accumulated_snapshot(profile: AccumulatedSnapshotProfile) -> list[dict[str, object]]:
    if not (
        profile.independent_accumulated_snapshot_signal_count >= 1
        and profile.confirmed_accumulated_snapshot_count == 0
        and profile.structural_conflict_count == 0
        and profile.sensitive_signal_count == 0
        and profile.contract_error_count == 0
    ):
        return []
    return [{
        "rule_id": "MDL-FACTACC-003",
        "classification_type": "accumulated_snapshot_review_required",
        "confidence": 0.0,
        "evidence": {"independent_accumulated_snapshot_signal_count": profile.independent_accumulated_snapshot_signal_count, "basis": "independent_aggregate_only_fail_closed_v1"},
        "question": {"text": "Qual snapshot acumulado, saldo, período, entidade ou evento e chave foram confirmados?", "reason": "A regra não classifica, propõe, confirma ou cria tabelas, nem infere snapshot, saldo, período, calendário, entidade, evento, chave, fato, dimensão, relação, métrica ou campo.", "question_type": "confirmation", "priority": "high", "blocking": True, "options": []},
    }]
