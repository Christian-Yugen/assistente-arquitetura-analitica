# MET-DCOUNT-004 — Gate Individual de Calibração Draft 001

Autorizada por Chris exclusivamente em draft. O golden sintético produz TP=1, FP=0 e FN=0. A regra emite somente `distinct_count_conceptual_metric_candidate` com `DISTINCTCOUNT(eligible_entity)` e pergunta bloqueante. Não calcula cardinalidade, seleciona entidade ou gera DAX/M. Sensibilidade, fórmulas, classificação/grão indefinidos, fato sem grão, conflito, ambiguidade e zero/múltiplos candidatos bloqueiam. **Produção permanece bloqueada.**
