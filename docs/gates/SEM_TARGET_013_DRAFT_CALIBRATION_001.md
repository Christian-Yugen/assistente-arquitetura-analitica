# SEM-TARGET-013 — Gate de Calibração Draft 001

## Decisão

A SEM-TARGET-013 está autorizada exclusivamente no perfil draft após a Proposta A e o Gate de Reconstrução 001 aprovados por Chris.

## Artefato de calibração

| Campo | Registro |
|---|---|
| Dataset golden | `GD-SEM-TARGET-013-001` |
| Arquivo | `artifacts/golden/sem-target-draft-golden-v1.json` |
| SHA-256 | `a11f20b9c875504db0c9746161b346e42757d4e24a3c8f290f934af8da121279` |
| Avaliador | `engine/calibration/evaluate_sem_target_draft_golden.py` |
| Resultado | 3 TP, 0 FP, 0 FN |
| Perfil de execução | `executable_draft` |

## Controles preservados

A regra aceita somente o vocabulário fechado `meta`, `previsto`, `previsao`, `orcado`, `orcamento`, `forecast`, `target`, `budget` e `planejado`, com ao menos dez números físicos finitos. Fórmulas, texto numérico, ambiguidade numérica, datas reconhecidas, tipos físicos não numéricos e cabeçalhos fora do vocabulário impedem a classificação. A saída é `target_or_forecast_candidate`, com confiança `0.75`, evidências agregadas e pergunta humana bloqueante. O profiler não expõe conteúdo, cabeçalho, fórmulas, posições, títulos de aba, períodos, hashes ou identificadores. A produção permanece bloqueada; qualquer ampliação exige nova proposta, aprovação, calibração e gate.
