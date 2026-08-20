# QLT-MIXTYPE-005-RECONSTRUCTION-AUTHORIZATION-001

**Data da decisão:** 20 de agosto de 2026.  
**Decisor:** Chris.  
**Decisão:** **Aprovada a Opção A conservadora para implementação exclusiva no perfil draft.**  
**Produção:** bloqueada.

## Objeto da autorização

Este gate autoriza a implementação da `QLT-MIXTYPE-005 — Tipos mistos` somente conforme a política e a especificação propostas em `QLT_MIXTYPE_005_POLICY_PROPOSAL_001.md` e `QLT_MIXTYPE_005_LOGICAL_SPEC_PROPOSAL_001.md`. A fonte oficial registra a regra como `P0`, de escopo por coluna, dependente de profiling e com saída primária `finding`.

## Escopo aprovado

| Elemento | Decisão aprovada |
|---|---|
| Condição | Emitir finding somente para ao menos cinco valores não ausentes, com dois ou mais grupos físicos incompatíveis e pelo menos duas ocorrências por grupo. |
| Grupos elegíveis | Booleano, número físico, texto não numérico e valor temporal físico. |
| Ausências | Excluir nulos estruturais, texto em branco e `NaN` numérico do denominador e da avaliação. |
| Números em texto | Excluir cadeias numéricas canônicas desta regra e preservar sua avaliação na QLT-NUMTEXT-007. |
| Evidência | Somente contagens, proporções e base de normalização; sem valores, exemplos, fórmulas, posições, nomes de colunas ou títulos de aba. |
| Intervenção | Não converter, excluir, preencher, reordenar ou corrigir qualquer célula. |
| Pergunta | Exigir validação humana apenas para severidade média ou alta, sem identificar a coluna. |

## Exclusões mandatórias

Não estão autorizadas inferência de tipo de negócio, interpretação de códigos numéricos, parsing de datas em texto, reconhecimento de sentinelas, atribuição de chave, alteração automática de tipo, execução fora do perfil draft ou promoção produtiva.

## Evidências e controles requeridos antes de ativação

A implementação deverá criar perfil agregado próprio, testes unitários positivos, negativos, limítrofes e de privacidade, golden dataset sem dados brutos, manifesto SHA-256, avaliador de calibração reprodutível, gate de calibração individual e prova documental da cadeia de decisão. A regra só poderá entrar na allowlist após métricas explícitas de verdadeiros positivos, falsos positivos e falsos negativos no dataset autorizado.

> A autorização de Chris para a Opção A permite apenas a execução deste ciclo draft. Não libera produção, não amplia o catálogo produtivo e não substitui o gate de calibração da regra nem o Gate MVP 1.0.
