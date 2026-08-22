# GRN-ENTITY-003 — Especificação Lógica Proposta 001

## Estado

Esta especificação é **não executável**. Ela documenta apenas a tradução lógica da Proposta A, sem criar código, perfil, classificador, registro, contrato, pipeline, testes executáveis, catálogo ou calibração. A implementação permanece condicionada à escolha explícita de Chris e ao gate de reconstrução subsequente.

## Perfil privado proposto

```text
EntityPerRowSheetProfile(
  observed_row_count: int,
  entity_header_eligible_count: int,
  explicit_key_candidate_count: int,
  descriptive_attribute_candidate_count: int,
  non_competence_date_candidate_count: int,
  event_candidate_count: int,
  measure_candidate_count: int,
  excluded_entity_marker_count: int,
  entity_marker_formula_count: int,
  ambiguity_count: int,
  basis: str
)
```

O perfil será imutável e armazenará exclusivamente contagens e booleanos agregados. A elegibilidade de cabeçalho ocorrerá de forma transitória e será reduzida a um booleano. Não serão retidos ou projetados nomes, valores, posições, identificadores de coluna, títulos de aba, pares de sinais, fórmulas, exemplos, tokens, hashes ou frequências por valor.

## Algoritmo proposto para a alternativa A

```text
entity_markers = colunas com cabeçalho fechado elegível
                 e tipo físico de texto
                 e sem sinal sensível, descritivo, data ou fórmula

descriptive_attributes = sinais já classificados como descrição,
                         categoria, localização ou status

SE observed_row_count >= 20
  E entity_header_eligible_count == 1
  E explicit_key_candidate_count == 1
  E descriptive_attribute_candidate_count >= 1
  E non_competence_date_candidate_count == 0
  E event_candidate_count == 0
  E measure_candidate_count == 0
  E excluded_entity_marker_count == 0
  E entity_marker_formula_count == 0
  E ambiguity_count == 0
ENTÃO emitir entity_per_row_candidate com confidence = 0.75
SENÃO não emitir hipótese de granularidade
```

`explicit_key_candidate_count` conta apenas hipóteses já emitidas pela `GRN-EXPL-002`; `descriptive_attribute_candidate_count`, datas, eventos e medidas contam somente sinais já classificados. A regra não reavalia coluna, cabeçalho, valores, unicidade ou fórmula, não confirma entidade de negócio, não classifica dimensão e não cria relacionamentos ou SCD.

## Fragmento canônico proposto

```json
{
  "grain_hypothesis": "entity_per_row_candidate",
  "confidence": 0.75,
  "evidence": {
    "basis": "closed_entity_marker_explicit_key_descriptive_attribute_without_event_time_measure_v1",
    "minimum_observed_row_count": 20,
    "observed_row_count": 20,
    "entity_header_eligible_count": 1,
    "explicit_key_candidate_count": 1,
    "descriptive_attribute_candidate_count": 1,
    "non_competence_date_candidate_count": 0,
    "event_candidate_count": 0,
    "measure_candidate_count": 0,
    "excluded_entity_marker_count": 0,
    "entity_marker_formula_count": 0,
    "ambiguity_count": 0
  },
  "rule_id": "GRN-ENTITY-003",
  "rule_version": "unassigned"
}
```

A pergunta vinculada será bloqueante: **“Cada linha desta aba representa uma entidade estável de cadastro, e não um evento, período, relacionamento ou medida?”** Nenhum cabeçalho, valor, identificador de coluna ou título de aba será incluído na pergunta, na evidência ou no contrato.

## Casos de teste previstos

| Caso | Resultado esperado |
|---|---|
| Marcador `Cliente`, uma chave explícita e atributo categórico em 20 linhas | Positivo. |
| Marcador `Produto`, uma chave explícita e descrição em 25 linhas | Positivo. |
| Marcador `Fornecedor`, uma chave explícita e status em 30 linhas | Positivo. |
| Marcador fora do vocabulário fechado | Negativo. |
| Apenas chave e atributo, sem marcador | Negativo na Proposta A. |
| Uma data não competência ou marcador de evento | Negativo. |
| Medida, menos de 20 linhas, fórmula, sensibilidade, descrição ou tipos divergentes | Negativo. |
| Dois marcadores, duas chaves ou ambiguidades | Negativo. |

O golden dataset futuro conterá apenas dados sintéticos e agregados, sem qualquer conteúdo pessoal. A calibração proposta para uma ativação draft exige `{"tp": 3, "fp": 0, "fn": 0}`; até então, a regra permanecerá não executável.
