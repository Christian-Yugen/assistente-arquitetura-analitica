# SEM-LOC-011 — Especificação Lógica Proposta 001

## Estado

Especificação não executável. Esta proposta não inicia código e permanece condicionada à aprovação explícita de Chris para a Proposta A e ao gate de reconstrução posterior.

## Perfil privado proposto

```text
SemanticLocationProfile(
  header_eligible: bool,
  physical_text_count: int,
  ambiguity_count: int,
  basis: str
)
```

O classificador proposto combinará esse perfil apenas com as contagens já agregadas e transitórias de tipo físico, ausências, distintos, fórmulas e datas. O perfil será imutável e não armazenará valores, rótulos, cabeçalhos normalizados, textos, exemplos, frequências individuais, ordem, posições, formatos ou títulos de abas.

## Algoritmo proposto

```text
SE header_eligible
  E non_missing_count >= 10
  E physical_text_count == non_missing_count
  E 2 <= distinct_non_missing_count <= 50
  E distinct_ratio <= 0.90
  E formula_count == 0
  E recognized_date_count == 0
  E ambiguity_count == 0
ENTÃO emitir location_candidate com confidence = 0.75
SENÃO não emitir classificação
```

O algoritmo proposto não examina rótulos para validar território, não resolve ambiguidade por conteúdo, não consulta fonte externa, não interpreta códigos, não cria grupos e não infere hierarquia. O cabeçalho é avaliado uma única vez e não é projetado no diagnóstico.

## Fragmento canônico proposto

```json
{
  "semantic_type": "location_candidate",
  "confidence": 0.75,
  "evidence": {
    "basis": "closed_location_header_with_aggregate_text_cardinality_v1",
    "minimum_non_missing_count": 10,
    "physical_text_count": 10,
    "distinct_non_missing_count": 2,
    "max_distinct_count": 50,
    "max_distinct_ratio": 0.9,
    "formula_count": 0,
    "recognized_date_count": 0,
    "ambiguity_count": 0
  },
  "rule_id": "SEM-LOC-011",
  "rule_version": "0.1.0-provisional.1"
}
```

A pergunta vinculada ao fragmento deverá ser bloqueante e solicitar confirmação humana de que a coluna representa uma localização de negócio útil ao modelo. O contrato existente de `semantic_classifications` será reutilizado; nenhuma coleção de sensibilidade será modificada.

## Casos de teste previstos

| Caso | Resultado esperado |
|---|---|
| `Cidade` com 10 textos físicos e 2 localidades agregadas | Positivo |
| `Município` com 20 textos físicos e 4 localidades agregadas | Positivo |
| `Região` com 50 textos físicos e 25 localidades agregadas | Positivo |
| `Estado` com dados equivalentes | Negativo: vocabulário ambiguamente reservado |
| `Endereço` com dados equivalentes | Negativo: escopo não autorizado |
| `Cidade` com 51 localidades agregadas | Negativo: cardinalidade máxima excedida |
| `Cidade` com razão de distintos acima de `0.90` | Negativo |
| `Cidade` com fórmula, data ou tipo divergente | Negativo |
| `Cidade` com menos de 10 observações | Negativo |

O golden dataset conterá somente metadados e tipos sintéticos, sem rótulos territoriais reais, endereços, CEPs, coordenadas ou conteúdo pessoal. A calibração exigirá `{"tp": 3, "fp": 0, "fn": 0}` antes de qualquer autorização draft.
