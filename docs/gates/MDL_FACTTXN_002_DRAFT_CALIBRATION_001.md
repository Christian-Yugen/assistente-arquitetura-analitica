# Gate de Calibração Draft — MDL-FACTTXN-002

**Status:** aprovado para perfil draft.

O gate registra a calibração `CAL-MDL-FACTTXN-002-001` contra o dataset `GD-MDL-FACTTXN-002-001`, assinado com SHA-256 `76bfe8dd518647460ae9b9f92bf3391708e42478d74e49263c1aff091734eb75`. O avaliador reproduzível reporta **1 verdadeiro positivo, 0 falsos positivos e 0 falsos negativos**.

A regra somente emite a hipótese `fact_transactional_candidate` quando há granularidade candidata, no mínimo vinte linhas, uma data reconhecida cuja razão `datas distintas / datas reconhecidas` seja maior ou igual a `0,80` e uma medida numérica física elegível. A saída contém somente métricas agregadas privadas, sem dados brutos, cabeçalhos, posições ou datas. A confirmação humana é bloqueante; a classificação continua uma hipótese no perfil draft e a produção permanece bloqueada.
