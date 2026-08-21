# QLT-NEGATIVE-011 — Especificação lógica proposta 001

**Estado:** não executável; depende da autorização da política proposta.  
**Versão pretendida:** `0.1.0-provisional.1`.  
**Escopo:** uma coluna por avaliação.

## Contrato de entrada e saída proposto

O profiler recebe a sequência de células e o cabeçalho da coluna em fluxo de leitura. O cabeçalho é normalizado somente durante a classificação de elegibilidade e é descartado antes da criação do perfil. Ao final, retorna um objeto imutável `NegativeValuesProfile` contendo `physical_numeric_count`, `negative_physical_count`, `negative_physical_ratio`, `header_eligible` e `basis`. O perfil não aceita, referencia ou serializa valores, cabeçalhos, posições, amostras, títulos de aba, fórmulas ou identificadores brutos.

O avaliador recebe apenas um `column_id` interno não identificável e o perfil agregado. Se a coluna não for elegível, tiver menos de 10 números físicos ou não tiver negativos, retorna lista vazia. Caso contrário, produz um finding canônico da `QLT-NEGATIVE-011` com evidência agregada, confiança moderada e uma pergunta de validação humana genérica.

## Algoritmo proposto

| Etapa | Operação determinística |
|---|---|
| 1 | Normalizar transitoriamente o cabeçalho por NFKC, `casefold`, remoção de acentos e colapso de espaços. |
| 2 | Marcar a coluna como elegível somente quando o resultado pertencer ao vocabulário fechado aprovado. |
| 3 | Percorrer células sem reter valores ou posições; ignorar vazios, booleanos, datas, erros, números textuais, fórmulas e números não finitos. |
| 4 | Contar os números físicos finitos e, dentre eles, os estritamente menores que zero. |
| 5 | Calcular a razão `negative_physical_count / physical_numeric_count`, com zero quando o denominador for zero. |
| 6 | Emitir finding somente quando a coluna for elegível, a base for de pelo menos 10 números físicos e a contagem negativa for maior que zero. |
| 7 | Mapear a razão para severidade e emitir a pergunta humana sem revelar o cabeçalho ou valores. |

## Invariantes

O algoritmo não deduz regras de negócio, não compara colunas, não calcula saldo, não interpreta fórmulas, não converte tipos, não usa um modelo estatístico, não transmite cabeçalhos nem valores e não modifica a planilha. Uma coluna de moeda, saldo, preço ou resultado não é elegível por esta proposta, mesmo que todos os seus valores sejam negativos.

## Casos previstos para calibração

| Caso | Resultado esperado |
|---|---|
| `quantidade` com 20 números físicos e um negativo | Finding de severidade baixa e pergunta humana. |
| `estoque` com 20 números físicos e quatro negativos | Finding de severidade média e pergunta humana. |
| `volume` com 10 números físicos e três negativos | Finding de severidade alta e pergunta humana. |
| `saldo` ou `valor` com números negativos | Sem finding. |
| Cabeçalho não elegível, menos de 10 números físicos, número negativo em texto, fórmula, data, booleano ou `NaN` | Sem finding. |
| Perfil serializado | Não contém cabeçalho, valores, posições, exemplos nem título de aba. |
