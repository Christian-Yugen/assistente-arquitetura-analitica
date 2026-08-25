"""MET-RATE-007: recomendação conceitual privada para taxa."""
from __future__ import annotations
from dataclasses import dataclass
@dataclass(frozen=True)
class RateConceptProfile:
    row_count:int=0; physical_column_count:int=0; numerator_candidate_count:int=0; denominator_candidate_count:int=0; has_defined_grain:bool=False; grain_ambiguity_count:int=0; has_undefined_classification:bool=False; has_fact_without_grain:bool=False; classification_conflict_count:int=0; has_sensitive_signal:bool=False; has_formula_signal:bool=False
def classify_rate_concept(profile:RateConceptProfile)->dict[str,object]|None:
    blocked=profile.has_sensitive_signal or profile.has_formula_signal or profile.has_undefined_classification or profile.has_fact_without_grain or profile.classification_conflict_count>0 or profile.grain_ambiguity_count>0
    if blocked or not(profile.row_count>=20 and profile.physical_column_count>=2 and profile.numerator_candidate_count==1 and profile.denominator_candidate_count==1 and profile.has_defined_grain): return None
    return {"rule_id":"MET-RATE-007","metric_type":"rate_conceptual_metric_candidate","confidence":0.60,"severity":"review_required","conceptual_formula":"eligible_numerator / eligible_denominator","evidence":{"row_count":profile.row_count,"physical_column_count":profile.physical_column_count,"numerator_candidate_count":1,"denominator_candidate_count":1,"has_defined_grain":True},"question":{"text":"Qual numerador e denominador devem definir a taxa, em qual unidade, população e filtros?","reason":"A regra não calcula taxa, não seleciona campos e não gera DAX ou Power Query.","question_type":"single_choice","priority":"high","blocking":True,"options":["Definir numerador, denominador, unidade, população e filtros","Não recomendar esta métrica","Revisar a granularidade antes"]}}
