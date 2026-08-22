# SEM-DUR-008 — Gate de Reconstrução e Autorização 001

## Decisão

Chris aprovou explicitamente a Proposta A da `SEM-DUR-008` nesta sessão. Fica autorizada a reconstrução de uma implementação provisória de **Duração**, limitada ao perfil draft controlado.

## Escopo autorizado

| Elemento | Limite autorizado |
|---|---|
| Vocabulário | Após normalização transitória: `duracao`, `duracao (horas)`, `duracao (minutos)`, `duracao (segundos)` e `duracao (dias)` |
| Base | No mínimo 10 observações não ausentes, todas números físicos finitos |
| Fórmulas | `formula_count = 0` é obrigatório |
| Datas | `recognized_date_count = 0` é obrigatório |
| Ambiguidade | `ambiguity_count = 0` é obrigatório |
| Conflitos | Não emitir quando quantidade, percentual, moeda, data ou competência estiverem elegíveis |
| Saída | `duration_candidate` no campo canônico `semantic_type` |
| Confiança | `0.80` |
| Revisão humana | Pergunta bloqueante obrigatória |
| Ambiente | Exclusivamente `executable_draft`; produção permanece bloqueada |

## Privacidade e limites

O profiler poderá reter apenas `header_eligible` e contagens agregadas de números físicos, não ausentes, fórmulas, datas reconhecidas e ambiguidades. O cabeçalho será normalizado somente em memória para produzir o booleano de elegibilidade.

Não são autorizadas inspeção ou retenção de valores, texto, cabeçalhos, tokens, unidade derivada, exemplos, mínimo, máximo, média, distribuição, posição, título de aba, formato de célula, fórmula, domínio, magnitude, frequência ou hash de conteúdo. O mascaramento existente continua independente e obrigatório.

## Implementação condicionada

A autorização permite somente um perfil agregado imutável, classificador determinístico, registro semântico, versão contratual, integração canônica protegida por allowlist, testes unitários e de pipeline, golden dataset sintético, SHA-256, avaliador reproduzível de TP/FP/FN e gate individual de calibração.

Não estão autorizadas conversão, inferência ou normalização de unidade; `tempo`, `horas`, `minutos`, `segundos`, `dias`, `prazo`, `periodo`, `intervalo`, `meses`, `anos` e qualquer sinônimo livre continuam fora do vocabulário.

## Rastreabilidade

1. `artifacts/intake/SEM-DUR-008.json`.
2. `docs/rules/SEM_DUR_008_POLICY_PROPOSAL_001.md`.
3. `docs/rules/SEM_DUR_008_LOGICAL_SPEC_PROPOSAL_001.md`.
4. Aprovação explícita de Chris para a Proposta A nesta sessão.
