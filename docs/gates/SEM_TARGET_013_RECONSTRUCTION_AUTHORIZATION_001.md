# SEM-TARGET-013 — Gate de Reconstrução e Autorização 001

## Decisão

Chris aprovou explicitamente a Proposta A da `SEM-TARGET-013` em 21 de agosto de 2026. Fica autorizada a reconstrução de uma implementação provisória de **Meta ou previsto**, limitada ao perfil draft controlado.

## Escopo autorizado

| Elemento | Limite autorizado |
|---|---|
| Identificação | Vocabulário fechado definido em `SEM_TARGET_013_POLICY_PROPOSAL_001.md` |
| Base mínima | 10 números físicos finitos |
| Tipo físico | Numérico |
| Exclusões | Fórmulas, texto numérico, ambiguidade, data, tipo físico não numérico e cabeçalho inelegível |
| Saída | `target_or_forecast_candidate` na coleção canônica `semantic_classifications` |
| Confiança | `0.75` |
| Revisão humana | Pergunta bloqueante obrigatória |
| Privacidade | Somente booleanos e contagens agregadas; nenhum valor, cabeçalho, fórmula, posição, título de aba, período, hash ou identificador persistido |
| Ambiente | Exclusivamente `executable_draft`; produção permanece bloqueada |

## Implementação condicionada

A autorização permite criar perfil privado, classificador determinístico, registro semântico, versão de contrato, integração canônica, testes, dataset golden, calibração reproduzível e gate individual de calibração. A regra não poderá ser adicionada à allowlist draft até que a calibração registre os resultados e o gate individual seja formalizado.

## Limites não autorizados

Não estão autorizados vocabulário fora da lista fechada, contexto de outras colunas ou abas, inferência por distribuição, períodos, fórmulas, moeda, percentual ou unidade; persistência de cabeçalho, valores ou metadados identificáveis; nem promoção produtiva. Qualquer ampliação exige novo intake, política, aprovação explícita, testes, calibração e gate.

## Rastreabilidade

1. `artifacts/intake/SEM-TARGET-013.json`.
2. `docs/rules/SEM_TARGET_013_POLICY_PROPOSAL_001.md`.
3. `docs/rules/SEM_TARGET_013_LOGICAL_SPEC_PROPOSAL_001.md`.
4. Aprovação explícita de Chris em 21 de agosto de 2026.
