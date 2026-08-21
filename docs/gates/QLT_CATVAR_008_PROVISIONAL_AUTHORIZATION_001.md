# Gate QLT-CATVAR-008-PROVISIONAL-AUTHORIZATION-001

## Decisão

> **Aprovado por Chris para implementação provisória no perfil draft.** A autorização permite normalização técnica de espaços, caixa, pontuação e acentuação, além da criação de um mecanismo de dicionário de domínio versionável. Ela não autoriza equivalência automática para siglas, abreviações, singular/plural, sinônimos ou distância textual.

| Critério | Evidência | Decisão |
|---|---|---|
| Identidade oficial | Blueprint `PM-MVP-PBI-RULE-BP-001`, sequência 8 | Conforme |
| Política operacional | `QLT_CATVAR_008_POLICY_PROVISIONAL_001.md` | Aprovada para draft |
| Limite semântico | Dicionário vazio e sem fusão automática | Obrigatório |
| Privacidade | Evidência estritamente agregada | Obrigatório |
| Implementação | Profiling, executor, testes e golden dataset | Autorizada |
| Ativação na allowlist draft | Depende de calibração e gate de fechamento | Bloqueada neste gate |
| Produção | Depende do Gate MVP 1.0 e de todos os bloqueios globais | Bloqueada |

## Risco controlado

A remoção de acentos e normalização de pontuação podem unir grafias que sejam distintos códigos de negócio. Por isso, a saída é um finding candidato e não uma transformação; a pergunta em severidade alta preserva a decisão humana. A política não incorpora inferência lexical, nem cria um dicionário de termos sem fonte de domínio fornecida por Chris.

## Próximo gate

O gate `QLT-CATVAR-008-DRAFT-CALIBRATION-001` deverá registrar implementação, testes positivos e negativos, golden dataset, resultados de falsos positivos/falsos negativos e decisão explícita de inclusão — ou não — na allowlist draft.
