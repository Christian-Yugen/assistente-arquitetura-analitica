"""MET-DCOUNT-004: recomendação conceitual privada de contagem distinta."""
from __future__ import annotations
from dataclasses import dataclass
@dataclass(frozen=True)
class DistinctCountConceptProfile:
    row_count:int=0; physical_column_count:int=0; entity_candidate_count:int=0; has_defined_grain:bool=False; grain_ambiguity_count:int=0; has_undefined_classification:bool=False; has_fact_without_grain:bool=False; classification_conflict_count:int=0; has_sensitive_signal:bool=False; has_formula_signal:bool=False
def classify_distinct_count_concept(profile:DistinctCountConceptProfile)->dict[str,object]|None:
    blocked=profile.has_sensitive_signal or profile.has_formula_signal or profile.has_undefined_classification or profile.has_fact_without_grain or profile.classification_conflict_count>0 or profile.grain_ambiguity_count>0
    if blocked or not(profile.row_count>=20 and profile.physical_column_count>=2 and profile.entity_candidate_count==1 and profile.has_defined_grain): return None
    return {"rule_id":"MET-DCOUNT-004","metric_type":"distinct_count_conceptual_metric_candidate","confidence":0.60,"severity":"review_required","conceptual_formula":"DISTINCTCOUNT(eligible_entity)","evidence":{"row_count":profile.row_count,"physical_column_count":profile.physical_column_count,"entity_candidate_count":1,"has_defined_grain":True},"question":{"text":"Qual entidade distinta deve ser contada e quais filtros se aplicam?","reason":"A regra não calcula cardinalidade, não seleciona entidade e não gera DAX ou Power Query.","question_type":"single_choice","priority":"high","blocking":True,"options":["Definir entidade e filtros","Não recomendar esta métrica","Revisar a granularidade antes"]}}
