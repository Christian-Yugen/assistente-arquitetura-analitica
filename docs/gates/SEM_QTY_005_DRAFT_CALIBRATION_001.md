# SEM-QTY-005 — Gate de Calibração Draft 001

## Decisão

A SEM-QTY-005 está autorizada exclusivamente no perfil draft após a Proposta A e o Gate de Reconstrução 001 aprovados por Chris.

## Artefato de calibração

| Campo | Registro |
|---|---|
| Dataset golden | `GD-SEM-QTY-005-001` |
| Arquivo | `artifacts/golden/sem-qty-draft-golden-v1.json` |
| SHA-256 | `b6883698fbad6bd40de5c216b9871ecd3c15ddafdc6e9cb6a7715dbdd67bf6a6` |
| Avaliador | `engine/calibration/evaluate_sem_qty_draft_golden.py` |
| Resultado | 3 TP, 0 FP, 0 FN |
| Perfil de execução | `executable_draft` |

## Controles preservados

A regra usa somente sinais privados agregados, vocabulário fechado, confiança `0.75` e pergunta humana bloqueante. Não expõe conteúdo, cabeçalho, posições, títulos de aba, hashes ou identificadores. A produção permanece bloqueada; qualquer ampliação de vocabulário, limiar ou semântica requer nova proposta, aprovação, calibração e gate.
