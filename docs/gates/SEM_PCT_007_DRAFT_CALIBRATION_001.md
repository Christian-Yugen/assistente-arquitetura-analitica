# SEM-PCT-007 — Gate de Calibração Draft 001

## Decisão

A SEM-PCT-007 está autorizada exclusivamente no perfil draft após a Proposta A e o Gate de Reconstrução 001 aprovados por Chris.

## Artefato de calibração

| Campo | Registro |
|---|---|
| Dataset golden | `GD-SEM-PCT-007-001` |
| Arquivo | `artifacts/golden/sem-pct-draft-golden-v1.json` |
| SHA-256 | `8c7f49281bfa7b01a286e5ccb1d1065b05d3808049e7a914aee79f64ced29b1f` |
| Avaliador | `engine/calibration/evaluate_sem_pct_draft_golden.py` |
| Resultado | 3 TP, 0 FP, 0 FN |
| Perfil de execução | `executable_draft` |

## Controles preservados

A regra aceita somente os cabeçalhos fechados `percentual`, `percentagem`, `pct` e `%`, com ao menos dez números físicos finitos integralmente no intervalo `[0,1]`. Fórmulas, texto numérico, ambiguidade numérica e datas reconhecidas impedem a classificação. A saída é `percentage_candidate`, com confiança `0.75`, evidências agregadas e pergunta humana bloqueante. Não expõe conteúdo, cabeçalho, posições, títulos de aba, hashes ou identificadores. A produção permanece bloqueada; qualquer ampliação de vocabulário, intervalo, limiar ou semântica requer nova proposta, aprovação, calibração e gate.
