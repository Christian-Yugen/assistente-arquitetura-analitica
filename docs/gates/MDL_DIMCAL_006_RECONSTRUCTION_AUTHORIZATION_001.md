# MDL-DIMCAL-006 — Gate de Reconstrução 001

## Decisão

Chris aprovou a Proposta A para a hipótese conservadora de dimensão calendário.

## Escopo autorizado

Está autorizada exclusivamente a implementação draft que exige granularidade válida, base mínima de 20 linhas, coluna física de data integralmente reconhecida, datas individualmente únicas, transições diárias consecutivas e ausência de medida numérica física elegível. A saída deve usar `dimension_calendar_candidate`, confiança `0.75`, evidência agregada e confirmação humana bloqueante.

## Limites

Não está autorizada a confirmação de calendário fiscal, mensal, semanal, de feriados, de entidade temporal ou de relacionamento. A implementação não pode expor datas, valores, cabeçalhos, posições, títulos de aba, hashes ou dados sensíveis; não pode inferir pela nomenclatura da aba, formatos além dos parsers estritos já autorizados, regex ou conteúdo textual. A hipótese poderá coexistir com classificações draft concorrentes quando aplicável; sua ativação depende de testes, golden dataset, calibração, gate individual e allowlist explícita. Produção permanece bloqueada.
