# QLT-TOTALROW-010 — Especificação lógica proposta 001

**Estado:** não executável; depende da aprovação da política proposta.  
**Versão pretendida:** `0.1.0-provisional.1`.  
**Escopo:** uma aba por avaliação.

## Contrato de entrada e saída

O profiler recebe as linhas de uma aba somente em fluxo de leitura. Ao finalizar, ele retorna um objeto imutável `TotalRowsProfile` com `non_empty_row_count`, `total_row_candidate_count`, `total_row_candidate_ratio` e `normalization_basis`. O objeto não aceita, referencia ou serializa textos, números, fórmulas, índices, posições, identificadores de aba ou nomes de coluna.

O avaliador recebe um wrapper por aba contendo apenas `sheet_id` interno e o perfil agregado. Se `total_row_candidate_count` for zero, retorna lista vazia. Caso contrário, produz um finding canônico da `QLT-TOTALROW-010`, com evidência agregada e, nas severidades média e alta, uma pergunta humana sem nomear a aba.

## Algoritmo proposto

| Etapa | Operação determinística |
|---|---|
| 1 | Ignorar linha sem conteúdo pela semântica comum de ausência. |
| 2 | Manter contador de linhas não vazias já observadas, sem reter posição. |
| 3 | Quando houver ao menos três linhas anteriores, localizar a primeira célula com conteúdo. |
| 4 | Aceitar apenas quando essa célula for texto e sua normalização técnica pertencer exatamente ao vocabulário fechado. |
| 5 | Verificar a existência de ao menos um número físico em célula distinta da célula de rótulo. |
| 6 | Incrementar somente a contagem agregada de candidatas quando todas as condições forem verdadeiras. |
| 7 | Ao final, calcular `candidate_count / non_empty_row_count`, com zero para denominador zero. |

## Invariantes

O algoritmo não valida somas, não infere idioma, não converte números textuais, não interpreta fórmulas, não altera a planilha e não emite valores de célula. Uma linha rotulada como total sem número físico não é candidata. Uma linha com número físico e rótulo diferente do vocabulário fechado não é candidata. Datas nativas, booleanos e `NaN` não satisfazem o sinal complementar.

## Casos previstos para calibração

| Caso | Resultado esperado |
|---|---|
| `Total`, após três linhas de dados e com número físico adicional | Finding. |
| `Subtotal` ou `Total geral` com variação apenas de caixa e espaços | Finding. |
| Rótulo em outro idioma, antes do limiar ou sem número físico adicional | Sem finding. |
| Texto `TOTAL` com número serializado em texto | Sem finding. |
| Linha de fórmula ou valor que coincida numericamente com parcelas | Fora do escopo. |
