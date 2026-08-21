# QLT-TOTALROW-010-RECONSTRUCTION-AUTHORIZATION-001

**Data da decisão:** 20 de agosto de 2026.  
**Decisor:** Chris.  
**Decisão:** **Aprovada a Opção A para implementação exclusiva no perfil draft.**  
**Produção:** bloqueada.

## Objeto da autorização

Este gate autoriza a implementação da `QLT-TOTALROW-010 — Linhas de totalização` somente conforme a política e a especificação em `QLT_TOTALROW_010_POLICY_PROPOSAL_001.md` e `QLT_TOTALROW_010_LOGICAL_SPEC_PROPOSAL_001.md`. O blueprint oficial classifica a regra como P0, de escopo por aba, dependente de profiling e com saída `finding`.

## Escopo aprovado

| Elemento | Decisão aprovada |
|---|---|
| Prefixo tabular | Pelo menos três linhas com conteúdo antes da linha candidata. |
| Rótulo elegível | A primeira célula significativa, após normalização técnica restrita, é exatamente `total`, `subtotal` ou `total geral`. |
| Sinal numérico | A linha candidata contém pelo menos um valor numérico físico em outra célula. |
| Evidência | Somente contagem de linhas candidatas, linhas com conteúdo e proporção; sem valores, fórmulas, posições, nomes de coluna ou títulos de aba. |
| Severidade | Baixa até 5%; média acima de 5% até 20%; alta acima de 20%. |
| Pergunta | Apenas para severidade média ou alta, sem identificar a aba. |
| Intervenção | Não calcular somas, interpretar fórmulas, excluir, mover, preencher ou alterar linhas. |

## Exclusões mandatórias

Não estão autorizadas correspondência parcial, sinônimos, outros idiomas, números em texto, fórmulas, valores de data, verificação de igualdade de soma, inferência de hierarquia, deduplicação, tratamento de linhas vazias ou qualquer mudança no workbook. Linhas anteriores ao limiar de três linhas com conteúdo permanecem excluídas.

## Evidências obrigatórias antes da allowlist

A implementação deverá produzir perfil agregado por aba, testes positivos, negativos, limítrofes e de privacidade, golden dataset sem conteúdo bruto, manifesto SHA-256, avaliador de calibração reprodutível, gate individual de calibração e prova documental. A entrada na allowlist depende de métricas explícitas de TP, FP e FN no dataset autorizado.

> A autorização de Chris permite somente este ciclo draft. Não libera produção, não amplia o vocabulário e não substitui o gate de calibração nem o Gate MVP 1.0.
