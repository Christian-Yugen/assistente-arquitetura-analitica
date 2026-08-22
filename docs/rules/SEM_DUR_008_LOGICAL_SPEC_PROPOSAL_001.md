# SEM-DUR-008 — Especificação Lógica Proposta 001

## Estado

Especificação não executável. Depende da aprovação da Proposta A e não substitui o gate de reconstrução.

## Perfil privado proposto

```text
SemanticDurationProfile(
  header_eligible: bool,
  non_missing_count: int,
  physical_finite_numeric_count: int,
  formula_count: int,
  recognized_date_count: int,
  ambiguity_count: int,
  basis: str
)
```

O perfil será imutável e só poderá conter contagens e booleanos agregados. Ele não poderá carregar valores, cabeçalhos normalizados, unidade derivada, exemplos, distribuições, formatos, títulos de abas ou identificadores de células.

## Algoritmo proposto

```text
SE header_eligible
  E non_missing_count >= 10
  E physical_finite_numeric_count == non_missing_count
  E formula_count == 0
  E recognized_date_count == 0
  E ambiguity_count == 0
  E nenhum candidato conflitante de data, competência, percentual, quantidade ou moeda estiver elegível
ENTÃO emitir duration_candidate com confidence = 0.80
SENÃO não emitir classificação
```

## Fragmento canônico proposto

```json
{
  "semantic_type": "duration_candidate",
  "confidence": 0.8,
  "evidence": {
    "basis": "closed_duration_headers_with_aggregate_physical_numeric_signals",
    "minimum_non_missing_count": 10,
    "physical_finite_numeric_count": 10,
    "formula_count": 0,
    "recognized_date_count": 0,
    "ambiguity_count": 0
  },
  "rule_id": "SEM-DUR-008",
  "rule_version": "0.1.0-provisional.1"
}
```

A pergunta ligada ao fragmento deverá ser bloqueante e solicitar confirmação humana de que a coluna representa duração na unidade explicitada no cabeçalho. O contrato existente de `semantic_classifications` será reutilizado; nenhuma coleção de sensibilidade será alterada.

## Casos de teste previstos

| Caso | Resultado esperado |
|---|---|
| `Duração (horas)` e 10 números físicos | Positivo |
| `Duração` e 10 números físicos | Positivo |
| `Tempo` e 10 números físicos | Negativo: vocabulário fora da lista fechada |
| `Duração` com fórmula | Negativo |
| `Duração` com número textual | Negativo |
| `Duração` com data reconhecida | Negativo |
| `Duração` com menos de 10 observações | Negativo |
| `Duração` com candidato de quantidade elegível | Negativo por precedência |

O golden dataset conterá somente metadados e tipos sintéticos, sem conteúdo pessoal, e a calibração exigirá `{"tp": 3, "fp": 0, "fn": 0}` antes de qualquer autorização draft.
