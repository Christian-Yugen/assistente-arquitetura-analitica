# REL-CONFORMED-010 — Gate de Calibração Draft 001

## Decisão

O gate `REL-CONFORMED-010-DRAFT-CALIBRATION-001` autoriza exclusivamente a futura promoção da `REL-CONFORMED-010@0.1.0-provisional.1` para o perfil `executable_draft`, depois da Proposta A aprovada sob a diretriz de Chris, do gate de reconstrução, da autorização específica posterior de implementação e da evidência sintética abaixo. **Ele não autoriza produção.**

## Evidência reproduzível

| Elemento | Evidência verificada |
|---|---|
| Dataset | `GD-REL-CONFORMED-010-001`, exclusivamente sintético e sem nomes, valores, cabeçalhos, posições, pares ou lista de fatos conectados. |
| Arquivo | `artifacts/golden/rel-conformed-draft-golden-v1.json`. |
| SHA-256 | `716c20ca0e5760a80e83e2859b09cfe9702305c743d6ada05611de51841cc851`. |
| Avaliador | `engine/calibration/evaluate_rel_conformed_draft_golden.py`. |
| Resultado | 3 verdadeiros positivos, 0 falsos positivos e 0 falsos negativos. |
| Cobertura negativa | Não-dimensão, não-fato, calendário, classificação indefinida, fato sem grão, conflito, sensibilidade, fórmula, autorreferência, chaves/referências não elegíveis, incompletude, cobertura parcial/zero, direção ambígua, um único fato conectado, 1:1, N:N e ambiguidade. |

## Limites de ativação

A ativação draft poderá produzir somente `conformed_dimension_review_candidate`, confiança `0.75`, severidade `review_required`, evidências agregadas e pergunta humana bloqueante. O perfil e a saída não podem revelar títulos de abas, cabeçalhos, valores, posições, pares correspondentes, frequências individuais, exemplos, chaves, identificadores ou lista de fatos conectados.

O mascaramento e a `SEM-SENS-015` continuam controles independentes: qualquer sinal sensível deve bloquear a hipótese. A regra não confirma conformidade, não cria dimensão compartilhada, relacionamento, filtro, alteração de dados, modelo Power BI, Power Query ou DAX.

## Produção bloqueada

Este gate não remove os bloqueios de produção, que continuam dependentes da calibração integral do motor, dos demais ciclos governados e do Gate MVP 1.0 produtivo; **a produção permanece bloqueada**. A REL-CONFORMED-010 permanece uma experiência controlada em draft com confirmação humana obrigatória.
