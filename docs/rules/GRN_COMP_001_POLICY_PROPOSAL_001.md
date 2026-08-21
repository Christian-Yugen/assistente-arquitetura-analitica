# GRN-COMP-001 — Proposta de Política 001

**Regra:** `GRN-COMP-001` — Chave composta  
**Estado:** proposta não executável; implementação bloqueada.  
**Fonte recuperada:** blueprint oficial: P0, `grain_inference`, escopo por aba, dependência de `semantic_typing`, saída `grain`.

## Lacuna da fonte

O catálogo oficial não materializa a condição de uma chave composta, os limites, a evidência nem o modelo de saída. Portanto, esta proposta não alega reconstruir uma definição canônica; ela estabelece uma alternativa draft conservadora, sujeita a autorização específica de Chris.

## Proposta A — candidato de chave composta com confirmação humana

A regra só poderá produzir uma **hipótese de granularidade**, nunca declarar uma chave de negócio nem alterar dados. A avaliação ficará limitada a pares de colunas previamente elegíveis pela tipagem semântica e ocorrerá somente quando houver pelo menos **20 linhas observadas**. Um par será candidato apenas se: ambas as colunas estiverem completas no conjunto avaliado; nenhuma delas for individualmente única; e a combinação das duas for única em 100% das linhas observadas.

Para evitar explosão combinatória, a análise deverá considerar no máximo **10 pares** por aba e excluir colunas sensíveis, campos livres, fórmulas, datas, métricas e candidatos cuja elegibilidade semântica não seja comprovada. O perfil poderá reter exclusivamente contagens agregadas: total observado, completude do par, cardinalidade individual, cardinalidade conjunta, razão de unicidade conjunta e total de pares examinados. Valores, pares, hashes, cabeçalhos, posições e títulos de abas permanecem proibidos.

Quando satisfeita, a saída proposta será uma hipótese `composite_key_candidate` associada à aba, com confiança de **0,70** e pergunta humana obrigatória: “Este par representa o identificador único da linha para esta aba?”. A resposta humana deverá governar qualquer promoção posterior da granularidade. Sem resposta, a hipótese não é uma chave confirmada e não habilita regras de relacionamento.

| Aspecto | Decisão proposta |
|---|---|
| Mínimo de linhas | 20 linhas observadas |
| Cobertura | 100% de completude em ambos os componentes |
| Unicidade individual | Nenhum componente pode ser único sozinho |
| Unicidade conjunta | 100% das combinações observadas |
| Escopo | Aba; no máximo 10 pares elegíveis |
| Saída | Hipótese de granularidade, não chave confirmada |
| Confiança | 0,70, condicionada a validação humana |

## Alternativa B — não inferir automaticamente

Alternativamente, a GRN-COMP-001 pode apenas apresentar uma pergunta guiada quando existirem duas colunas identificadoras incompletas ou não únicas, sem calcular unicidade conjunta. Essa opção reduz a inferência, mas limita a utilidade do motor na identificação de granularidade.

## Controle de ativação

Nenhuma alternativa autoriza código, registro, alteração de contrato ou execução. Após escolha explícita de Chris, o próximo passo será criar o gate de reconstrução e somente então detalhar profile, avaliador, testes, golden dataset e calibração.
