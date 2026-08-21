# QLT-EMPTYROW-004 — Especificação Lógica Reconstruída

**Regra:** `QLT-EMPTYROW-004`  
**Versão candidata:** `0.1.0-reconstructed.1`  
**Perfil:** apenas draft, condicionado ao gate `QLT-EMPTYROW-004-DRAFT-CALIBRATION-001`.

## Entrada e perfil agregado

Para cada aba, o profiler lê as linhas físicas após o cabeçalho e classifica cada linha como `content` ou `empty` segundo a política reconstruída. Ele percorre a sequência para contar somente blocos `empty` que tenham pelo menos uma linha `content` em ambos os lados. O perfil não armazena células, números de linha, títulos de aba ou amostras.

| Campo agregado | Tipo | Regra |
|---|---|---|
| `empty_row_count` | inteiro não negativo | Soma das linhas vazias em blocos internos elegíveis |
| `empty_row_block_count` | inteiro não negativo | Quantidade de blocos internos elegíveis |
| `non_empty_row_count` | inteiro não negativo | Linhas não vazias consideradas para o limite de confiança |
| `empty_row_ratio` | número de 0 a 1 | `empty_row_count / (empty_row_count + non_empty_row_count)` |
| `sheet_ref` | texto anonimizado | Identificador de aba já sanitizado pelo profiler |

## Algoritmo e limiares

1. Para cada aba, percorrer linhas físicas de dados, sem incluir o cabeçalho.
2. Classificar cada célula como vazia apenas se for nula, ausente ou texto composto somente por espaços.
3. Marcar uma linha `empty` se todas as suas células forem vazias; caso contrário, marcá-la `content`.
4. Agrupar sequências contíguas de linhas `empty` e reter apenas blocos com `content` antes e depois.
5. Emitir no máximo um finding por aba quando `empty_row_count > 0`.
6. Definir severidade como baixa quando `empty_row_ratio < 0,05`, média quando a razão for de `0,05` a menos de `0,20` e alta nos demais casos; incluir pergunta de validação somente na severidade alta.
7. Calcular confiança `0,95`, reduzindo-a para `0,80` quando `non_empty_row_count == 2`.

## Fragmento canônico e limites

O adaptador canônico produz finding de escopo de aba, com métricas agregadas e recomendação determinística para revisar a continuidade da região tabular antes da modelagem. A pergunta de alta severidade solicita confirmação de que os blocos representam separadores intencionais e não lacunas de extração. O adaptador não informa número de linha, valores, nomes brutos de aba, decisão de remoção ou hipótese de chave.

## Matriz mínima de testes

| Cenário | Resultado esperado |
|---|---|
| Uma linha vazia interna em mais de 20 linhas com conteúdo | Finding de baixa severidade |
| Bloco interno que represente de 5% a menos de 20% da região | Finding de média severidade |
| Bloco interno que represente 20% ou mais da região | Finding de alta severidade e pergunta |
| Linhas vazias somente no início ou fim | Sem finding |
| Linha com `0`, `false`, data, fórmula ou texto não vazio | Não classificada como vazia |
| Payload com texto identificável | Nenhum valor bruto no perfil ou finding |

O registro no catálogo só pode ocorrer após testes unitários, golden dataset agregado com manifesto SHA-256, calibração reprodutível e gate de ativação.
