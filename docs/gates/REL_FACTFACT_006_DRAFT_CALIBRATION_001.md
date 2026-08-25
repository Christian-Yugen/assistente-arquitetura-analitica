# REL-FACTFACT-006 — Gate de Calibração Draft 001

## Decisão

O gate `REL-FACTFACT-006-DRAFT-CALIBRATION-001` autoriza exclusivamente a futura promoção da `REL-FACTFACT-006@0.1.0-provisional.1` para o perfil `executable_draft`, depois da Proposta A aprovada por Chris, do gate de reconstrução, da autorização específica posterior de implementação e da evidência sintética abaixo. **Ele não autoriza produção.**

## Evidência reproduzível

| Elemento | Evidência verificada |
|---|---|
| Dataset | `GD-REL-FACTFACT-006-001`, exclusivamente sintético e sem nomes, valores, cabeçalhos, posições ou pares de origem. |
| Arquivo | `artifacts/golden/rel-factfact-draft-golden-v1.json`. |
| SHA-256 | `e39d4ebd3d4cc28aad558f95cd791ef3e1ef5685a6e57fe5b8c009ddbde9eca6`. |
| Avaliador | `engine/calibration/evaluate_rel_factfact_draft_golden.py`. |
| Resultado | 3 verdadeiros positivos, 0 falsos positivos e 0 falsos negativos. |
| Cobertura negativa | Não-fato, dimensão, classificação indefinida, fato sem grão, conflito, sensibilidade, fórmula, autorreferência, múltiplas chaves/referências, incompletude, chave de origem não única, referência de destino única, cobertura parcial/zero, direção ambígua, 1:1, N:N e ambiguidade. |

## Limites de ativação

A ativação draft poderá produzir somente `direct_fact_to_fact_relationship_review_candidate`, confiança `0.65`, severidade `review_required`, evidências agregadas e pergunta humana bloqueante. O perfil e a saída não podem revelar títulos de abas, cabeçalhos, valores, posições, pares correspondentes, frequências individuais, exemplos, chaves, identificadores ou hashes de conteúdo.

O mascaramento e a `SEM-SENS-015` continuam controles independentes: qualquer sinal sensível deve bloquear a hipótese. A regra não afirma que fatos devem ser relacionados diretamente, não cria relacionamento, dimensão compartilhada, tabela ponte, direção de filtro ou alteração de dados, modelo Power BI, Power Query ou DAX.

## Produção bloqueada

Este gate não remove os bloqueios de produção, que continuam dependentes da calibração integral do motor, dos demais ciclos governados e do Gate MVP 1.0 produtivo; **a produção permanece bloqueada**. A REL-FACTFACT-006 permanece uma experiência controlada em draft com confirmação humana obrigatória.
