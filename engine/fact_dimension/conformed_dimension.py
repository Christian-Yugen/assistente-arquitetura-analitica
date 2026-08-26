from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class ConformedDimensionProfile:
    """Somente sinais independentes e agregados; nunca dimensão, chave, relação ou conteúdo de workbook."""
    independent_conformed_dimension_signal_count: int = 0
    confirmed_dimension_design_count: int = 0
    structural_conflict_count: int = 0
    sensitive_signal_count: int = 0
    contract_error_count: int = 0

def classify_conformed_dimension(profile: ConformedDimensionProfile) -> list[dict[str, object]]:
    if not (profile.independent_conformed_dimension_signal_count >= 1 and profile.confirmed_dimension_design_count == 0 and profile.structural_conflict_count == 0 and profile.sensitive_signal_count == 0 and profile.contract_error_count == 0): return []
    return [{"rule_id":"MDL-DIMCONF-005","classification_type":"conformed_dimension_review_required","confidence":0.0,"evidence":{"independent_conformed_dimension_signal_count":profile.independent_conformed_dimension_signal_count,"basis":"independent_aggregate_only_fail_closed_v1"},"question":{"text":"Qual dimensão compartilhada, entidade, chave, atributos e relações foram confirmados?","reason":"A regra não classifica, propõe, confirma ou cria dimensões, entidades, fatos, chaves, relações, cardinalidades, atributos ou campos.","question_type":"confirmation","priority":"high","blocking":True,"options":[]}}]
