# REL-COMPKEY-009 — Gate de Reconstrução 001

## Decisão registrada

A Proposta A da `REL-COMPKEY-009 — Chave composta` foi aprovada sob a diretriz `PROPOSAL-A-APPROVAL-DELEGATION-001`. Esta decisão sela a política proposta e permite somente a preparação controlada para uma possível implementação futura no perfil draft.

> Este gate não autoriza escrever, integrar ou executar lógica da regra. Ele não altera a allowlist, não cria profiler, perfil, classificador, registro, contrato, pipeline, teste executável, golden dataset, manifesto, avaliador, calibração ou ativação draft.

## Política selada

A eventual regra poderá produzir apenas a hipótese opaca `composite_relationship_key_review_candidate`. Ela deve exigir um par de abas distintas já classificadas como dimensão padrão e fato transacional/periódico, exatamente uma composição de dois campos completa e única, uma referência composta completa e não única, nenhuma chave simples elegível, cobertura referencial agregada de `1.0` e exatamente uma direção candidata.

| Grupo | Condições que bloqueiam qualquer emissão |
|---|---|
| Estrutura e cobertura | Chave simples elegível, zero ou múltiplas composições, incompletude, cobertura parcial ou zero, zero ou múltiplas direções, padrão 1:1 ou padrão N:N. |
| Privacidade e sinais | Fórmulas, sensibilidade, valores, cabeçalhos, títulos, posições, pares correspondentes, frequências individuais, tuplas, assinaturas, chaves ou identificadores. |
| Classificação | Autorrefêrencia, dimensão calendário, fato sem granularidade, classificação indefinida, conflito ou ambiguidade. |

Se implementada após nova autorização, a regra continuará sendo apenas um alerta de revisão, com confiança máxima `0.70`, severidade `review_required` e pergunta humana bloqueante. Ela não cria colunas concatenadas, relação, filtro ou direção de filtro.

## Controles preservados

Um futuro profiler pode usar assinaturas transitórias de tuplas de dois campos em memória somente para derivar métricas agregadas; deve descartá-las antes de retorno, persistência, evidência, contrato ou log. `SEM-SENS-015`, mascaramento e `sensitivity_classifications` são controles independentes e continuam bloqueando a hipótese.

## Limite da autorização

Uma autorização explícita posterior de Chris é obrigatória antes de implementar qualquer profiler, perfil, classificador, registro, contrato, pipeline, teste executável, golden dataset, manifesto, avaliador ou calibração. Depois disso, o ciclo ainda exigirá testes, dataset exclusivamente sintético, hash SHA-256, TP/FP/FN, gate individual e allowlist controlada para eventual execução draft.

**A produção permanece bloqueada.** Este gate não autoriza criação automática de colunas, relações, filtros, Power Query, DAX ou qualquer mudança em arquivos de usuários.
