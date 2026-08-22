# SEM-LOC-011 — Gate de Reconstrução e Autorização 001

## Decisão

Chris aprovou explicitamente a Proposta A da `SEM-LOC-011` nesta sessão. Fica autorizada a reconstrução de uma implementação provisória de **Localização**, limitada ao perfil draft controlado.

## Escopo autorizado

| Elemento | Limite autorizado |
|---|---|
| Vocabulário | Após normalização transitória: exatamente `cidade`, `municipio`, `pais`, `regiao` ou `localizacao` |
| Base | Pelo menos 10 observações não ausentes, todas textos físicos não vazios |
| Cardinalidade | De 2 a 50 localidades agregadas e `distinct_ratio <= 0.90` |
| Fórmulas | `formula_count = 0` é obrigatório |
| Datas | `recognized_date_count = 0` é obrigatório |
| Ambiguidade | `ambiguity_count = 0` é obrigatório |
| Saída | `location_candidate` no campo canônico `semantic_type` |
| Confiança | `0.75` |
| Revisão humana | Pergunta bloqueante obrigatória |
| Ambiente | Implementação e eventual execução exclusivamente `executable_draft`; produção permanece bloqueada |

## Privacidade e limites

O profiler poderá reter apenas `header_eligible`, contagens agregadas de textos físicos e ambiguidades, além da base técnica. O cabeçalho será normalizado somente em memória para produzir o booleano de elegibilidade. As contagens transitórias de ausências, distintos, fórmulas e datas serão reutilizadas somente para a decisão determinística.

Não são autorizadas inspeção ou retenção de valores, rótulos, textos, cabeçalhos normalizados, tokens, exemplos, frequências por rótulo, posição, título de aba, formato de célula, fórmula, endereço, CEP, coordenada, domínio, idioma, geocodificação, consulta territorial externa ou hash de conteúdo. O mascaramento existente continua independente e obrigatório; a `SEM-SENS-015` e `sensitivity_classifications` não poderão ser alteradas.

## Implementação condicionada

A autorização permite somente um perfil agregado imutável, classificador determinístico, registro semântico, versão contratual, integração canônica protegida por catálogo, testes unitários e de pipeline, golden dataset sintético, SHA-256, avaliador reproduzível de TP/FP/FN e gate individual de calibração.

Não estão autorizados vocabulário adicional, inferência por conteúdo de rótulo, sinônimos livres, aprendizado de máquina, decisão automática de território, endereço, dimensão geográfica, relacionamento, granularidade, chave, métrica, entidade ou tratamento de dados.

## Rastreabilidade

1. `artifacts/intake/SEM-LOC-011.json`.
2. `docs/rules/SEM_LOC_011_POLICY_PROPOSAL_001.md`.
3. `docs/rules/SEM_LOC_011_LOGICAL_SPEC_PROPOSAL_001.md`.
4. Aprovação explícita de Chris para a Proposta A nesta sessão.
