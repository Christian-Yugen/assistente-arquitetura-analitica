# Gate de Calibração Draft — MDL-DIMEXTRACT-016

**Gate:** `MDL-DIMEXTRACT-016-DRAFT-CALIBRATION-001`. **Autorização de código:** Chris, `Chat: Sim, autorizado`.

## Evidência limitada

O golden `MDL-DIMEXTRACT-016-DRAFT-GOLDEN-001` é estritamente sintético, não contém dados de workbook e é selado por manifesto SHA-256. A calibração reproduzível mede apenas o classificador determinístico: `tp=1`, `fp=0` e `fn=0`.

## Limites executáveis

O pipeline real fixa `independent_extractable_dimension_signal_count=0`; portanto, nenhum conteúdo do workbook produz finding desta regra. Só um sinal independente, autorizado, opaco e agregado, ausente no pipeline real, poderia produzir uma pergunta humana bloqueante. Confirmação humana, conflito, sensibilidade ou erro contratual suprimem o resultado de modo fail-closed.

**Produção não autorizada.** Este gate não autoriza classificar, propor, confirmar ou criar dimensões extraíveis da fato, dimensões, fatos, entidades, tabelas, chaves, relações, cardinalidades, atributos ou campos.
