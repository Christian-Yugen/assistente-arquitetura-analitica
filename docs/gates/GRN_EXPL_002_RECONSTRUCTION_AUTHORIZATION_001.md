# GRN-EXPL-002 — Gate de Reconstrução e Autorização 001

## Decisão

Chris aprovou explicitamente a Proposta A da `GRN-EXPL-002` nesta sessão. Fica autorizada a reconstrução de uma implementação provisória de **Chave explícita**, limitada ao perfil draft controlado.

## Escopo autorizado

| Elemento | Limite autorizado |
|---|---|
| Vocabulário | Após normalização transitória: exatamente `id`, `chave` ou `key` |
| Base | Pelo menos 20 linhas observadas na aba |
| Elegibilidade | Exatamente uma coluna semanticamente identificadora, não sensível, não descritiva e não temporal |
| Completude | Cobertura total no conjunto de linhas observadas |
| Unicidade | Cardinalidade distinta igual ao conjunto de linhas observadas |
| Fórmulas | Zero fórmulas na coluna candidata |
| Ambiguidade | Exatamente um candidato; zero ou dois ou mais bloqueiam a saída |
| Saída | Hipótese de granularidade `explicit_key_candidate` |
| Confiança | `0.85` |
| Revisão humana | Pergunta bloqueante obrigatória |
| Ambiente | Implementação e eventual execução exclusivamente `executable_draft`; produção permanece bloqueada |

## Privacidade e limites

O profiler poderá reter apenas contagens agregadas de linhas, candidatos elegíveis, candidatos completos, candidatos únicos, fórmulas e ambiguidades, além da base técnica. A elegibilidade de cabeçalho e as classificações de apoio serão avaliadas somente em memória, sem projetar ou reter cabeçalho, índice, valores, rótulos, exemplos, posições, títulos de abas, tokens, fórmulas ou hashes de conteúdo.

Não são autorizadas inspeção ou retenção de dados de coluna, criação de chave técnica, confirmação de chave primária, inferência de relacionamento, inferência de chave composta, decisão de modelo ou tratamento de dados. O mascaramento existente continua independente e obrigatório; a `SEM-SENS-015` e `sensitivity_classifications` não poderão ser alteradas.

## Implementação condicionada

A autorização permite somente um perfil agregado imutável, classificador determinístico, registro de granularidade, versão contratual, integração canônica protegida por catálogo, testes unitários e de pipeline, golden dataset sintético, SHA-256, avaliador reproduzível de TP/FP/FN e gate individual de calibração.

Não estão autorizados vocabulário adicional, sinônimos livres, inferência por conteúdo, aprendizado de máquina, combinação de colunas, decisão automática de chave de negócio, relação, granularidade, dimensão, fato, métrica ou entidade.

## Rastreabilidade

1. `artifacts/intake/GRN-EXPL-002.json`.
2. `docs/rules/GRN_EXPL_002_POLICY_PROPOSAL_001.md`.
3. `docs/rules/GRN_EXPL_002_LOGICAL_SPEC_PROPOSAL_001.md`.
4. Aprovação explícita de Chris para a Proposta A nesta sessão.
