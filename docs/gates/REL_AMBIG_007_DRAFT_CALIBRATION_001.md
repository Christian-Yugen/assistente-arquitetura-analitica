# REL-AMBIG-007 — Gate de Calibração Draft 001

## Decisão

O gate `REL-AMBIG-007-DRAFT-CALIBRATION-001` autoriza exclusivamente a futura promoção da `REL-AMBIG-007@0.1.0-provisional.1` para o perfil `executable_draft`, depois da Proposta A aprovada por Chris, do gate de reconstrução, da autorização específica posterior de implementação e da evidência sintética abaixo. **Ele não autoriza produção.**

## Evidência reproduzível

| Elemento | Evidência verificada |
|---|---|
| Dataset | `GD-REL-AMBIG-007-001`, exclusivamente sintético e sem nomes, valores, cabeçalhos, posições ou pares de origem. |
| Arquivo | `artifacts/golden/rel-ambig-draft-golden-v1.json`. |
| SHA-256 | `d644b59fac63c147c4a15adbd3978fc7f74abec7126308f7d6cc47acd6f8a817`. |
| Avaliador | `engine/calibration/evaluate_rel_ambig_draft_golden.py`. |
| Resultado | 3 verdadeiros positivos, 0 falsos positivos e 0 falsos negativos. |
| Cobertura negativa | Não-dimensão, não-fato, calendário, classificação indefinida, fato sem grão, conflito, sensibilidade, fórmula, autorreferência, ausência de chave/referência, incompletude, chave não única, referência única, cobertura parcial/zero, uma única direção, 1:1, N:N e ambiguidade de classificação. |

## Limites de ativação

A ativação draft poderá produzir somente `ambiguous_relationship_path_review_candidate`, confiança `0.60`, severidade `review_required`, evidências agregadas e pergunta humana bloqueante. O perfil e a saída não podem revelar títulos de abas, cabeçalhos, valores, posições, pares correspondentes, frequências individuais, exemplos, chaves, identificadores ou hashes de conteúdo.

O mascaramento e a `SEM-SENS-015` continuam controles independentes: qualquer sinal sensível deve bloquear a hipótese. A regra não afirma que exista caminho ambíguo em Power BI, não cria relacionamento, filtro, direção de filtro ou alteração de dados, modelo Power BI, Power Query ou DAX.

## Produção bloqueada

Este gate não remove os bloqueios de produção, que continuam dependentes da calibração integral do motor, dos demais ciclos governados e do Gate MVP 1.0 produtivo; **a produção permanece bloqueada**. A REL-AMBIG-007 permanece uma experiência controlada em draft com confirmação humana obrigatória.
