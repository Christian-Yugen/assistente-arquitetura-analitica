# MET-COMPL-001 — Especificação Lógica Proposta 001

## Estado desta especificação

Este documento descreve uma especificação **não executável**. A Proposta A foi aprovada sob `PROPOSAL-A-APPROVAL-DELEGATION-001`, mas código só pode ser criado depois de autorização explícita de Chris para implementação, testes, dataset golden sintético, manifesto, calibração e gate individual. Até então, `MET-COMPL-001` permanece fora da allowlist draft.

## Perfil privado proposto

O futuro `CompletionRateConceptProfile` deverá aceitar apenas campos agregados e booleanos, sem nomes, valores, candidatos individuais, identificadores ou posições.

| Campo proposto | Tipo | Uso |
|---|---|---|
| `row_count`, `physical_column_count` | inteiro | Cobertura estrutural mínima. |
| `status_candidate_count` | inteiro | Conta candidatos de status sem revelar a coluna. |
| `has_defined_grain`, `grain_ambiguity_count` | boolean/inteiro | Indica se o numerador/denominador pode ser discutido por unidade de grão. |
| `has_undefined_classification`, `has_fact_without_grain`, `classification_conflict_count` | boolean/inteiro | Bloqueios de classificação. |
| `has_sensitive_signal`, `has_formula_signal` | boolean | Bloqueios de privacidade e confiabilidade. |

## Lógica determinística proposta

1. Retornar lista vazia se existir sinal sensível, fórmula, classificação indefinida, fato sem grão, conflito ou ambiguidade de grão.
2. Retornar lista vazia se houver menos de 20 linhas, menos de duas colunas físicas ou quantidade de candidatos de status diferente de `1`.
3. Retornar lista vazia se não houver granularidade definida.
4. Caso contrário, emitir somente `completion_rate_conceptual_metric_candidate`, versão provisória, confiança `0.60`, severidade `review_required` e pergunta humana bloqueante sobre estados concluídos e denominador elegível.

O finding futuro não deve conter valores, nomes, cabeçalhos, posições, frequências ou fórmula DAX. A recomendação conceitual poderá registrar apenas `completed_items / eligible_items` como descrição, nunca como cálculo executado.

## Matriz de testes planejada

| Caso | Resultado esperado |
|---|---|
| Aba com 20+ linhas, duas colunas, um candidato de status e grão definido | Uma recomendação conceitual com pergunta bloqueante. |
| Zero ou múltiplos candidatos de status, cobertura insuficiente ou grão ausente/ambíguo | Nenhuma recomendação. |
| Sensibilidade, fórmula, classificação indefinida, fato sem grão ou conflito | Nenhuma recomendação. |
| Projeção contratual | Nenhum valor de status, cabeçalho, posição ou DAX na saída. |

## Saídas e bloqueios

Qualquer implementação futura exigirá testes unitários, de integração de contrato, de privacidade, golden dataset exclusivamente sintético, manifesto SHA-256, avaliador reproduzível, métricas TP/FP/FN e gate individual. Produção continua bloqueada independentemente do resultado draft.
