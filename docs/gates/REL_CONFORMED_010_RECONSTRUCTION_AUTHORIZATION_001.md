# REL-CONFORMED-010 — Gate de Reconstrução 001

## Decisão registrada

A Proposta A da `REL-CONFORMED-010 — Dimensão compartilhada` foi aprovada sob a diretriz `PROPOSAL-A-APPROVAL-DELEGATION-001`. Esta decisão sela a política proposta e permite somente a preparação controlada para uma possível implementação futura no perfil draft.

> Este gate não autoriza escrever, integrar ou executar lógica da regra. Ele não altera a allowlist, não cria perfil, classificador, registro, contrato, pipeline, teste executável, golden dataset, manifesto, avaliador, calibração ou ativação draft.

## Política selada

A eventual regra poderá produzir apenas a hipótese opaca `conformed_dimension_review_candidate`. Ela deve exigir um par dimensão–fato com chave única/completa, referência não única/completa, cobertura referencial agregada de `1.0`, uma direção e contagem agregada mínima de dois fatos conectados à mesma dimensão, sem expor esses fatos.

| Grupo | Condições que bloqueiam qualquer emissão |
|---|---|
| Estrutura e cobertura | Incompletude, cobertura parcial ou zero, zero ou múltiplas direções elegíveis, menos de dois fatos conectados, padrão 1:1 ou padrão N:N. |
| Privacidade e sinais | Fórmulas, sensibilidade, valores, cabeçalhos, títulos, posições, pares correspondentes, frequências individuais, chaves, identificadores ou lista de fatos. |
| Classificação | Autorrefêrencia, dimensão calendário, fato sem granularidade, classificação indefinida, conflito ou ambiguidade. |

Se implementada após nova autorização, a regra continuará sendo apenas um alerta de revisão, com confiança máxima `0.75`, severidade `review_required` e pergunta humana bloqueante. Ela não confirma conformidade, não cria dimensão compartilhada, relação ou filtro.

## Controles preservados

O futuro perfil deverá receber somente métricas e flags agregadas. IDs opacos usados temporariamente para contar os fatos conectados devem ser descartados antes de retorno, persistência, evidência, contrato ou log. `SEM-SENS-015`, mascaramento e `sensitivity_classifications` são controles independentes e continuam bloqueando a hipótese.

## Limite da autorização

Uma autorização explícita posterior de Chris é obrigatória antes de implementar qualquer perfil, classificador, registro, contrato, pipeline, teste executável, golden dataset, manifesto, avaliador ou calibração. Depois disso, o ciclo ainda exigirá testes, dataset exclusivamente sintético, hash SHA-256, TP/FP/FN, gate individual e allowlist controlada para eventual execução draft.

**A produção permanece bloqueada.** Este gate não autoriza criação automática de dimensões, relações, filtros, Power Query, DAX ou qualquer mudança em arquivos de usuários.
