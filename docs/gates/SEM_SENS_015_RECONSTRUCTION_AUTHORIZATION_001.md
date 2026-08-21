# SEM-SENS-015 — Gate de Reconstrução e Autorização 001

## Decisão

Chris aprovou explicitamente a Proposta A da `SEM-SENS-015` em 21 de agosto de 2026. Fica autorizada a reconstrução de uma implementação provisória de **Sensibilidade e dado pessoal**, limitada ao perfil draft controlado.

## Escopo autorizado

| Elemento | Limite autorizado |
|---|---|
| Identificação | Somente o vocabulário fechado definido em `SEM_SENS_015_POLICY_PROPOSAL_001.md` |
| Evidência | Cabeçalho elegível e ao menos uma observação não ausente, ambos reduzidos a sinais agregados |
| Inspeção de valores | Proibida |
| Saída | `personal_data_candidate` no campo canônico `sensitivity` |
| Confiança | `0.90` |
| Revisão humana | Pergunta bloqueante obrigatória |
| Mascaramento | Controle existente, independente, obrigatório e não condicionado à classificação |
| Privacidade | Nenhum valor, cabeçalho, formato, domínio, posição, aba, hash ou identificador persistido |
| Ambiente | Exclusivamente `executable_draft`; produção permanece bloqueada |

## Implementação condicionada

A autorização permite reutilizar somente sinais privados já agregados do perfil de identificador, criar classificador determinístico, registro semântico, versão de contrato, integração canônica, testes sem dados pessoais, dataset golden sintético apenas com contagens e cabeçalhos de regra, calibração reprodutível e gate individual de calibração. A regra não poderá ser adicionada à allowlist draft até que a calibração registre os resultados e o gate individual seja formalizado.

## Limites não autorizados

Não estão autorizadas inspeção ou reconhecimento de padrão de valores, retenção de amostras, uso de domínio de e-mail, formatos de documento, contexto de outras colunas ou abas, redução do mascaramento existente, decisão jurídica, classificação definitiva de dado sensível ou promoção produtiva. Qualquer ampliação exige novo intake, política, aprovação explícita, testes, calibração e gate.

## Rastreabilidade

1. `artifacts/intake/SEM-SENS-015.json`.
2. `docs/rules/SEM_SENS_015_POLICY_PROPOSAL_001.md`.
3. `docs/rules/SEM_SENS_015_LOGICAL_SPEC_PROPOSAL_001.md`.
4. Aprovação explícita de Chris em 21 de agosto de 2026.
