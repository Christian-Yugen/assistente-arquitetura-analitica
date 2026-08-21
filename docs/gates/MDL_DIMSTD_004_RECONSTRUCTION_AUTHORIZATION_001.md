# MDL-DIMSTD-004 — Gate de Reconstrução 001

## Decisão

Chris aprovou a Proposta A para a hipótese conservadora de dimensão cadastral.

## Escopo autorizado

Está autorizada exclusivamente a implementação draft que exige granularidade válida, base mínima de 20 linhas, identificador semanticamente elegível com cobertura e unicidade individuais de 100%, atributo textual descritivo elegível e ausência de medida numérica física ou data integralmente reconhecida. A saída deve usar `dimension_standard_candidate`, confiança `0.70`, evidência agregada e confirmação humana bloqueante.

## Limites

Não está autorizada a confirmação determinística de chave de negócio, entidade, dimensão física ou relacionamento. A implementação não pode expor valores, cabeçalhos, posições, títulos de aba, hashes ou dados sensíveis; não pode inferir pela nomenclatura da aba, formato de valores, regex ou conteúdo textual. A hipótese deverá coexistir com classificações draft concorrentes quando aplicável, e a ativação exige testes, golden dataset, calibração, gate individual e allowlist explícita. Produção permanece bloqueada.
