# SEM-STATUS-009 — Gate de Reconstrução e Autorização 001

## Decisão

Chris aprovou explicitamente a Proposta A da `SEM-STATUS-009` nesta sessão. Fica autorizada a reconstrução de uma implementação provisória de **Status**, limitada ao perfil draft controlado.

## Escopo autorizado

| Elemento | Limite autorizado |
|---|---|
| Vocabulário | Após normalização transitória: `status`, `situacao` e `estado` |
| Base | Pelo menos 10 observações não ausentes, todas textos físicos não vazios |
| Cardinalidade | De 2 a 12 categorias agregadas e `distinct_ratio <= 0.50` |
| Fórmulas | `formula_count = 0` é obrigatório |
| Datas | `recognized_date_count = 0` é obrigatório |
| Ambiguidade | `ambiguity_count = 0` é obrigatório |
| Conflitos | Não emitir com candidato de nome ou descrição elegível |
| Saída | `status_candidate` no campo canônico `semantic_type` |
| Confiança | `0.75` |
| Revisão humana | Pergunta bloqueante obrigatória |
| Ambiente | Exclusivamente `executable_draft`; produção permanece bloqueada |

## Privacidade e limites

O profiler poderá reter apenas `header_eligible`, contagens agregadas de presença, textos físicos, distintos, fórmulas, datas reconhecidas e ambiguidades, além da razão agregada de distintos. O cabeçalho será normalizado somente em memória para produzir o booleano de elegibilidade.

Não são autorizadas inspeção ou retenção de valores, rótulos, textos, cabeçalhos normalizados, tokens, exemplos, frequências por rótulo, posição, título de aba, formato de célula, fórmula, domínio, idioma ou hash de conteúdo. O mascaramento existente continua independente e obrigatório; a SEM-SENS-015 e `sensitivity_classifications` não poderão ser alteradas.

## Implementação condicionada

A autorização permite somente um perfil agregado imutável, classificador determinístico, registro semântico, versão contratual, integração canônica protegida por allowlist, testes unitários e de pipeline, golden dataset sintético, SHA-256, avaliador reproduzível de TP/FP/FN e gate individual de calibração.

Não estão autorizados vocabulário adicional, inferência por semântica de rótulo, sinônimos livres, aprendizado de máquina, decisão automática de processo, métrica, entidade, chave, dimensão, relacionamento, granularidade ou tratamento de dados.

## Rastreabilidade

1. `artifacts/intake/SEM-STATUS-009.json`.
2. `docs/rules/SEM_STATUS_009_POLICY_PROPOSAL_001.md`.
3. `docs/rules/SEM_STATUS_009_LOGICAL_SPEC_PROPOSAL_001.md`.
4. Aprovação explícita de Chris para a Proposta A nesta sessão.
