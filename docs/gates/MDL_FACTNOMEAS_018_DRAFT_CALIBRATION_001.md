# Gate de Calibração Draft — MDL-FACTNOMEAS-018

**Gate:** `MDL-FACTNOMEAS-018-DRAFT-CALIBRATION-001`. **Perfil:** draft. **Produção:** não autorizada.

O golden `MDL-FACTNOMEAS-018-DRAFT-GOLDEN-001` é estritamente sintético, não contém dados de workbook e é selado por manifesto SHA-256. A calibração reproduzível mede apenas o classificador determinístico: `tp=1`, `fp=0` e `fn=0`.

O pipeline real fixa `independent_fact_without_measures_signal_count=0`; portanto, nenhum conteúdo do workbook produz finding desta regra. Só um sinal independente, autorizado, opaco e agregado, ausente no pipeline real, poderia produzir uma pergunta humana bloqueante. Confirmação humana, conflito, sensibilidade ou erro contratual suprimem o resultado de modo fail-closed.

Este gate não classifica, propõe, confirma ou cria fato sem medidas, fato, dimensão, entidade, tabela, chave, atributo, relação, cardinalidade, granularidade, período, métrica, campo, valor, frequência, par ou conteúdo privado. **Produção permanece bloqueada.**
