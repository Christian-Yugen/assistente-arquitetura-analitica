# REL-BIDIR-008 — Gate de Calibração Draft 001

## Decisão

O gate `REL-BIDIR-008-DRAFT-CALIBRATION-001` autoriza exclusivamente a futura promoção da `REL-BIDIR-008@0.1.0-provisional.1` para o perfil `executable_draft`, depois da Proposta A aprovada sob a diretriz de Chris, do gate de reconstrução, da autorização específica posterior de implementação e da evidência sintética abaixo. **Ele não autoriza produção.**

## Evidência reproduzível

| Elemento | Evidência verificada |
|---|---|
| Dataset | `GD-REL-BIDIR-008-001`, exclusivamente sintético e sem nomes, valores, cabeçalhos, posições ou pares de origem. |
| Arquivo | `artifacts/golden/rel-bidir-draft-golden-v1.json`. |
| SHA-256 | `372d5dad4caafbd7a4f2ad21429a3c96892bf24f62e57c86220b18dca52ecdc9`. |
| Avaliador | `engine/calibration/evaluate_rel_bidir_draft_golden.py`. |
| Resultado | 3 verdadeiros positivos, 0 falsos positivos e 0 falsos negativos. |
| Cobertura negativa | Não-dimensão, não-fato, calendário, classificação indefinida, fato sem grão, conflito, sensibilidade, fórmula, autorreferência, múltiplas chaves/referências, incompletude, chave de dimensão não única, referência de fato única, cobertura parcial/zero, direção ambígua, 1:1, N:N e ambiguidade. |

## Limites de ativação

A ativação draft poderá produzir somente `bidirectional_filter_review_candidate`, confiança `0.70`, severidade `review_required`, evidências agregadas e pergunta humana bloqueante. O perfil e a saída não podem revelar títulos de abas, cabeçalhos, valores, posições, pares correspondentes, frequências individuais, exemplos, chaves, identificadores ou hashes de conteúdo.

O mascaramento e a `SEM-SENS-015` continuam controles independentes: qualquer sinal sensível deve bloquear a hipótese. A regra não detecta filtro Power BI existente e não cria relacionamento, filtro, direção de filtro, alteração de dados, modelo Power BI, Power Query ou DAX.

## Produção bloqueada

Este gate não remove os bloqueios de produção, que continuam dependentes da calibração integral do motor, dos demais ciclos governados e do Gate MVP 1.0 produtivo; **a produção permanece bloqueada**. A REL-BIDIR-008 permanece uma experiência controlada em draft com confirmação humana obrigatória.
