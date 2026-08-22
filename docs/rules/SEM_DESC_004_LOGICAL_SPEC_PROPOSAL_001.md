# SEM-DESC-004 — Especificação Lógica Proposta A 001

## Status

Este documento é não executável. Ele detalha a Proposta A para apreciação de Chris e não cria módulo, registro, contrato, pipeline, teste executável, dataset, autorização de catálogo ou promoção de ambiente.

## Perfil privado previsto

O futuro `SemanticDescriptionProfile` deverá armazenar exclusivamente os campos abaixo, todos derivados em memória e imutáveis.

| Campo | Tipo | Origem permitida |
|---|---|---|
| `header_eligible` | booleano | Comparação transitória do cabeçalho normalizado com vocabulário fechado |
| `non_missing_count` | inteiro | Contagem agregada de observações não ausentes |
| `physical_text_count` | inteiro | Contagem por tipo físico textual, sem reter texto |
| `physical_numeric_or_date_count` | inteiro | Contagem por tipo físico não textual, sem reter valor |
| `formula_count` | inteiro | Contagem agregada de fórmulas |
| `recognized_date_count` | inteiro | Contagem agregada do perfil temporal existente |
| `distinct_non_missing_count` | inteiro | Contagem agregada já disponível no perfil de identificador |
| `distinct_ratio` | número | Razão agregada já disponível no perfil de identificador |

O profiler descartará acumuladores após a finalização. Ele não poderá expor valores, cabeçalhos normalizados, tokens, assinaturas, comprimentos individuais, posições, títulos de abas, hashes de conteúdo ou amostras.

## Predicado determinístico

```text
eligible :=
  header_eligible
  AND non_missing_count >= 10
  AND physical_text_count = non_missing_count
  AND physical_numeric_or_date_count = 0
  AND formula_count = 0
  AND recognized_date_count = 0
  AND distinct_non_missing_count >= 2
  AND distinct_ratio >= 0.20
```

Quando `eligible` for verdadeiro, o classificador produzirá exatamente um candidato `name_or_description_candidate` com confiança `0.70`. Caso contrário, retornará lista vazia. A implementação não poderá introduzir pontuação, heurística probabilística, aprendizado de máquina, vocabulário adicional, fallback por valor ou inferência contextual.

## Fragmento canônico esperado

O futuro adaptador deverá usar a projeção semântica canônica existente e incluir somente `semantic_type`, `confidence`, `rule_id`, `rule_version`, `affected_entities` e evidência agregada. A pergunta humana bloqueante será vinculada ao candidato pelo mecanismo canônico de perguntas. A SEM-SENS-015 continuará na coleção segregada `sensitivity_classifications`; esta regra não pode gravar, alterar ou duplicar a sua saída.

## Matriz mínima de aceitação futura

| Cenário sintético | Resultado esperado |
|---|---|
| `Nome` com 10 textos distintos | candidato e classificação de sensibilidade independente |
| `Descrição` com 10 textos e razão distinta ≥ 0,20 | candidato |
| `Descricao` com valores textuais repetidos, razão distinta ≥ 0,20 | candidato |
| Cabeçalho fora da lista | vazio |
| Nove textos | vazio |
| Uma fórmula | vazio |
| Número, data ou booleano físico | vazio |
| Data textual reconhecida | vazio |
| Uma única descrição repetida | vazio |
| Serialização do diagnóstico | não contém cabeçalho ou qualquer valor de entrada |

## Condição de progresso

O único próximo passo permitido é a aprovação explícita de Chris para esta Proposta A. Após isso, deverá existir um gate de reconstrução separado que replique estes limites antes da implementação exclusiva no perfil draft.
