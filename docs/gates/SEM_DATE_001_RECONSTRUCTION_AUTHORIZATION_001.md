# SEM-DATE-001-RECONSTRUCTION-AUTHORIZATION-001

**Data da proposta:** 20 de agosto de 2026.  
**Decisor requerido:** Chris.  
**Estado da decisão:** **pendente de aprovação.**  
**Produção:** bloqueada.

## Objeto da decisão

O blueprint oficial recuperado define a `SEM-DATE-001 — Data genérica` como regra P0, por coluna, dependente de profiling e com saída `semantic_type`, mas não determina formatos, limiares, confiança ou projeção no contrato. A Proposta A em `SEM_DATE_001_POLICY_PROPOSAL_001.md` e `SEM_DATE_001_LOGICAL_SPEC_PROPOSAL_001.md` restringe a reconstrução a datas físicas e três gramáticas textuais estritas, com cobertura de 100% e saída canônica isolada.

| Elemento a aprovar | Proposta A |
|---|---|
| Base mínima | Pelo menos 10 valores físicos não ausentes. |
| Valores permitidos | Datas físicas e textos válidos em `AAAA-MM-DD`, `DD-MM-AAAA` ou `DD/MM/AAAA`, após `strip`. |
| Limiar | 100% dos valores físicos não ausentes devem ser reconhecidos. |
| Classificação | `date_generic`, confiança moderada e pergunta humana não bloqueante. |
| Projeção de contrato | Coleção `semantic_classifications` opcional, agregada e versionada, sem alterar a semântica de findings e questions existentes. |
| Exclusões | Seriais Excel, timestamps textuais, horas, outros formatos, locale, timezone, cabeçalho, papel de negócio, conversão e correção automática. |
| Intervenção | Nenhuma transformação de dados ou planilha. |

## Decisão solicitada

Chris deve aprovar ou rejeitar a Proposta A, incluindo a extensão mínima `semantic_classifications` no fragmento canônico. A aprovação autoriza somente implementação, testes e calibração do perfil draft descrito; não ativa a regra, não libera produção, não autoriza outros formatos e não substitui o gate individual de calibração.

> Até que a decisão seja registrada como aprovada, `SEM-DATE-001` permanece fora da allowlist e nenhum módulo executável ou extensão de contrato será criado ou alterado.
