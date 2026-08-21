# QLT-IDMISS-015 — Especificação lógica proposta 001

**Estado:** não executável; depende da autorização da política proposta.  
**Versão pretendida:** `0.1.0-provisional.1`.  
**Escopo:** uma coluna por avaliação.

## Contrato de entrada e saída proposto

O profiler recebe o cabeçalho e as células de uma coluna. O cabeçalho é normalizado somente durante a classificação de elegibilidade e é descartado. Para cada valor não ausente suportado, o profiler constrói uma impressão digital tipada, usada apenas enquanto a contagem de frequências é acumulada e descartada no `finalize`. O perfil imutável `IdentifierCompletenessProfile` retorna `header_eligible`, `observed_cell_count`, `missing_cell_count`, `non_missing_cell_count`, `duplicate_group_count`, `duplicate_occurrence_count`, `missing_ratio`, `duplicate_ratio` e `basis`; não retorna valores, impressões digitais, hashes, cabeçalhos, posições, exemplos ou títulos de aba.

O avaliador recebe apenas um `column_id` interno não identificável e o perfil agregado. Colunas não elegíveis, bases abaixo de 10 e perfis sem ausência ou duplicidade retornam lista vazia. Caso contrário, o avaliador gera finding canônico com evidência agregada, confiança moderada e pergunta humana genérica.

## Algoritmo proposto

| Etapa | Operação determinística |
|---|---|
| 1 | Normalizar transitoriamente o cabeçalho por NFKC, `casefold`, remoção de acentos e colapso de espaços; verificar vocabulário fechado. |
| 2 | Percorrer os valores e aplicar a mesma classificação privada de ausência da QLT-NULL-001. |
| 3 | Para valores não ausentes, aceitar somente tipos físicos suportados; produzir impressão digital tipada transitória. Textos recebem NFKC somente, sem `trim` ou `casefold`. |
| 4 | Contar frequências transitórias e, ao finalizar, calcular grupos com frequência de pelo menos dois e todas as suas ocorrências. |
| 5 | Descartar as impressões digitais e seus contadores antes de expor o perfil; manter exclusivamente as contagens e razões agregadas. |
| 6 | Exigir cabeçalho elegível e pelo menos 10 observações; emitir finding somente quando houver ausência ou ocorrência duplicada. |
| 7 | Mapear a maior razão agregada para severidade e emitir pergunta humana sem revelar o campo ou seus valores. |

## Invariantes

O algoritmo não persiste cabeçalho, identificador, valor, hash, impressão digital, exemplo, posição ou título de aba. Ele não faz inferência de chave, não monta chave composta, não normaliza valores para tentar encontrar equivalência, não valida formato, não consulta sistemas externos e não modifica a planilha. Textos `ABC`, `abc`, `ABC ` e `ABC` são comparados conforme sua representação exata após NFKC, pois a regra não pode presumir que caixa ou espaço não seja significativo para a organização.

## Casos previstos para calibração

| Caso | Resultado esperado |
|---|---|
| `id` com 20 observações e uma ausência | Finding de severidade baixa e pergunta humana. |
| `codigo` com 20 observações e duas ocorrências do mesmo texto exato | Finding de severidade média e pergunta humana. |
| `cpf` com 10 observações e três ausências ou duplicidades | Finding de severidade alta e pergunta humana. |
| Cabeçalho não elegível, nove observações, valores apenas únicos, diferenças somente de caixa ou espaço, fórmula, número textual ou formato potencialmente inválido | Sem finding. |
| Perfil serializado | Não contém cabeçalho, identificador, valor, hash, impressão digital, posição, exemplo ou título de aba. |
