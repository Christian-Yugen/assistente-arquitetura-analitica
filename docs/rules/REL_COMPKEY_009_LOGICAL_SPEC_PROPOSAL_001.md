# REL-COMPKEY-009 — Especificação Lógica Proposta 001

## Estado desta especificação

Este documento descreve uma especificação **não executável**. A Proposta A foi aprovada sob `PROPOSAL-A-APPROVAL-DELEGATION-001`, mas código só pode ser criado depois de autorização explícita de Chris para implementação, testes, dataset golden sintético, manifesto, calibração e gate individual. Até então, `REL-COMPKEY-009` permanece fora da allowlist draft.

## Perfil privado proposto

O futuro `CompositeRelationshipKeyPairProfile` deverá aceitar apenas campos agregados e booleanos. Um profiler auxiliar poderá manipular assinaturas transitórias de tuplas de dois campos apenas em memória para derivar contagens e cobertura; essas assinaturas devem ser descartadas antes de materializar o perfil.

| Campo proposto | Tipo | Uso |
|---|---|---|
| `source_standard_dimension_candidate`, `target_fact_candidate` | boolean | Compatibilidade de classificação da relação candidata. |
| `source_calendar_dimension_candidate`, `source_or_target_undefined_candidate`, `source_or_target_fact_without_grain_candidate`, `source_or_target_classification_conflict` | boolean | Classificações incompatíveis que bloqueiam. |
| `source_or_target_sensitive`, `source_or_target_has_formula`, `self_reference` | boolean | Bloqueios de privacidade e estrutura. |
| `eligible_composite_key_pair_count`, `eligible_composite_reference_pair_count`, `eligible_direction_count` | inteiro | Contagens agregadas de pares de campos sem identificá-los. |
| `has_eligible_simple_key`, `composite_key_complete`, `composite_key_unique`, `composite_reference_complete`, `composite_reference_unique`, `referential_coverage_ratio` | boolean/decimal | Elegibilidade e cobertura agregadas. |
| `has_one_to_one_pattern`, `has_many_to_many_pattern`, `ambiguity_count` | boolean/inteiro | Padrões incompatíveis e conflito de classificação. |

## Lógica determinística proposta

1. Retornar lista vazia se qualquer bloqueio estiver verdadeiro.
2. Retornar lista vazia se a origem não for dimensão padrão ou o destino não for fato transacional/periódico.
3. Retornar lista vazia se existir chave simples elegível, se a quantidade de pares compostos de chave/referência não for exatamente `1`, se a chave composta não for completa/única ou se a referência composta não for completa/não única.
4. Retornar lista vazia se a cobertura não for exatamente `1.0` ou a quantidade de direções elegíveis não for exatamente `1`.
5. Caso contrário, emitir somente `composite_relationship_key_review_candidate`, versão provisória, confiança `0.70`, severidade `review_required` e pergunta humana bloqueante.

O finding futuro não deve identificar abas, colunas, valores, posições, correspondências, frequências, tuplas ou exemplo de chave. Ele não deve criar colunas concatenadas, relação, filtro ou artefato Power BI.

## Matriz de testes planejada

| Caso | Resultado esperado |
|---|---|
| Dimensão e fato compatíveis, uma composição de dois campos única/completa, referência composta completa/não única e cobertura integral | Uma hipótese de revisão com pergunta bloqueante. |
| Chave simples elegível, zero/múltiplas composições, cobertura parcial/zero ou direção ambígua | Nenhuma hipótese. |
| Fórmula, sensibilidade, autorreferência, 1:1, N:N, calendário, fato sem grão, classificação indefinida, conflito ou ambiguidade | Nenhuma hipótese. |
| Perfil e projeção contratual | Nenhum campo identificável, tupla ou assinatura no fragmento de relacionamento. |

## Saídas e bloqueios

Qualquer implementação futura exigirá testes unitários, de integração de contrato, de privacidade, golden dataset exclusivamente sintético, manifesto SHA-256, avaliador reproduzível, métricas TP/FP/FN e gate individual. Produção continua bloqueada independentemente do resultado draft.
