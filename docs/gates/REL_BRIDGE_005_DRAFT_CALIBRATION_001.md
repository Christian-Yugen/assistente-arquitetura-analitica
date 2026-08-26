# Gate de Calibração Draft — REL-BRIDGE-005

**Gate:** `REL-BRIDGE-005-DRAFT-CALIBRATION-001`. **Perfil:** draft. **Produção:** não autorizada.

O golden `REL-BRIDGE-005-DRAFT-GOLDEN-001` é estritamente sintético, não contém dados de workbook e é selado por manifesto SHA-256. A calibração reproduzível mede apenas o classificador determinístico: `tp=1`, `fp=0` e `fn=0`.

O pipeline real fixa `independent_bridge_need_signal_count=0`; portanto, nenhum conteúdo do workbook produz finding desta regra. Só um sinal independente, autorizado, opaco e agregado, ausente no pipeline real, poderia produzir uma pergunta humana bloqueante. Confirmação humana, conflito, sensibilidade ou erro contratual suprimem o resultado de modo fail-closed.

Este gate não detecta, recomenda, classifica, propõe, confirma ou cria necessidade de ponte, tabelas ponte, pontes, relacionamentos, dimensões, fatos, entidades, tabelas, chaves, atributos, relações, cardinalidades, granularidade, período, métrica, campo, valor, frequência, pares ou conteúdo privado. **Produção permanece bloqueada.**
