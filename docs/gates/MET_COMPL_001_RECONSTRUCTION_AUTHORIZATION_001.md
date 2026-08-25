# MET-COMPL-001 — Gate de Reconstrução 001

## Decisão registrada

A Proposta A da `MET-COMPL-001 — Percentual de conclusão` foi aprovada sob a diretriz `PROPOSAL-A-APPROVAL-DELEGATION-001`. Esta decisão sela a política proposta e permite somente a preparação controlada para uma possível implementação futura no perfil draft.

> Este gate não autoriza escrever, integrar ou executar lógica da regra. Ele não altera a allowlist, não cria perfil, classificador, registro, contrato, pipeline, teste executável, golden dataset, manifesto, avaliador, calibração ou ativação draft.

## Política selada

A eventual regra poderá produzir apenas a recomendação opaca `completion_rate_conceptual_metric_candidate`. Ela deve exigir 20 ou mais linhas, duas ou mais colunas físicas, exatamente um candidato de status e granularidade definida, sem escolher valores de status, sem calcular percentual e sem gerar DAX.

| Grupo | Condições que bloqueiam qualquer emissão |
|---|---|
| Estrutura e semântica | Menos de 20 linhas, menos de duas colunas, zero ou múltiplos candidatos de status, grão ausente/ambíguo, classificação indefinida, fato sem grão ou conflito. |
| Privacidade e sinais | Sensibilidade, fórmulas, valores, cabeçalhos, títulos, posições, exemplos, frequências individuais ou identificadores. |
| Ação automática | Cálculo de percentual, escolha de estados concluídos, definição do denominador, geração de DAX/M, criação de medida ou mudança de arquivo/modelo. |

Se implementada após nova autorização, a regra continuará sendo apenas uma recomendação conceitual, com confiança máxima `0.60`, severidade `review_required` e pergunta humana bloqueante. Ela não cria medida, calcula percentual ou modifica Power BI.

## Controles preservados

O futuro perfil deverá receber somente métricas e flags agregadas. `SEM-SENS-015`, mascaramento e `sensitivity_classifications` são controles independentes e continuam bloqueando a hipótese.

## Limite da autorização

Uma autorização explícita posterior de Chris é obrigatória antes de implementar qualquer perfil, classificador, registro, contrato, pipeline, teste executável, golden dataset, manifesto, avaliador ou calibração. Depois disso, o ciclo ainda exigirá testes, dataset exclusivamente sintético, hash SHA-256, TP/FP/FN, gate individual e allowlist controlada para eventual execução draft.

**A produção permanece bloqueada.** Este gate não autoriza criação automática de métricas, DAX, Power Query ou qualquer mudança em arquivos de usuários.
