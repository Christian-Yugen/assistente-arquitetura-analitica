# QLT-BADDATE-006-RECONSTRUCTION-AUTHORIZATION-001

**Data da decisão:** 20 de agosto de 2026.  
**Decisor:** Chris.  
**Decisão:** **Aprovada a Opção A final para implementação exclusiva no perfil draft.**  
**Produção:** bloqueada.

## Objeto da autorização

Este gate autoriza a implementação da `QLT-BADDATE-006 — Datas inválidas` exclusivamente conforme a política e a especificação em `QLT_BADDATE_006_POLICY_PROPOSAL_001.md` e `QLT_BADDATE_006_LOGICAL_SPEC_PROPOSAL_001.md`. O blueprint oficial classifica a regra como `P0`, de escopo por coluna, dependente de profiling e com saída primária `finding`.

## Escopo aprovado

| Elemento | Decisão aprovada |
|---|---|
| Gramáticas elegíveis | Somente `AAAA-MM-DD`, `DD-MM-AAAA` e `DD/MM/AAAA`, com correspondência integral. |
| Validação | `date.fromisoformat` para ISO; `datetime.strptime` com `%d-%m-%Y` ou `%d/%m/%Y` para os formatos brasileiros. |
| Gatilho | Pelo menos um texto elegível que falhe no parser de calendário correspondente. |
| Evidência | Apenas contagem de candidatos estritos, contagem inválida, proporção inválida e base de normalização. |
| Severidade | Baixa até 5%, média acima de 5% até 20% e alta acima de 20%. |
| Pergunta humana | Somente para severidade média ou alta, sem identificar a coluna. |
| Intervenção | Não converter, corrigir, excluir, preencher ou reordenar dados. |

## Exclusões mandatórias

Não estão autorizados parsing de outros formatos, inferência de locale, textos de mês, horários, fusos, fórmulas, números seriais do Excel, datas nativas, códigos ou valores ausentes. A regra não pode reter ou revelar valores, amostras, posições, nomes de coluna ou títulos de abas.

## Evidências obrigatórias antes da allowlist

A implementação deverá produzir perfil agregado próprio, testes unitários positivos, negativos, limítrofes e de privacidade, golden dataset sem conteúdo bruto, manifesto SHA-256, avaliador de calibração reprodutível, gate individual de calibração e prova documental. A inclusão na allowlist só é permitida após a calibração registrar métricas explícitas de TP, FP e FN.

> Esta autorização não libera produção, não amplia o escopo para outras gramáticas e não substitui o gate de calibração individual nem o Gate MVP 1.0.
