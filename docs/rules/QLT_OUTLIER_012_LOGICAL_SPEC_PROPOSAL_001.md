# QLT-OUTLIER-012 — Especificação lógica proposta 001

**Estado:** não executável; depende da autorização da política proposta.  
**Versão pretendida:** `0.1.0-provisional.1`.  
**Escopo:** uma coluna por avaliação.

## Contrato de entrada e saída proposto

O profiler recebe células de uma coluna em fluxo de leitura. Durante esse fluxo, conta células físicas não vazias, identifica números físicos finitos não booleanos, ordena somente o conjunto numérico transitoriamente, calcula quartis lineares e descarta os valores antes de retornar. O objeto imutável `OutlierProfile` preserva apenas `physical_nonempty_count`, `physical_numeric_count`, `lower_outlier_count`, `upper_outlier_count`, `outlier_count`, `outlier_ratio`, `basis` e `eligible`; não aceita nem serializa valores, quartis, cercas, cabeçalho, posições, exemplos, fórmulas ou títulos de aba.

O avaliador recebe somente um `column_id` interno não identificável e o perfil agregado. Quando não houver elegibilidade ou candidatos, retorna lista vazia. Caso contrário, emite finding canônico com evidências agregadas, confiança moderada e pergunta de validação humana genérica.

## Algoritmo proposto

| Etapa | Operação determinística |
|---|---|
| 1 | Percorrer células e contar entradas físicas não vazias, excluindo vazios, booleanos, datas, fórmulas, erros, números em texto e valores não finitos da base numérica. |
| 2 | Exigir pelo menos 20 números físicos finitos e participação numérica de pelo menos 80%. |
| 3 | Ordenar transitoriamente os números físicos e calcular `Q1` e `Q3` com interpolação linear, em posições `0,25 × (n − 1)` e `0,75 × (n − 1)`. |
| 4 | Calcular `IQR = Q3 − Q1`; se `IQR = 0`, encerrar sem finding. |
| 5 | Calcular cercas `Q1 − 1,5 × IQR` e `Q3 + 1,5 × IQR`; contar candidatos estritamente fora das cercas. |
| 6 | Descartar valores, quartis e cercas; manter apenas as contagens e razão agregadas no perfil. |
| 7 | Emitir finding somente quando a coluna for elegível e a contagem de candidatos for maior que zero. |

## Invariantes

O algoritmo não expõe valores, limites estatísticos, posições ou cabeçalhos; não faz correção automática; não troca de método quando o IQR for zero; não aplica z-score, MAD, aprendizado de máquina, segmentação, agrupamento ou inferência de domínio. A referência a “atípico” fica limitada ao método descrito, sem atribuição de causa ou erro de negócio.

## Casos previstos para calibração

| Caso | Resultado esperado |
|---|---|
| 20 números físicos com um candidato superior fora da cerca | Finding de severidade baixa e pergunta humana. |
| 20 números físicos com dois candidatos inferiores e dois superiores | Finding de severidade média e pergunta humana. |
| 20 números físicos com cinco candidatos fora das cercas | Finding de severidade alta e pergunta humana. |
| Base sem candidatos, `IQR = 0`, 19 números físicos ou participação numérica inferior a 80% | Sem finding. |
| Número em texto, fórmula, data, booleano, erro, `NaN` ou infinito | Excluído da base e sem vazamento no perfil. |
| Perfil serializado | Não contém valores, quartis, cercas, cabeçalho, posições, exemplos ou título de aba. |
