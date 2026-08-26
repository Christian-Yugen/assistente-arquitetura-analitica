# MDL-PARAM-011 — Gate individual de calibração draft

**Regra:** `MDL-PARAM-011@0.1.0-provisional.1`  
**Autorização de implementação:** Chris — `Chat: Ok. Autorizado continue`.  
**Perfil:** draft; sinal independente, autorizado, opaco e agregado.

O golden `MDL-PARAM-011-DRAFT-GOLDEN-001` é exclusivamente sintético, possui manifesto SHA-256 verificável e calibração limitada com `tp=1`, `fp=0` e `fn=0`. A emissão é permitida somente no teste sintético com `independent_parameter_table_signal_count=1` e sem confirmação, conflito, sinal sensível ou erro contratual.

No pipeline de workbook, `independent_parameter_table_signal_count=0` é fixado. Portanto, a regra não deriva sinais de conteúdo privado e permanece fail-closed. Ela somente consolida sinal independente em pergunta humana bloqueante; não classifica, propõe, confirma ou cria tabelas parâmetro, tabelas auxiliares, dimensões, entidades, fatos, chaves, relações, cardinalidades, atributos ou campos. **Produção não autorizada.**
