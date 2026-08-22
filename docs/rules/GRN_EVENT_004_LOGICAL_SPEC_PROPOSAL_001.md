# GRN-EVENT-004 — Especificação Lógica Proposta 001

## Estado

Esta especificação é **não executável**. Ela documenta apenas a tradução lógica da Proposta A, sem criar código, perfil, classificador, registro, contrato, pipeline, testes executáveis, catálogo ou calibração. A implementação permanece condicionada à escolha explícita de Chris e ao gate de reconstrução subsequente.

## Perfil privado proposto

```text
EventPerRowSheetProfile(
  observed_row_count: int,
  event_header_eligible_count: int,
  explicit_key_candidate_count: int,
  non_competence_date_candidate_count: int,
  excluded_event_marker_count: int,
  event_marker_formula_count: int,
  ambiguity_count: int,
  basis: str
)
```

O perfil será imutável e armazenará exclusivamente contagens e booleanos agregados. A elegibilidade de cabeçalho ocorrerá de forma transitória e será reduzida a um booleano. Não serão retidos ou projetados nomes, valores, posições, identificadores de coluna, títulos de aba, pares de sinais, fórmulas, exemplos, tokens, hashes ou frequências por valor.

## Algoritmo proposto para a alternativa A

```text
event_markers = colunas com cabeçalho fechado elegível
                e tipo físico de texto
                e sem sinal sensível, descritivo, data ou fórmula

time_signals = colunas reconhecidas pela SEM-DATE-001
               e não classificadas pela SEM-COMP-002

SE observed_row_count >= 20
  E event_header_eligible_count == 1
  E excluded_event_marker_count == 0
  E event_marker_formula_count == 0
  E explicit_key_candidate_count == 1
  E non_competence_date_candidate_count == 1
  E ambiguity_count == 0
ENTÃO emitir event_per_row_candidate com confidence = 0.80
SENÃO não emitir hipótese de granularidade
```

`explicit_key_candidate_count` conta apenas hipóteses já emitidas pela `GRN-EXPL-002`, sem reavaliar a coluna ou expor sua identidade. `non_competence_date_candidate_count` conta apenas datas já reconhecidas e não classificadas como competência. O algoritmo não lê valores de negócio, não confirma evento, não classifica tabela como fato e não cria relacionamentos.

## Fragmento canônico proposto

```json
{
  "grain_hypothesis": "event_per_row_candidate",
  "confidence": 0.8,
  "evidence": {
    "basis": "closed_event_marker_explicit_key_non_competence_date_v1",
    "minimum_observed_row_count": 20,
    "observed_row_count": 20,
    "event_header_eligible_count": 1,
    "explicit_key_candidate_count": 1,
    "non_competence_date_candidate_count": 1,
    "excluded_event_marker_count": 0,
    "event_marker_formula_count": 0,
    "ambiguity_count": 0
  },
  "rule_id": "GRN-EVENT-004",
  "rule_version": "unassigned"
}
```

A pergunta vinculada será bloqueante: **“Cada linha desta aba representa um evento pontual identificável no processo de negócio?”** Nenhum cabeçalho, valor, identificador de coluna ou título de aba será incluído na pergunta, na evidência ou no contrato.

## Casos de teste previstos

| Caso | Resultado esperado |
|---|---|
| Marcador `Evento`, uma chave explícita e uma data não competência em 20 linhas | Positivo. |
| Marcador `Transação`, uma chave explícita e uma data não competência em 25 linhas | Positivo. |
| Marcador `Ocorrência`, uma chave explícita e uma data não competência em 30 linhas | Positivo. |
| Marcador fora do vocabulário fechado | Negativo. |
| Apenas chave e data, sem marcador | Negativo na Proposta A. |
| Data de competência como único sinal temporal | Negativo. |
| Menos de 20 linhas, fórmula, sensibilidade, descrição ou tipos divergentes | Negativo. |
| Dois marcadores, duas chaves ou duas datas elegíveis | Negativo por ambiguidade. |

O golden dataset futuro conterá apenas dados sintéticos e agregados, sem qualquer conteúdo pessoal. A calibração proposta para uma ativação draft exige `{"tp": 3, "fp": 0, "fn": 0}`; até então, a regra permanecerá não executável.
