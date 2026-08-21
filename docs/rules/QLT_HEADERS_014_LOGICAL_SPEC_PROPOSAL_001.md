# QLT-HEADERS-014 — Especificação lógica proposta 001

**Estado:** não executável; depende da autorização da política proposta.  
**Versão pretendida:** `0.1.0-provisional.1`.  
**Escopo:** uma aba por avaliação.

## Contrato de entrada e saída proposto

O profiler recebe apenas a primeira e, quando necessária para o candidato multinível, a segunda linha da aba, além de ranges mesclados. Os textos da primeira linha são normalizados somente durante a contagem de ausência e duplicidade; ranges e posições são usados apenas para contar candidatos multinível. O perfil imutável `HeadersProfile` retorna `header_column_count`, `missing_header_count`, `duplicate_normalized_group_count`, `duplicate_header_count`, `multilevel_candidate_count` e `basis`, sem aceitar ou serializar textos, títulos de abas, posições, endereços de célula, ranges, fórmulas ou valores de dados.

O avaliador recebe apenas um `sheet_id` interno não identificável e o perfil agregado. Sem sinais, retorna lista vazia. Com qualquer sinal, emite finding canônico com evidência agregada, confiança moderada e pergunta humana genérica.

## Algoritmo proposto

| Etapa | Operação determinística |
|---|---|
| 1 | Ler apenas a primeira linha materializada como cabeçalho candidato e contar suas colunas. |
| 2 | Contar ausências segundo `None`, texto vazio após `strip` ou célula do tipo fórmula. |
| 3 | Para textos não vazios, aplicar NFKC, `casefold`, remoção de acentos e colapso de espaços; contar grupos normalizados com frequência de pelo menos dois. |
| 4 | Avaliar apenas ranges mesclados horizontais iniciados na primeira linha e com largura de pelo menos duas colunas. |
| 5 | Para cada range elegível, contar como candidato multinível somente se a segunda linha tiver pelo menos duas células físicas não vazias dentro daquele intervalo. |
| 6 | Descartar textos, ranges e posições; manter apenas contagens agregadas no perfil. |
| 7 | Emitir finding se qualquer contagem de sinal for maior que zero; mapear severidade e emitir pergunta humana sem identificar a aba. |

## Invariantes

O algoritmo não procura outra linha de cabeçalho, não lê dados abaixo da segunda linha para esta regra, não revela textos, não reconhece semântica, não modifica mesclagens, não preenche cabeçalhos e não converte um candidato multinível em erro confirmado. Uma aba com cabeçalho propositalmente ausente, duplicado ou multinível exige decisão humana.

## Casos previstos para calibração

| Caso | Resultado esperado |
|---|---|
| Um cabeçalho ausente em quatro colunas | Finding de severidade média e pergunta humana. |
| Dois grupos normalizados duplicados | Finding de severidade média e pergunta humana. |
| Range mesclado horizontal na primeira linha e duas células preenchidas na segunda | Finding de severidade alta e pergunta humana. |
| Cabeçalhos únicos e presentes, range mesclado fora da primeira linha, range sem segunda linha estrutural ou texto apenas semelhante | Sem finding. |
| Perfil serializado | Não contém texto, título de aba, posição, endereço, range, fórmula ou valor bruto. |
