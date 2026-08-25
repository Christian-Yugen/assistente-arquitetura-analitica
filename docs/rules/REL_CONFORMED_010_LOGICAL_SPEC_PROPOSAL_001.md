# REL-CONFORMED-010 — Especificação Lógica Proposta 001

## Estado desta especificação

Este documento descreve uma especificação **não executável**. A Proposta A foi aprovada sob `PROPOSAL-A-APPROVAL-DELEGATION-001`, mas código só pode ser criado depois de autorização explícita de Chris para implementação, testes, dataset golden sintético, manifesto, calibração e gate individual. Até então, `REL-CONFORMED-010` permanece fora da allowlist draft.

## Perfil privado proposto

O futuro `ConformedDimensionPairProfile` deverá aceitar somente flags e métricas agregadas. A contagem de fatos conectados será calculada a partir de IDs opacos transitórios e descartará a lista desses IDs antes de materializar o perfil, retornar o finding, persistir evidência ou gerar log.

| Campo proposto | Tipo | Uso |
|---|---|---|
| `source_standard_dimension_candidate`, `target_fact_candidate` | boolean | Compatibilidade de classificação do par em revisão. |
| `source_calendar_dimension_candidate`, `source_or_target_undefined_candidate`, `source_or_target_fact_without_grain_candidate`, `source_or_target_classification_conflict` | boolean | Classificações incompatíveis que bloqueiam. |
| `source_or_target_sensitive`, `source_or_target_has_formula`, `self_reference` | boolean | Bloqueios de privacidade e estrutura. |
| `eligible_dimension_key_count`, `eligible_fact_reference_count`, `eligible_direction_count` | inteiro | Elegibilidade do par sem identificar colunas ou abas. |
| `dimension_key_complete`, `dimension_key_unique`, `fact_reference_complete`, `fact_reference_unique`, `referential_coverage_ratio` | boolean/decimal | Cobertura agregada do par. |
| `connected_fact_count` | inteiro | Número agregado de fatos candidatos ligados à dimensão, sem lista de fatos. |
| `has_one_to_one_pattern`, `has_many_to_many_pattern`, `ambiguity_count` | boolean/inteiro | Padrões incompatíveis e conflito de classificação. |

## Lógica determinística proposta

1. Retornar lista vazia se qualquer bloqueio estiver verdadeiro.
2. Retornar lista vazia se a origem não for dimensão padrão ou o destino não for fato transacional/periódico.
3. Retornar lista vazia se a contagem de chave de dimensão ou referência de fato não for exatamente `1`, se a chave não for única/completa ou se a referência não for completa/não única.
4. Retornar lista vazia se a cobertura não for exatamente `1.0`, a quantidade de direções não for exatamente `1` ou `connected_fact_count` for menor que `2`.
5. Caso contrário, emitir somente `conformed_dimension_review_candidate`, versão provisória, confiança `0.75`, severidade `review_required` e pergunta humana bloqueante.

O finding futuro não deve identificar abas, colunas, valores, posições, correspondências, frequências, chaves ou os fatos conectados. Ele não deve criar dimensão, relação, filtro ou artefato Power BI.

## Matriz de testes planejada

| Caso | Resultado esperado |
|---|---|
| Dimensão padrão e fato compatíveis, cardinalidade 1:N, cobertura integral, direção única e dois fatos agregados | Uma hipótese de revisão com pergunta bloqueante. |
| Um único fato conectado, cobertura parcial/zero, direção zero/ambígua ou chave/referência não elegível | Nenhuma hipótese. |
| Fórmula, sensibilidade, autorreferência, 1:1, N:N, calendário, fato sem grão, classificação indefinida, conflito ou ambiguidade | Nenhuma hipótese. |
| Projeção contratual | Nenhum campo identificável ou lista de fatos no fragmento de relacionamento. |

## Saídas e bloqueios

Qualquer implementação futura exigirá testes unitários, de integração de contrato, de privacidade, golden dataset exclusivamente sintético, manifesto SHA-256, avaliador reproduzível, métricas TP/FP/FN e gate individual. Produção continua bloqueada independentemente do resultado draft.
