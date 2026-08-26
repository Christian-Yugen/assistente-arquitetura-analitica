from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class InconsistentGrainProfile:
    """Somente sinais independentes e agregados; nunca granularidade ou conteúdo de workbook."""
    independent_inconsistent_grain_signal_count: int = 0
    confirmed_grain_count: int = 0
    structural_conflict_count: int = 0
    sensitive_signal_count: int = 0
    contract_error_count: int = 0

def classify_inconsistent_grain(profile: InconsistentGrainProfile) -> dict[str, object] | None:
    if not (profile.independent_inconsistent_grain_signal_count >= 1 and profile.confirmed_grain_count == 0 and profile.structural_conflict_count == 0 and profile.sensitive_signal_count == 0 and profile.contract_error_count == 0):
        return None
    return {"rule_id":"GRN-INCONS-009","category":"grain","severity":"high","title":"Possível granularidade inconsistente exige revisão","description":"Um sinal agregado e independente exige confirmação humana antes de tratar a granularidade como consistente.","evidence":[{"code":"EVD-GRN-INCONS-INDEPENDENT-SIGNAL","effect":"inconsistent_grain_review_required","observed_value":profile.independent_inconsistent_grain_signal_count,"expected_condition":"at least one independently produced aggregated inconsistent-grain signal without confirmation or blocking conflict"}],"impact":"A estrutura não deve orientar a modelagem até confirmação humana.","recommendation":"Confirmar entidade ou evento, nível de detalhe, período e chave antes da modelagem.","question":{"text":"Qual entidade ou evento, nível de detalhe, período e chave foram confirmados para esta estrutura?","reason":"A regra não infere, valida, determina, combina ou corrige granularidades, entidades, eventos, chaves, fatos, dimensões, relações, cardinalidades ou campos.","question_type":"single_choice","priority":"high","blocking":True,"options":[{"option_id":"confirm_grain","label":"Informar granularidade confirmada"},{"option_id":"defer_modeling","label":"Adiar modelagem até revisão"}],"affected_modules":["grain","modeling"]}}
