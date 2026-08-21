# GRN-COMP-001-RECONSTRUCTION-AUTHORIZATION-001

**Data da decisão:** 21 de agosto de 2026.  
**Decisor:** Chris.  
**Estado:** **aprovado para implementação, testes e calibração exclusivamente no perfil draft.**  
**Produção:** bloqueada.

## Decisão vinculada

Chris aprovou a **Opção A** de `GRN_COMP_001_POLICY_PROPOSAL_001.md`. A reconstrução poderá produzir somente uma hipótese `composite_key_candidate` por aba, com confirmação humana obrigatória, sem declarar chave de negócio, alterar dados ou habilitar inferências relacionais posteriores.

| Elemento aprovado | Limite autorizado |
|---|---|
| Base mínima | 20 linhas observadas |
| Elegibilidade | Pares previamente elegíveis pela tipagem semântica |
| Completude | 100% em ambos os componentes do par |
| Unicidade individual | Nenhum componente único isoladamente |
| Unicidade conjunta | 100% das combinações observadas |
| Limite de busca | Até 10 pares por aba |
| Saída | Hipótese de granularidade; confiança 0,70; pergunta humana obrigatória |
| Privacidade | Apenas contagens agregadas; nenhum valor, par, hash, cabeçalho, posição ou título de aba |

## Limites

Esta autorização permite criar perfil, avaliador, testes, golden dataset, calibração e o gate draft individual. Ela não ativa a regra, não libera produção, não confirma chaves de negócio e não substitui o gate de calibração `GRN-COMP-001-DRAFT-CALIBRATION-001`.
