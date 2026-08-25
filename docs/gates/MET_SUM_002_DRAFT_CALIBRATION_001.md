# MET-SUM-002 — Gate Individual de Calibração Draft 001

O gate `MET-SUM-002-DRAFT-CALIBRATION-001` autoriza somente a execução controlada da regra no perfil **draft**, após a autorização explícita de Chris.

| Controle | Estado |
|---|---|
| Perfil e saída | Agregados; somente `sum_conceptual_metric_candidate`. |
| Calibração sintética | TP=1, FP=0, FN=0. |
| Proibição | Não escolhe medida/unidade, não soma valores e não gera DAX ou M. |
| Confirmação humana | Pergunta bloqueante sobre medida, unidade e filtros. |
| Produção | Bloqueada. |

Sensibilidade, fórmulas, classificação/grão indefinidos, fato sem grão, conflito, ambiguidade e zero/múltiplos candidatos quantidade/moeda impedem a hipótese. A regra não expõe valores, cabeçalhos, posições, IDs de coluna ou exemplos.
