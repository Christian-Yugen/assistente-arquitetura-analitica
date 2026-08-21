# QLT-IDMISS-015-RECONSTRUCTION-AUTHORIZATION-001

**Data da proposta:** 20 de agosto de 2026.  
**Decisor requerido:** Chris.  
**Estado da decisão:** **aprovada por Chris para a Proposta A, exclusivamente no perfil draft.**  
**Produção:** bloqueada.

## Objeto da decisão

O blueprint oficial recuperado define a `QLT-IDMISS-015 — Identificadores incompletos` como regra P0, por coluna, dependente de profiling e com saída `finding`, mas não define cabeçalhos de identificador, formato, normalização ou limiares. A Proposta A em `QLT_IDMISS_015_POLICY_PROPOSAL_001.md` e `QLT_IDMISS_015_LOGICAL_SPEC_PROPOSAL_001.md` restringe a reconstrução a ausência e duplicidade exata em vocabulário fechado, preservando a avaliação de formatos inválidos para uma decisão futura específica.

| Elemento a aprovar | Proposta A |
|---|---|
| Vocabulário fechado | `id`, `codigo`, `cod`, `chave`, `matricula`, `cpf`, `cnpj`, `numero` e `num`, após normalização técnica do cabeçalho. |
| Base mínima | Pelo menos 10 células observadas. |
| Sinais autorizados | Ausência privada e repetição exata, tipada e transitória de valores não ausentes. |
| Evidência | Contagens e razões agregadas; sem cabeçalho, identificador, valor, hash, posição, exemplo ou título de aba. |
| Exclusões | Inferência de chave, chaves compostas, similaridade, normalização de valores, fórmulas, números em texto, formatos inválidos e correção automática. |
| Saída | Finding com confiança moderada e pergunta humana em toda ocorrência. |
| Intervenção | Nenhum preenchimento, geração, correção, deduplicação ou alteração automática. |

## Decisão solicitada

Chris aprovou a Proposta A. A decisão autorizou somente implementação, testes e calibração do perfil draft descrito; não ativou a regra, não liberou produção, não autorizou validação de formato e não substituiu o gate individual de calibração.

> Esta autorização não amplia o perfil draft e não remove qualquer bloqueio de produção.
