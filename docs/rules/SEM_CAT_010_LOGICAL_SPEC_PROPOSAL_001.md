# SEM-CAT-010 — Especificação Lógica Proposta 001

## Estado

Especificação não executável. Esta proposta não inicia código e permanece condicionada à aprovação explícita de Chris para a Proposta A e ao gate de reconstrução posterior.

## Perfil privado proposto

```text
SemanticCategoryProfile(
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

O perfil será imutável e armazenará somente booleanos, contagens e razão. Valores, rótulos, cabeçalhos normalizados, textos, exemplos, frequências individuais, ordem, posições, formatos e títulos de abas deverão ser descartados imediatamente após a derivação agregada.

## Algoritmo proposto

```text
SE header_eligible
  E non_missing_count >= 10
  E physical_text_count == non_missing_count
  E 2 <= distinct_non_missing_count <= 20
  E distinct_ratio <= 0.50
  E formula_count == 0
  E recognized_date_count == 0
  E ambiguity_count == 0
ENTÃO emitir category_candidate com confidence = 0.70
SENÃO não emitir classificação
```

O algoritmo proposto não examina rótulos para validar domínio, não cria grupos, não infere hierarquia, não interpreta códigos e não aplica normalização de valores além da contagem agregada de distintos. O cabeçalho é avaliado uma única vez e não é projetado no diagnóstico.

## Fragmento canônico proposto

```json
{
  "semantic_type": "category_candidate",
  "confidence": 0.7,
  "evidence": {
    "basis": "closed_category_header_with_aggregate_text_cardinality_v1",
    "minimum_non_missing_count": 10,
    "physical_text_count": 10,
    "distinct_non_missing_count": 2,
    "max_distinct_count": 20,
    "max_distinct_ratio": 0.5,
    "formula_count": 0,
    "recognized_date_count": 0,
    "ambiguity_count": 0
  },
  "rule_id": "SEM-CAT-010",
  "rule_version": "0.1.0-provisional.1"
}
```

A pergunta vinculada ao fragmento deverá ser bloqueante e solicitar confirmação humana de que a coluna representa uma categorização de negócio apropriada. O contrato existente de `semantic_classifications` será reutilizado; nenhuma coleção de sensibilidade será modificada.

## Casos de teste previstos

| Caso | Resultado esperado |
|---|---|
| `Categoria` com 10 textos físicos e 2 categorias agregadas | Positivo |
| `Categoria` com 20 textos físicos e 4 categorias agregadas | Positivo |
| `Categoria` com 24 textos físicos e 12 categorias agregadas | Positivo |
| `Grupo` com dados equivalentes | Negativo: vocabulário fora da lista fechada |
| `Categoria` com 21 categorias agregadas | Negativo: cardinalidade máxima excedida |
| `Categoria` com razão de distintos acima de `0.50` | Negativo |
| `Categoria` com fórmula, data ou tipo divergente | Negativo |
| `Categoria` com menos de 10 observações | Negativo |

O golden dataset conterá apenas metadados e tipos sintéticos, sem rótulos ou conteúdo pessoal. A calibração exigirá `{"tp": 3, "fp": 0, "fn": 0}` antes de qualquer autorização draft.
