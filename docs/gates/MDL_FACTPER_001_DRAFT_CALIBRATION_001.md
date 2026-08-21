# Gate de Calibração Draft — MDL-FACTPER-001

**Status:** aprovado para perfil draft.

O gate registra a calibração `CAL-MDL-FACTPER-001-001` contra o dataset `GD-MDL-FACTPER-001-001`, assinado com SHA-256 `a01ccbc91f0890588e9eeda53322cef1faa97868f350bd5ef5fe3be343237ec1`. O avaliador reproduzível reporta **1 verdadeiro positivo, 0 falsos positivos e 0 falsos negativos**.

A regra somente emite a hipótese `fact_periodic_candidate` quando há granularidade validada, no mínimo vinte linhas, dois ou mais períodos reconhecidos e uma medida numérica física elegível. A saída não contém dados brutos, cabeçalhos, posições ou períodos. A confirmação humana é obrigatória e a produção permanece bloqueada.
