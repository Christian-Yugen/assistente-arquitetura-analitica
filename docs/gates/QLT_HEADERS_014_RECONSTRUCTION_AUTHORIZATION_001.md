# QLT-HEADERS-014-RECONSTRUCTION-AUTHORIZATION-001

**Data da proposta:** 20 de agosto de 2026.  
**Decisor requerido:** Chris.  
**Estado da decisão:** **aprovada por Chris para a Proposta A, exclusivamente no perfil draft.**  
**Produção:** bloqueada.

## Objeto da decisão

O blueprint oficial recuperado define a `QLT-HEADERS-014 — Cabeçalhos inválidos` como regra P0, por aba, dependente de profiling e com saída `finding`, mas não determina como classificar ausência, duplicidade ou multinível. A Proposta A em `QLT_HEADERS_014_POLICY_PROPOSAL_001.md` e `QLT_HEADERS_014_LOGICAL_SPEC_PROPOSAL_001.md` restringe a reconstrução à primeira linha e a sinais estruturais transitórios com evidência agregada.

| Elemento a aprovar | Proposta A |
|---|---|
| Linha analisada | Somente primeira linha materializada, sem busca de outra linha de cabeçalho. |
| Sinais autorizados | Ausência, duplicidade textual normalizada e candidato multinível por range mesclado horizontal iniciado na primeira linha. |
| Critério multinível | Range com largura de ao menos duas colunas e pelo menos duas células físicas não vazias na segunda linha. |
| Evidência | Contagens agregadas; sem títulos, abas, textos, posições, ranges ou valores. |
| Exclusões | Estilos, cores, comentários, fórmulas, nomes semânticos, cabeçalhos posteriores, mesclagens fora da primeira linha e correção automática. |
| Saída | Finding com confiança moderada e pergunta humana em toda ocorrência. |
| Intervenção | Nenhum preenchimento, renomeação, deduplicação, desmesclagem ou alteração estrutural automática. |

## Decisão solicitada

Chris aprovou a Proposta A. A decisão autorizou somente implementação, testes e calibração do perfil draft descrito; não ativou produção, não autorizou revelar títulos ou cabeçalhos e não substituiu o gate individual de calibração.

> Esta autorização não amplia o perfil draft e não remove qualquer bloqueio de produção.
