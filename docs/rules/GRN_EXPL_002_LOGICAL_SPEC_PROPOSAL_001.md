# GRN-EXPL-002 — Especificação Lógica Proposta 001

## Estado

Especificação não executável. Esta proposta não inicia código e permanece condicionada à aprovação explícita de Chris para a Proposta A e ao gate de reconstrução posterior.

## Perfil privado proposto

```text
ExplicitKeySheetProfile(
  observed_row_count: int,
  eligible_candidate_count: int,
  candidate_complete_count: int,
  candidate_unique_count: int,
  candidate_formula_count: int,
  ambiguity_count: int,
  basis: str
)
```

O perfil será imutável e armazenará somente contagens agregadas e uma base técnica. A seleção transitória de coluna poderá combinar os booleanos privados de cabeçalho elegível, identificador semântico, sensibilidade, descrição e data, mas nenhum nome, índice, valor, combinação, exemplo, posição ou título de aba será retido ou projetado.

## Algoritmo proposto

```text
candidates = colunas cuja semântica de identificador é elegível
             e cujo cabeçalho fechado é elegível
             e que não são sensíveis, descritivas ou datas

SE observed_row_count >= 20
  E eligible_candidate_count == 1
  E candidate_complete_count == 1
  E candidate_unique_count == 1
  E candidate_formula_count == 0
  E ambiguity_count == 0
ENTÃO emitir explicit_key_candidate com confidence = 0.85
SENÃO não emitir hipótese de granularidade
```

`candidate_complete_count` somente contará candidatos com cobertura total; `candidate_unique_count` somente contará candidatos cuja cardinalidade distinta é igual ao total de linhas observadas. O algoritmo não identifica a coluna, não produz chave técnica e não calcula chaves compostas.

## Fragmento canônico proposto

```json
{
  "grain_hypothesis": "explicit_key_candidate",
  "confidence": 0.85,
  "evidence": {
    "basis": "single_closed_explicit_key_with_aggregate_uniqueness_v1",
    "minimum_observed_row_count": 20,
    "observed_row_count": 20,
    "eligible_candidate_count": 1,
    "candidate_complete_count": 1,
    "candidate_unique_count": 1,
    "candidate_formula_count": 0,
    "ambiguity_count": 0
  },
  "rule_id": "GRN-EXPL-002",
  "rule_version": "0.1.0-provisional.1"
}
```

A pergunta vinculada ao fragmento deverá ser bloqueante e solicitar confirmação humana de que existe uma coluna explicitamente designada como identificador único da linha. O contrato de granularidade existente será reutilizado; nenhum cabeçalho, valor ou identificador de coluna será projetado.

## Casos de teste previstos

| Caso | Resultado esperado |
|---|---|
| Uma coluna `ID` completa e única em 20 linhas | Positivo |
| Uma coluna `Chave` completa e única em 25 linhas | Positivo |
| Uma coluna `Key` completa e única em 30 linhas | Positivo |
| Cabeçalho `Código` completo e único | Negativo: vocabulário fora da lista fechada |
| `ID` com 19 linhas | Negativo: base insuficiente |
| `ID` com ausência, duplicidade ou fórmula | Negativo |
| Duas colunas explícitas completas e únicas | Negativo: ambiguidade estrutural |
| Candidato sensível, data ou descrição | Negativo |

O golden dataset conterá somente valores sintéticos sem conteúdo pessoal e resultados agregados. A calibração exigirá `{"tp": 3, "fp": 0, "fn": 0}` antes de qualquer autorização draft.
