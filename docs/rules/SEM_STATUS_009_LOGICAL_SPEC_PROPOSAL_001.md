# SEM-STATUS-009 — Especificação Lógica Proposta 001

## Estado

Especificação não executável. A proposta não inicia código e permanece condicionada à aprovação explícita de Chris e ao gate de reconstrução.

## Perfil privado proposto

```text
SemanticStatusProfile(
  header_eligible: bool,
  non_missing_count: int,
  physical_text_count: int,
  distinct_non_missing_count: int,
  distinct_ratio: float,
  formula_count: int,
  recognized_date_count: int,
  ambiguity_count: int,
  basis: str
)
```

O perfil será imutável e armazenará somente contagens, razão e booleanos. Valores, rótulos, cabeçalhos normalizados, textos, exemplos, frequências individuais, ordem, posições, formatos e títulos de abas deverão ser descartados imediatamente após a derivação agregada.

## Algoritmo proposto

```text
SE header_eligible
  E non_missing_count >= 10
  E physical_text_count == non_missing_count
  E 2 <= distinct_non_missing_count <= 12
  E distinct_ratio <= 0.50
  E formula_count == 0
  E recognized_date_count == 0
  E ambiguity_count == 0
  E nenhum candidato conflitante de nome ou descrição estiver elegível
ENTÃO emitir status_candidate com confidence = 0.75
SENÃO não emitir classificação
```

## Fragmento canônico proposto

```json
{
  "semantic_type": "status_candidate",
  "confidence": 0.75,
  "evidence": {
    "basis": "closed_status_headers_with_aggregate_text_cardinality_v1",
    "minimum_non_missing_count": 10,
    "physical_text_count": 10,
    "distinct_non_missing_count": 2,
    "max_distinct_count": 12,
    "max_distinct_ratio": 0.5,
    "formula_count": 0,
    "recognized_date_count": 0,
    "ambiguity_count": 0
  },
  "rule_id": "SEM-STATUS-009",
  "rule_version": "0.1.0-provisional.1"
}
```

A pergunta vinculada ao fragmento deverá ser bloqueante e solicitar confirmação humana de que a coluna representa um conjunto de estados operacionais. O contrato existente de `semantic_classifications` será reutilizado; nenhuma coleção de sensibilidade será modificada.

## Casos de teste previstos

| Caso | Resultado esperado |
|---|---|
| `Status` com 10 textos físicos e 2 categorias agregadas | Positivo |
| `Situação` com 12 textos físicos e 3 categorias agregadas | Positivo |
| `Estado` com 10 textos físicos e 5 categorias agregadas | Positivo |
| `Fase` com dados equivalentes | Negativo: vocabulário fora da lista fechada |
| `Status` com 13 categorias agregadas | Negativo: cardinalidade máxima excedida |
| `Status` com razão de distintos acima de 0,50 | Negativo |
| `Status` com fórmula, data ou tipo divergente | Negativo |
| `Status` com menos de 10 observações | Negativo |

O golden dataset conterá apenas metadados e tipos sintéticos, sem rótulos ou conteúdo pessoal. A calibração exigirá `{"tp": 3, "fp": 0, "fn": 0}` antes de qualquer autorização draft.
