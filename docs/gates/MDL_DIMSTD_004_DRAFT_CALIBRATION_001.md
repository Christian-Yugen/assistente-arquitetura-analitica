# Gate de Calibração Draft — MDL-DIMSTD-004

**Status:** aprovado para perfil draft.

O gate registra a calibração `CAL-MDL-DIMSTD-004-001` contra o dataset `GD-MDL-DIMSTD-004-001`, assinado com SHA-256 `f55ed6831c0143d7091f65129f8fa7ba1915182ae4bf1cb3c5953841a154fba3`. O avaliador reproduzível e a regressão automatizada registram **1 verdadeiro positivo, 0 falsos positivos e 0 falsos negativos**.

A regra somente emite a hipótese `dimension_standard_candidate` quando há granularidade candidata, no mínimo vinte linhas, identificador individualmente único, atributo textual descritivo elegível e ausência de medida numérica física ou data integralmente reconhecida. A saída contém somente contagens agregadas privadas, sem dados brutos, cabeçalhos, posições, títulos de aba ou identificadores. A confirmação humana é bloqueante; a classificação continua uma hipótese no perfil draft e a produção permanece bloqueada.
