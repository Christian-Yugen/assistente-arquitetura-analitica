# REL-AMBIG-007 — Especificação Lógica Proposta 001

## Estado desta especificação

Este documento descreve uma especificação **não executável**. Ele só pode orientar código depois de Proposta A aprovada por Chris, gate de reconstrução, autorização explícita de implementação, testes, dataset golden sintético, manifesto, calibração e gate individual. Até então, `REL-AMBIG-007` permanece fora da allowlist draft.

## Perfil privado proposto

O futuro `AmbiguousRelationshipPathPairProfile` deverá aceitar apenas campos agregados e booleanos. IDs opacos transitórios podem existir exclusivamente antes da materialização do perfil para permitir a agregação; devem ser descartados antes de qualquer retorno, contrato, finding, persistência, evidência ou log.

| Campo proposto | Tipo | Uso |
|---|---|---|
| `source_standard_dimension_candidate` | boolean | Indica dimensão padrão já classificada na origem. |
| `target_fact_candidate` | boolean | Indica fato transacional ou periódico já classificado no destino. |
| `source_or_target_calendar_dimension_candidate`, `source_or_target_undefined_candidate`, `source_or_target_fact_without_grain_candidate`, `source_or_target_classification_conflict` | boolean | Classificações incompatíveis que bloqueiam. |
| `source_or_target_sensitive`, `source_or_target_has_formula`, `self_reference` | boolean | Bloqueios de privacidade e estrutura. |
| `eligible_source_key_count`, `eligible_target_reference_count`, `eligible_direction_count` | inteiro | Contagens agregadas sem identificar colunas ou abas. |
| `source_key_complete`, `source_key_unique`, `target_reference_complete`, `target_reference_unique`, `referential_coverage_ratio` | boolean/decimal | Elegibilidade e cobertura agregadas. |
| `has_one_to_one_pattern`, `has_many_to_many_pattern`, `ambiguity_count` | boolean/inteiro | Padrões incompatíveis e conflito de classificação. |

## Lógica determinística proposta

1. Retornar lista vazia se qualquer bloqueio estiver verdadeiro.
2. Retornar lista vazia se a origem não for dimensão padrão ou o destino não for fato transacional/periódico.
3. Retornar lista vazia se não houver pelo menos uma chave de origem e uma referência de destino elegíveis, completas e com unicidade compatível.
4. Retornar lista vazia se a cobertura não for exatamente `1.0` ou a quantidade de direções elegíveis for menor que `2`.
5. Caso contrário, emitir somente `ambiguous_relationship_path_review_candidate`, versão provisória, confiança `0.60`, severidade `review_required` e pergunta humana bloqueante.

O finding futuro não deve identificar abas, colunas, valores, posições, correspondências, frequências ou exemplo de chave. Ele não deve afirmar que há caminho ambíguo em Power BI, nem criar relação, direção de filtro ou artefato de Power BI.

## Matriz de testes planejada

| Caso | Resultado esperado |
|---|---|
| Dimensão padrão e fato compatíveis, cobertura integral e duas direções candidatas agregadas | Uma hipótese de revisão com pergunta bloqueante. |
| Uma única direção, cobertura parcial/zero ou ausência de chave/referência elegível | Nenhuma hipótese. |
| Fórmula, sensibilidade, autorreferência, 1:1, N:N, calendário, fato sem grão, classificação indefinida, conflito ou ambiguidade de classificação | Nenhuma hipótese. |
| Projeção contratual | Nenhum campo identificável no fragmento de relacionamento. |

## Saídas e bloqueios

Qualquer implementação futura exigirá testes unitários, de integração de contrato, de privacidade, golden dataset exclusivamente sintético, manifesto SHA-256, avaliador reproduzível, métricas TP/FP/FN e gate individual. Produção continua bloqueada independentemente do resultado draft.
