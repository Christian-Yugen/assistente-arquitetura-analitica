# MET-SUM-002 — Especificação Lógica Proposta 001

Esta especificação é **não executável** até autorização específica de Chris, testes, golden sintético, manifesto, calibração e gate individual.

| Campo privado proposto | Tipo | Uso |
|---|---|---|
| `row_count`, `physical_column_count` | inteiro | Cobertura estrutural. |
| `summable_candidate_count` | inteiro | Conta candidatos quantidade/moeda sem revelar a coluna. |
| `has_defined_grain`, `grain_ambiguity_count` | boolean/inteiro | Elegibilidade por grão. |
| `has_sensitive_signal`, `has_formula_signal`, `has_undefined_classification`, `has_fact_without_grain`, `classification_conflict_count` | boolean/inteiro | Bloqueios. |

A regra futura retorna vazio diante de qualquer bloqueio, de menos de 20 linhas/duas colunas, de candidato somável diferente de um ou de grão ausente. Caso contrário, emite somente `sum_conceptual_metric_candidate`, confiança `0.60`, severidade `review_required`, fórmula conceitual `SUM(eligible_measure)` e pergunta bloqueante. A saída não contém valores, nomes, cabeçalhos, posições, unidade ou DAX.
