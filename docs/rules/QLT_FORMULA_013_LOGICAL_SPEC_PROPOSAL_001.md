# QLT-FORMULA-013 — Especificação lógica proposta 001

**Estado:** não executável; depende da autorização da política proposta.  
**Versão pretendida:** `0.1.0-provisional.1`.  
**Escopo:** uma coluna por avaliação.

## Contrato de entrada e saída proposto

O profiler deverá percorrer as células de uma coluna no modo de fórmula (`data_only=False`) e classificar cada uma somente por dois atributos transitórios: vazia ou não vazia, e `data_type == "f"` ou não. A expressão, referências e valores calculados não devem ser copiados para acumuladores, perfis, logs, evidências ou findings. Ao final, retornará um `FormulaConsistencyProfile` imutável com `physical_nonempty_count`, `formula_count`, `nonformula_count`, `nonformula_ratio`, `eligible` e `basis`.

O avaliador recebe apenas um `column_id` interno não identificável e o perfil agregado. Quando a coluna não for elegível ou não houver não fórmulas, retorna lista vazia. Caso contrário, produz finding canônico com evidência agregada, confiança moderada e pergunta humana genérica.

## Algoritmo proposto

| Etapa | Operação determinística |
|---|---|
| 1 | Percorrer as células sem `values_only`; ler de forma transitória somente presença e `data_type`. |
| 2 | Incrementar a base apenas para células físicas não vazias; marcar fórmula somente quando `data_type == "f"`. |
| 3 | Calcular `formula_ratio = formula_count / physical_nonempty_count`, com zero quando a base for zero. |
| 4 | Marcar elegível somente com pelo menos 10 células físicas não vazias, 8 fórmulas e razão de fórmulas de pelo menos 80%. |
| 5 | Calcular `nonformula_count = physical_nonempty_count − formula_count`; emitir finding somente se elegível e a contagem for maior que zero. |
| 6 | Mapear a razão de não fórmulas para severidade e emitir pergunta humana sem revelar fórmula, valor, célula, linha ou coluna. |

## Invariantes

O algoritmo não lê nem normaliza expressões de fórmula, não avalia referências, não compara fórmulas entre si, não abre vínculos externos, não recalcula workbook, não acessa valores em cache e não altera a planilha. Ele não detecta uma fórmula matematicamente diferente de outra; detecta somente uma ruptura de presença versus ausência dentro de uma coluna predominantemente calculada.

## Casos previstos para calibração

| Caso | Resultado esperado |
|---|---|
| 20 células físicas, 19 fórmulas e um valor manual | Finding de severidade baixa e pergunta humana. |
| 20 células físicas, 18 fórmulas e dois valores manuais | Finding de severidade média e pergunta humana. |
| 20 células físicas, 16 fórmulas e quatro valores manuais | Finding de severidade alta e pergunta humana. |
| Coluna sem valores manuais, 7 fórmulas, 79% de fórmulas ou células vazias adicionais | Sem finding. |
| Perfil serializado | Não contém expressão, referência, valor calculado, cabeçalho, posição, exemplo ou título de aba. |
