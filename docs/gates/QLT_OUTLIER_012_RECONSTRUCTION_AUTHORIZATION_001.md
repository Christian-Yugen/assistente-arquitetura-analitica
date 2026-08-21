# QLT-OUTLIER-012-RECONSTRUCTION-AUTHORIZATION-001

**Data da proposta:** 20 de agosto de 2026.  
**Decisor requerido:** Chris.  
**Estado da decisão:** **aprovada por Chris para implementação e calibração draft.**  
**Produção:** bloqueada.

## Objeto da decisão

O blueprint oficial recuperado define a `QLT-OUTLIER-012 — Valores atípicos` como regra P1, por coluna, dependente de profiling e com saída `finding`, mas não determina método estatístico ou critérios de execução. A Proposta A em `QLT_OUTLIER_012_POLICY_PROPOSAL_001.md` e `QLT_OUTLIER_012_LOGICAL_SPEC_PROPOSAL_001.md` restringe a reconstrução a uma cerca de Tukey com limites objetivos, dados agregados e validação humana.

| Elemento a aprovar | Proposta A |
|---|---|
| Base de elegibilidade | Pelo menos 20 números físicos finitos e 80% de participação numérica. |
| Método fechado | Quartis por interpolação linear e cercas `Q1 − 1,5 × IQR` e `Q3 + 1,5 × IQR`. |
| Caso sem dispersão | `IQR = 0` não gera finding e não aciona método alternativo. |
| Evidência | Contagens e proporção agregadas; sem valores, quartis, cercas, cabeçalhos, posições ou títulos de aba. |
| Exclusões | Números em texto, fórmulas, datas, booleanos, erros, não finitos, base insuficiente, baixa participação numérica e análises de domínio. |
| Saída | Finding com confiança moderada e pergunta humana em toda ocorrência. |
| Intervenção | Nenhuma transformação, remoção ou correção automática. |

## Decisão solicitada

Chris aprovou a Proposta A. Esta decisão autoriza somente implementação, testes e calibração do perfil draft definido; não ativa a regra, não libera produção, não permite métodos alternativos e não substitui o gate individual de calibração.

> A regra permanece fora da allowlist até a aprovação do golden dataset, da calibração e do gate individual de calibração.
