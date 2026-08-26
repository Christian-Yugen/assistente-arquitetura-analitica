from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class DuplicateGrainProfile:
    """Somente sinais independentes e agregados; nunca linhas, chaves ou conteúdo de workbook."""
    independent_duplicate_grain_signal_count: int = 0
    confirmed_duplicate_resolution_count: int = 0
    structural_conflict_count: int = 0
    sensitive_signal_count: int = 0
    contract_error_count: int = 0

def classify_duplicate_grain(profile: DuplicateGrainProfile) -> dict[str, object] | None:
    if not (profile.independent_duplicate_grain_signal_count >= 1 and profile.confirmed_duplicate_resolution_count == 0 and profile.structural_conflict_count == 0 and profile.sensitive_signal_count == 0 and profile.contract_error_count == 0): return None
    return {"rule_id":"GRN-DUP-010","category":"grain","severity":"high","title":"Possível duplicidade na granularidade exige revisão","description":"Um sinal agregado e independente exige confirmação humana antes de tratar a granularidade como sem duplicidade.","evidence":[{"code":"EVD-GRN-DUP-INDEPENDENT-SIGNAL","effect":"duplicate_grain_review_required","observed_value":profile.independent_duplicate_grain_signal_count,"expected_condition":"at least one independently produced aggregated duplicate-grain signal without confirmation or blocking conflict"}],"impact":"A estrutura não deve orientar a modelagem até confirmação humana.","recommendation":"Confirmar entidade ou evento, nível de detalhe, chave e tratamento de duplicidade antes da modelagem.","question":{"text":"Qual entidade ou evento, nível de detalhe, chave e tratamento de duplicidade foram confirmados?","reason":"A regra não identifica, localiza, seleciona ou corrige linhas, chaves, entidades, eventos, fatos, dimensões, relações, cardinalidades ou campos.","question_type":"single_choice","priority":"high","blocking":True,"options":[{"option_id":"confirm_duplicate_treatment","label":"Informar tratamento de duplicidade confirmado"},{"option_id":"defer_modeling","label":"Adiar modelagem até revisão"}],"affected_modules":["grain","modeling"]}}
