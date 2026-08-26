# GRN-PREAGG-008 — Gate individual de calibração draft

**Decisão:** aprovada exclusivamente para **draft controlado**.
**Autorização de implementação:** Chris — “autorizado”.

O golden `GRN-PREAGG-008-DRAFT-GOLDEN-001` é estritamente sintético e possui SHA-256 `ddd8fb907d161beccd7b1be4da10ea7472759418b1d2a8346b238803d20623cc`. A calibração determinística registra `tp=1`, `fp=0` e `fn=0`; ela não constitui calibração produtiva.

O pipeline real fixa `independent_pre_aggregation_signal_count=0`, não deriva sinal de workbook e permanece fail-closed. A regra não calcula, soma, conta, compara, recomputa, seleciona ou desagrega métricas, medidas, níveis de detalhe, entidades, eventos, chaves, fatos, dimensões, relações, cardinalidades, campos, valores, frequências ou conteúdo privado. **Produção permanece bloqueada.**

