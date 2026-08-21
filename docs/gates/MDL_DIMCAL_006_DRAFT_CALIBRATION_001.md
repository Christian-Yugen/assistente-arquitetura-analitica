# Gate de Calibração Draft — MDL-DIMCAL-006

**Status:** aprovado para perfil draft.

O gate registra a calibração `CAL-MDL-DIMCAL-006-001` contra o dataset `GD-MDL-DIMCAL-006-001`, assinado com SHA-256 `1a6c97a46322e50bf33e997b50979915d3f5e51c169c5d201dc50520f35a1fdb`. O avaliador reproduzível e a regressão automatizada registram **1 verdadeiro positivo, 0 falsos positivos e 0 falsos negativos**.

A regra somente emite a hipótese `dimension_calendar_candidate` quando há granularidade candidata, no mínimo vinte linhas, data física integralmente reconhecida, datas únicas, sequência diária contínua e ausência de medida numérica física elegível. A saída contém somente contagens agregadas privadas, sem datas, dados brutos, cabeçalhos, posições, títulos de aba ou identificadores. A confirmação humana é bloqueante; a classificação continua uma hipótese no perfil draft e a produção permanece bloqueada.
