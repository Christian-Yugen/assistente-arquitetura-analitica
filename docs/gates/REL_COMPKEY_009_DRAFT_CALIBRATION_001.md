# REL-COMPKEY-009 — Gate de Calibração Draft 001

## Decisão

O gate `REL-COMPKEY-009-DRAFT-CALIBRATION-001` autoriza exclusivamente a futura promoção da `REL-COMPKEY-009@0.1.0-provisional.1` para o perfil `executable_draft`, depois da Proposta A aprovada sob a diretriz de Chris, do gate de reconstrução, da autorização específica posterior de implementação e da evidência sintética abaixo. **Ele não autoriza produção.**

## Evidência reproduzível

| Elemento | Evidência verificada |
|---|---|
| Dataset | `GD-REL-COMPKEY-009-001`, exclusivamente sintético e sem nomes, valores, cabeçalhos, posições, tuplas ou assinaturas de origem. |
| Arquivo | `artifacts/golden/rel-compkey-draft-golden-v1.json`. |
| SHA-256 | `f1fae8383331b1fa900af2163af6c78674fe450bf6d837d747be35d35792d3fa`. |
| Avaliador | `engine/calibration/evaluate_rel_compkey_draft_golden.py`. |
| Resultado | 3 verdadeiros positivos, 0 falsos positivos e 0 falsos negativos. |
| Cobertura negativa | Não-dimensão, não-fato, calendário, classificação indefinida, fato sem grão, conflito, sensibilidade, fórmula, autorreferência, chave simples, zero/múltiplas composições, incompletude, chave composta não única, referência composta única, cobertura parcial/zero, direção ambígua, 1:1, N:N e ambiguidade. |

## Limites de ativação

A ativação draft poderá produzir somente `composite_relationship_key_review_candidate`, confiança `0.70`, severidade `review_required`, evidências agregadas e pergunta humana bloqueante. O perfil e a saída não podem revelar títulos de abas, cabeçalhos, valores, posições, pares correspondentes, frequências individuais, exemplos, tuplas, assinaturas, chaves, identificadores ou hashes de conteúdo.

O profiler poderá usar assinaturas transitórias de tuplas de dois campos apenas em memória para derivar métricas agregadas e deve descartá-las antes de retorno, persistência, evidência, contrato ou log. O mascaramento e a `SEM-SENS-015` continuam controles independentes: qualquer sinal sensível deve bloquear a hipótese. A regra não cria colunas concatenadas, relacionamento, filtro, alteração de dados, modelo Power BI, Power Query ou DAX.

## Produção bloqueada

Este gate não remove os bloqueios de produção, que continuam dependentes da calibração integral do motor, dos demais ciclos governados e do Gate MVP 1.0 produtivo; **a produção permanece bloqueada**. A REL-COMPKEY-009 permanece uma experiência controlada em draft com confirmação humana obrigatória.
