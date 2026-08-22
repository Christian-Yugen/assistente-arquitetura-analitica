# SEM-RESP-012 — Especificação Lógica Proposta 001

## Estado

Especificação não executável. Esta proposta não inicia código e permanece condicionada à aprovação explícita de Chris para a Proposta A e ao gate de reconstrução posterior.

## Perfil privado proposto

```text
SemanticResponsibleProfile(
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
ENTÃO emitir responsible_candidate com confidence = 0.70
SENÃO não emitir classificação
```

O algoritmo proposto não examina rótulos para validar papel, não resolve ambiguidade por conteúdo, não identifica pessoa, área ou equipe, não consulta fonte externa, não cria grupos e não infere hierarquia. O cabeçalho é avaliado uma única vez e não é projetado no diagnóstico.

## Fragmento canônico proposto

```json
{
  "semantic_type": "responsible_candidate",
  "confidence": 0.7,
  "evidence": {
    "basis": "closed_responsible_header_with_aggregate_text_cardinality_v1",
    "minimum_non_missing_count": 10,
    "physical_text_count": 10,
    "distinct_non_missing_count": 2,
    "max_distinct_count": 50,
    "max_distinct_ratio": 0.9,
    "formula_count": 0,
    "recognized_date_count": 0,
    "ambiguity_count": 0
  },
  "rule_id": "SEM-RESP-012",
  "rule_version": "0.1.0-provisional.1"
}
```

A pergunta vinculada ao fragmento deverá ser bloqueante e solicitar confirmação humana de que a coluna representa um responsável de negócio útil ao modelo, sem revelar nem presumir sua natureza pessoal. O contrato existente de `semantic_classifications` será reutilizado; nenhuma coleção de sensibilidade será modificada.

## Casos de teste previstos

| Caso | Resultado esperado |
|---|---|
| `Responsável` com 10 textos físicos e 2 responsabilidades agregadas | Positivo |
| `Responsável` com 20 textos físicos e 4 responsabilidades agregadas | Positivo |
| `Responsável` com 50 textos físicos e 25 responsabilidades agregadas | Positivo |
| `Gestor` com dados equivalentes | Negativo: vocabulário fora da lista fechada |
| `Responsáveis` com dados equivalentes | Negativo: plural não autorizado |
| `Responsável` com 51 valores distintos agregados | Negativo: cardinalidade máxima excedida |
| `Responsável` com razão de distintos acima de `0.90` | Negativo |
| `Responsável` com fórmula, data ou tipo divergente | Negativo |
| `Responsável` com menos de 10 observações | Negativo |

O golden dataset conterá somente textos sintéticos não pessoais e metadados de tipo, sem nomes, e-mails, CPFs, identificadores, equipes reais ou conteúdo pessoal. A calibração exigirá `{"tp": 3, "fp": 0, "fn": 0}` antes de qualquer autorização draft.
