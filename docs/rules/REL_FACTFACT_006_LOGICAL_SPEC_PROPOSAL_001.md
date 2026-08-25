# REL-FACTFACT-006 — Especificação Lógica Proposta 001

## Estado desta especificação

Este documento descreve uma especificação **não executável**. Ele só pode orientar código depois de Proposta A aprovada por Chris, gate de reconstrução, autorização explícita de implementação, testes, dataset golden sintético, manifesto, calibração e gate individual. Até então, `REL-FACTFACT-006` permanece fora da allowlist draft.

## Perfil privado proposto

O futuro `DirectFactRelationshipPairProfile` deverá aceitar apenas campos agregados e booleanos. IDs opacos transitórios podem existir exclusivamente antes da materialização do perfil para permitir a agregação; devem ser descartados antes de qualquer retorno, contrato, finding, persistência, evidência ou log.

| Campo proposto | Tipo | Uso |
|---|---|---|
| `source_fact_candidate` | boolean | Indica fato transacional ou periódico já classificado no lado de origem. |
| `target_fact_candidate` | boolean | Indica fato transacional ou periódico já classificado no lado de destino. |
| `eligible_source_key_count` | inteiro | Conta chaves físicas completas e únicas elegíveis no lado de origem. |
| `eligible_target_reference_count` | inteiro | Conta referências físicas completas e não únicas elegíveis no lado de destino. |
| `source_key_complete` | boolean | Informa completude da chave de origem. |
| `target_reference_complete` | boolean | Informa completude da referência de destino. |
| `referential_coverage_ratio` | decimal | Cobertura referencial agregada no intervalo de zero a um. |
| `eligible_direction_count` | inteiro | Conta direções candidatas sem identificar colunas ou abas. |
| `has_formula_signal`, `has_sensitive_signal`, `has_conflict`, `has_ambiguity` | boolean | Bloqueios independentes. |
| `has_one_to_one_pattern`, `has_many_to_many_pattern`, `has_self_reference` | boolean | Padrões incompatíveis que bloqueiam. |
| `has_calendar_dimension`, `has_undefined_classification`, `has_fact_without_grain` | boolean | Classificações incompatíveis que bloqueiam. |

## Lógica determinística proposta

1. Retornar lista vazia se qualquer bloqueio estiver verdadeiro.
2. Retornar lista vazia se uma das abas não for fato transacional ou periódico.
3. Retornar lista vazia se a contagem de chave de origem não for exatamente `1`, se a chave não for completa, se a contagem de referência de destino não for exatamente `1` ou se a referência não for completa.
4. Retornar lista vazia se a cobertura não for exatamente `1.0` ou se a quantidade de direções não for exatamente `1`.
5. Caso contrário, emitir somente `direct_fact_to_fact_relationship_review_candidate`, versão provisória, confiança `0.65`, severidade `review_required` e pergunta humana bloqueante.

O finding futuro não deve identificar abas, colunas, valores, posições, correspondências, frequências ou exemplo de chave. Ele não deve concluir que fatos devem ser relacionados diretamente, nem criar artefatos de Power BI.

## Matriz de testes planejada

| Caso | Resultado esperado |
|---|---|
| Dois fatos compatíveis, chave única/completa, referência não única/completa, cobertura integral e direção única | Uma hipótese de revisão com pergunta bloqueante. |
| Cobertura parcial, zero ou direção ambígua | Nenhuma hipótese. |
| Fórmula, sensibilidade, conflito, ambiguidade, autorreferência, 1:1 ou muitos-para-muitos | Nenhuma hipótese. |
| Dimensão, calendário, fato sem grão ou classificação indefinida | Nenhuma hipótese. |
| Projeção contratual | Nenhum campo identificável no fragmento de relacionamento. |

## Saídas e bloqueios

Qualquer implementação futura exigirá testes unitários, de integração de contrato, de privacidade, golden dataset exclusivamente sintético, manifesto SHA-256, avaliador reprodutível, métricas TP/FP/FN e gate individual. Produção continua bloqueada independentemente do resultado draft.
