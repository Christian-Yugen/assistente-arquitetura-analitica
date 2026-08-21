# SEM-ACTUAL-014 — Gate de Calibração Draft 001

## Decisão

A SEM-ACTUAL-014 está autorizada exclusivamente no perfil draft após a Proposta A e o Gate de Reconstrução 001 aprovados por Chris.

## Artefato de calibração

| Campo | Registro |
|---|---|
| Dataset golden | `GD-SEM-ACTUAL-014-001` |
| Arquivo | `artifacts/golden/sem-actual-draft-golden-v1.json` |
| SHA-256 | `1850eee856e24195c716665095ca64ee3d6ae080b762a7be6ad6032601a1a702` |
| Avaliador | `engine/calibration/evaluate_sem_actual_draft_golden.py` |
| Resultado | 3 TP, 0 FP, 0 FN |
| Perfil de execução | `executable_draft` |

## Controles preservados

A regra aceita somente o vocabulário fechado `realizado`, `valor realizado`, `realizado total`, `executado`, `valor executado`, `observado` e `actual`, com ao menos dez números físicos finitos. Fórmulas, texto numérico, ambiguidade numérica, datas reconhecidas, tipos físicos não numéricos e cabeçalhos fora do vocabulário impedem a classificação. A saída é `actual_candidate`, com confiança `0.75`, evidências agregadas e pergunta humana bloqueante. O profiler não expõe conteúdo, cabeçalho, fórmulas, posições, títulos de aba, períodos, hashes ou identificadores. A produção permanece bloqueada; qualquer ampliação exige nova proposta, aprovação, calibração e gate.
