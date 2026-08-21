# SEM-CURR-006 — Gate de Calibração Draft 001

## Decisão

A SEM-CURR-006 está autorizada exclusivamente no perfil draft após a Proposta A e o Gate de Reconstrução 001 aprovados por Chris.

## Artefato de calibração

| Campo | Registro |
|---|---|
| Dataset golden | `GD-SEM-CURR-006-001` |
| Arquivo | `artifacts/golden/sem-curr-draft-golden-v1.json` |
| SHA-256 | `bd5bf10c8d481fe53f4167e4b415051620d213e9fa6003329dffc50dc69dcc58` |
| Avaliador | `engine/calibration/evaluate_sem_curr_draft_golden.py` |
| Resultado | 3 TP, 0 FP, 0 FN |
| Perfil de execução | `executable_draft` |

## Controles preservados

A regra aceita somente o vocabulário fechado `preco`, `preco unitario`, `preco total`, `valor monetario`, `valor financeiro`, `valor total`, `receita`, `faturamento`, `custo`, `custo total`, `despesa` e `saldo`, com ao menos dez números físicos finitos e marcador monetário explícito no formato Excel de todos esses números. Fórmulas, texto numérico, ambiguidade numérica, datas reconhecidas, formatos ausentes ou incompletos e cabeçalhos fora do vocabulário impedem a classificação. A saída é `currency_candidate`, com confiança `0.80`, evidências agregadas e pergunta humana bloqueante. O profiler reduz formatos transitórios a contagens e não expõe conteúdo, cabeçalho, marcador, posições, títulos de aba, hashes ou identificadores. A produção permanece bloqueada; qualquer ampliação exige nova proposta, aprovação, calibração e gate.
