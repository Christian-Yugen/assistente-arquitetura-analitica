# SEM-CURR-006 — Gate de Reconstrução e Autorização 001

## Decisão

Chris aprovou explicitamente a Proposta A da `SEM-CURR-006` em 21 de agosto de 2026. Fica autorizada a reconstrução de uma implementação provisória de **Valor monetário**, limitada ao perfil draft controlado.

## Escopo autorizado

| Elemento | Limite autorizado |
|---|---|
| Identificação | Vocabulário fechado definido em `SEM_CURR_006_POLICY_PROPOSAL_001.md` |
| Base mínima | 10 números físicos finitos |
| Evidência convergente | Cabeçalho elegível e formato Excel com marcador monetário explícito em todos os números físicos |
| Exclusões | Fórmulas, números textuais, ambiguidade, data, tipo físico não numérico, cabeçalho inelegível e formato monetário incompleto ou ausente |
| Saída | `currency_candidate` na coleção canônica `semantic_classifications` |
| Confiança | `0.80` |
| Revisão humana | Pergunta bloqueante obrigatória |
| Privacidade | Somente booleanos e contagens agregadas; nenhum valor, formato, marcador, cabeçalho, posição, título de aba, hash ou identificador persistido |
| Ambiente | Exclusivamente `executable_draft`; produção permanece bloqueada |

## Implementação condicionada

A autorização permite criar um profiler privado para reduzir formatos Excel a contagens agregadas, classificador determinístico, registro semântico, versão de contrato, integração canônica, testes, dataset golden, calibração reproduzível e gate individual de calibração. A regra não poderá ser adicionada à allowlist draft até que a calibração registre os resultados e o gate individual seja formalizado.

## Limites não autorizados

Não estão autorizados reconhecimento por magnitude, casas decimais, valores negativos, valores nulos, símbolos ou códigos persistidos, texto livre de cabeçalho, inferência de moeda de negócio, promoção produtiva ou alteração de outras regras. Qualquer ampliação exige novo intake, política, aprovação explícita, testes, calibração e gate.

## Rastreabilidade

1. `artifacts/intake/SEM-CURR-006.json`.
2. `docs/rules/SEM_CURR_006_POLICY_PROPOSAL_001.md`.
3. `docs/rules/SEM_CURR_006_LOGICAL_SPEC_PROPOSAL_001.md`.
4. Aprovação explícita de Chris em 21 de agosto de 2026.
