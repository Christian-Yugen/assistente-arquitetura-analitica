# SEM-ID-003-RECONSTRUCTION-AUTHORIZATION-001

**Data da decisão:** 21 de agosto de 2026.  
**Decisor:** Chris.  
**Estado:** **aprovado para implementação, testes e calibração exclusivamente em draft.**  
**Produção:** bloqueada.

## Decisão vinculada

Chris aprovou a Proposta A de `SEM_ID_003_POLICY_PROPOSAL_001.md`. A reconstrução poderá classificar uma coluna como `identifier`, sem confirmar chave de negócio e sem interpretar conteúdo de valores.

| Elemento aprovado | Limite autorizado |
|---|---|
| Base mínima | 20 valores observados |
| Sinal nominal | Vocabulário fechado e transitório: id, codigo, cod, chave, matricula, numero e num |
| Cobertura | Pelo menos 90% não ausente |
| Diversidade | Pelo menos 10% entre valores não ausentes |
| Tipos aceitos | Texto ou número físico, sem mistura |
| Confiança | 0,75 |
| Saída | `semantic_classifications` com pergunta humana não bloqueante |
| Privacidade | Nenhum valor, hash, cabeçalho, posição ou título de aba no perfil ou na projeção |

## Limites

Esta autorização permite criar perfil, classificador, testes, golden dataset, calibração e gate individual. Ela não ativa produção, não declara chave confirmada, não permite inferir formato de identificador nem substitui o gate `SEM-ID-003-DRAFT-CALIBRATION-001`.
