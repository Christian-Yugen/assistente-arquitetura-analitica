# SEM-COMP-002 — Gate de Calibração Draft 001

## Decisão

A SEM-COMP-002 está autorizada exclusivamente no perfil draft após a Proposta A e o Gate de Reconstrução 001 aprovados por Chris. A autorização não promove a regra para produção nem altera a SEM-DATE-001.

## Artefato de calibração

| Campo | Registro |
|---|---|
| Dataset golden | `GD-SEM-COMP-002-001` |
| Arquivo | `artifacts/golden/sem-comp-draft-golden-v1.json` |
| SHA-256 | `2037d2757f688b6674d99c77f7aa398b615b126d7966e4d6b937b35030f90523` |
| Avaliador | `engine/calibration/evaluate_sem_comp_draft_golden.py` |
| Resultado | 3 TP, 0 FP, 0 FN |
| Perfil de execução | `executable_draft` |

## Controles preservados

A regra exige apenas o vocabulário fechado `competencia`, `data competencia` e `data de competencia`, ao menos dez observações não ausentes, reconhecimento integral pela SEM-DATE-001 e ausência de fórmulas. Datas parciais, datas inválidas, serial Excel, timestamps, formatos não reconhecidos e cabeçalhos fora do vocabulário bloqueiam a classificação.

A saída é `competence_date_candidate`, com confiança `0.85`, evidências agregadas e pergunta humana bloqueante. O profiler não expõe valores, cabeçalhos, fórmulas, posições, títulos de aba, períodos, hashes ou identificadores. A classificação coexiste com `date_generic` e não infere o significado contábil, fiscal, trabalhista ou operacional do período. Produção permanece bloqueada; qualquer ampliação exige nova proposta, aprovação, calibração e gate.
