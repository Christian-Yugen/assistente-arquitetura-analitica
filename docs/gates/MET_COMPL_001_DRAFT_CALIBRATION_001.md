# MET-COMPL-001 — Gate de Calibração Draft 001

## Decisão

O gate `MET-COMPL-001-DRAFT-CALIBRATION-001` autoriza exclusivamente a futura promoção da `MET-COMPL-001@0.1.0-provisional.1` para o perfil `executable_draft`, depois da Proposta A aprovada sob a diretriz de Chris, do gate de reconstrução, da autorização específica posterior de implementação e da evidência sintética abaixo. **Ele não autoriza produção.**

## Evidência reproduzível

| Elemento | Evidência verificada |
|---|---|
| Dataset | `GD-MET-COMPL-001-001`, exclusivamente sintético e sem valores de status, cabeçalhos, posições, identificadores ou DAX. |
| Arquivo | `artifacts/golden/met-compl-draft-golden-v1.json`. |
| SHA-256 | `f6eb5dfe943b9e428dda692eee431b93850a1474e4cbec19a3e8c1863e4baaaf`. |
| Avaliador | `engine/calibration/evaluate_met_compl_draft_golden.py`. |
| Resultado | 3 verdadeiros positivos, 0 falsos positivos e 0 falsos negativos. |
| Cobertura negativa | Linhas/colunas insuficientes, zero ou múltiplos candidatos de status, grão ausente/ambíguo, classificação indefinida, fato sem grão, conflito, sensibilidade e fórmula. |

## Limites de ativação

A ativação draft poderá produzir somente `completion_rate_conceptual_metric_candidate`, confiança `0.60`, severidade `review_required`, evidências agregadas, fórmula conceitual `completed_items / eligible_items` e pergunta humana bloqueante. O perfil e a saída não podem revelar valores de status, títulos, cabeçalhos, posições, exemplos, frequências individuais, identificadores ou DAX.

O mascaramento e a `SEM-SENS-015` continuam controles independentes: qualquer sinal sensível deve bloquear a recomendação. A regra não calcula percentual, não escolhe estados concluídos, não define o denominador e não cria medida, DAX, Power Query, alteração de dados ou modelo Power BI.

## Produção bloqueada

Este gate não remove os bloqueios de produção, que continuam dependentes da calibração integral do motor, dos demais ciclos governados e do Gate MVP 1.0 produtivo; **a produção permanece bloqueada**. A MET-COMPL-001 permanece uma recomendação conceitual controlada em draft com confirmação humana obrigatória.
