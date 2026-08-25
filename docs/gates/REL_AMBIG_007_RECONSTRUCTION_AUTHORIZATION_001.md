# REL-AMBIG-007 — Gate de Reconstrução 001

## Decisão registrada

Chris aprovou explicitamente a **Proposta A** da `REL-AMBIG-007 — Caminhos ambíguos`, sob a diretriz `PROPOSAL-A-APPROVAL-DELEGATION-001`. Esta decisão sela a política proposta e permite somente a preparação controlada para uma possível implementação futura no perfil draft.

> Este gate não autoriza escrever, integrar ou executar lógica da regra. Ele não altera a allowlist, não cria perfil, classificador, registro, contrato, pipeline, teste executável, golden dataset, manifesto, avaliador, calibração ou ativação draft.

## Política selada

A eventual regra poderá produzir apenas a hipótese opaca `ambiguous_relationship_path_review_candidate`. Ela deve exigir um par de abas distintas já classificadas como dimensão padrão e fato transacional/periódico, ao menos uma chave e uma referência completas com unicidade compatível, cobertura referencial agregada de `1.0` e duas ou mais direções candidatas agregadas.

| Grupo | Condições que bloqueiam qualquer emissão |
|---|---|
| Estrutura e cobertura | Incompletude, cobertura parcial ou zero, zero ou uma direção elegível, padrão 1:1 ou padrão N:N. |
| Privacidade e sinais | Fórmulas, sensibilidade, valores, cabeçalhos, títulos, posições, pares correspondentes, frequências individuais, chaves ou identificadores. |
| Classificação | Autorrefêrencia, dimensão calendário, fato sem granularidade, classificação indefinida, conflito ou ambiguidade de classificação. |

Se implementada após nova autorização, a regra continuará sendo apenas um alerta de revisão, com confiança máxima `0.60`, severidade `review_required` e pergunta humana bloqueante. Ela não afirma que exista caminho ambíguo no Power BI e não recomenda criar relações, filtros ou direções de filtro.

## Controles preservados

O futuro perfil deverá receber somente métricas e flags agregadas de um par opaco. Qualquer identificador opaco transitório usado antes da agregação deve ser descartado antes de retorno, persistência, evidência, contrato ou log. `SEM-SENS-015`, mascaramento e `sensitivity_classifications` são controles independentes e continuam bloqueando a hipótese.

## Limite da autorização

Uma autorização explícita posterior de Chris é obrigatória antes de implementar qualquer perfil, classificador, registro, contrato, pipeline, teste executável, golden dataset, manifesto, avaliador ou calibração. Depois disso, o ciclo ainda exigirá testes, dataset exclusivamente sintético, hash SHA-256, TP/FP/FN, gate individual e allowlist controlada para eventual execução draft.

**A produção permanece bloqueada.** Este gate não autoriza criação automática de relações, filtros, Power Query, DAX ou qualquer mudança em arquivos de usuários.
