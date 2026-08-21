# QLT-FORMULA-013-RECONSTRUCTION-AUTHORIZATION-001

**Data da proposta:** 20 de agosto de 2026.  
**Decisor requerido:** Chris.  
**Estado da decisão:** **aprovada para implementação, testes e calibração no perfil draft.**  
**Produção:** bloqueada.

## Objeto da decisão

O blueprint oficial recuperado define a `QLT-FORMULA-013 — Fórmulas inconsistentes` como regra P1, por coluna, dependente de profiling e com saída `finding`, mas não define a divergência a detectar. A Proposta A em `QLT_FORMULA_013_POLICY_PROPOSAL_001.md` e `QLT_FORMULA_013_LOGICAL_SPEC_PROPOSAL_001.md` limita a reconstrução a rupturas de presença versus ausência de fórmula em colunas predominantemente calculadas, usando apenas o tipo interno da célula.

| Elemento a aprovar | Proposta A |
|---|---|
| Base de elegibilidade | Pelo menos 10 células físicas não vazias, 8 fórmulas e participação de fórmula de pelo menos 80%. |
| Sinal fechado | Pelo menos uma célula física não vazia sem fórmula na coluna elegível. |
| Inspeção permitida | Apenas presença e `data_type == "f"` de forma transitória; não ler, reter ou comparar expressões. |
| Evidência | Contagens e proporção agregadas; sem fórmulas, referências, valores, cabeçalhos, posições ou títulos de aba. |
| Exclusões | Células vazias, base insuficiente, baixa participação de fórmulas, comparação entre expressões, recálculo e qualquer análise de significado do valor manual. |
| Saída | Finding com confiança moderada e pergunta humana em toda ocorrência. |
| Intervenção | Nenhuma cópia, criação, correção, preenchimento ou exclusão automática. |

## Decisão solicitada

Chris aprovou a Proposta A. A aprovação autoriza somente implementação, testes e calibração do perfil draft descrito; não ativa a regra, não libera produção, não permite leitura de expressões ou fórmulas automáticas e não substitui o gate individual de calibração.

> Até a aprovação do gate individual de calibração, `QLT-FORMULA-013` permanece fora da allowlist e não pode executar no perfil draft.
