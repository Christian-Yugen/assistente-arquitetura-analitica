# REL-ORPHAN-003 — Gate de Calibração Draft 001

## Decisão

O gate `REL-ORPHAN-003-DRAFT-CALIBRATION-001` autoriza exclusivamente a promoção da `REL-ORPHAN-003@0.1.0-provisional.1` para `executable_draft`, depois da Proposta A aprovada por Chris, do gate de reconstrução, da autorização específica posterior de implementação e da evidência sintética abaixo. **Ele não autoriza produção.**

## Evidência reproduzível

| Elemento | Evidência verificada |
|---|---|
| Dataset | `GD-REL-ORPHAN-003-001`, exclusivamente sintético e sem nomes, valores, cabeçalhos ou pares de origem. |
| Arquivo | `artifacts/golden/rel-orphan-draft-golden-v1.json`. |
| SHA-256 | `28b9f3b5ede8505018f494f8ce75e8bd8dedd7aca7889a3b7c92c350aa2a3641`. |
| Avaliador | `engine/calibration/evaluate_rel_orphan_draft_golden.py`. |
| Resultado | 3 verdadeiros positivos, 0 falsos positivos e 0 falsos negativos. |
| Cobertura negativa | Fórmulas, sensibilidade, incompletude, cobertura zero ou integral, autorreferência, dimensão calendário, fato sem grão, classificação indefinida, conflitos, 1:1, N:N, ambiguidade, cardinalidade/direção não elegíveis e ausência de referências não cobertas. |

## Limites de ativação

A ativação draft poderá produzir somente `orphan_reference_candidate`, confiança `0.80`, severidade `warning`, evidências agregadas e pergunta humana bloqueante. O perfil e a saída não podem revelar títulos de abas, cabeçalhos, valores, posições, pares correspondentes, frequências individuais, exemplos, chaves, identificadores ou hashes de conteúdo.

O mascaramento e a `SEM-SENS-015` continuam controles independentes: qualquer sinal sensível deve bloquear a hipótese, mesmo quando houver cobertura parcial. A regra não identifica referências sem cobertura, não confirma erro de negócio, não seleciona correção, não cria relacionamento e não altera dados ou o modelo Power BI.

## Produção bloqueada

Este gate não remove os bloqueios de produção, que continuam dependentes da calibração integral do motor, dos demais ciclos governados e do Gate MVP 1.0 produtivo; **a produção permanece bloqueada**. A REL-ORPHAN-003 permanece uma experiência controlada em draft com confirmação humana obrigatória.
