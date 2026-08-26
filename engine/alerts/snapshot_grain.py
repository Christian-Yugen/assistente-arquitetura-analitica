"""GRN-SNAP-006: hipótese de snapshot somente com sinal independente agregado."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class SnapshotGrainProfile:
    independent_snapshot_signal_count: int = 0
    confirmed_snapshot_grain_count: int = 0
    structural_conflict_count: int = 0
    sensitive_signal_count: int = 0
    contract_error_count: int = 0


def classify_snapshot_grain(profile: SnapshotGrainProfile) -> dict[str, object] | None:
    if not (profile.independent_snapshot_signal_count >= 1 and profile.confirmed_snapshot_grain_count == 0 and profile.structural_conflict_count == 0 and profile.sensitive_signal_count == 0 and profile.contract_error_count == 0):
        return None
    return {"rule_id": "GRN-SNAP-006", "category": "grain", "severity": "high", "title": "Possível snapshot exige revisão", "description": "Um sinal agregado e independente exige confirmação humana antes de tratar a estrutura como snapshot.", "evidence": [{"code": "EVD-GRN-SNAP-INDEPENDENT-SIGNAL", "effect": "snapshot_grain_review_required", "observed_value": profile.independent_snapshot_signal_count, "expected_condition": "at least one independently produced aggregated snapshot signal without confirmation or blocking conflict"}], "impact": "A estrutura não deve orientar a modelagem até confirmação humana.", "recommendation": "Confirmar periodicidade, referência temporal, entidade ou evento e chave antes da modelagem.", "question": {"text": "Qual periodicidade, referência temporal, entidade ou evento e chave foram confirmados para esta estrutura?", "reason": "A regra não infere período, calendário, entidade, evento, chave, fato, dimensão, relação, medida ou campo.", "question_type": "single_choice", "priority": "high", "blocking": True, "options": [{"option_id": "confirm_snapshot", "label": "Informar snapshot confirmado"}, {"option_id": "defer_modeling", "label": "Adiar modelagem até revisão"}], "affected_modules": ["grain", "modeling"]}}
