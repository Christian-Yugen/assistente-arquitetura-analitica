# GRN-ASSOC-007 — Gate individual de calibração draft

**Decisão:** aprovada exclusivamente para **draft controlado**.
**Autorização de implementação:** Chris — “autorizado”.

O golden `GRN-ASSOC-007-DRAFT-GOLDEN-001` é estritamente sintético e possui SHA-256 `5e1350b9239a9ff8947f487e59d8e8818c78a4737d8276043035c0d8b6ec928f`. A calibração determinística registra `tp=1`, `fp=0` e `fn=0`; ela não constitui calibração produtiva.

A regra somente consolida sinal independente, opaco e agregado. O pipeline real fixa `independent_association_signal_count=0`; assim, não deriva sinal de workbook e permanece fail-closed. A regra não infere, identifica, vincula, compara ou seleciona entidades, eventos, chaves, fatos, dimensões, relações, cardinalidades, campos, valores, pares, frequências, calendário ou conteúdo privado.

**Produção permanece bloqueada** até cobertura aplicável, calibração produtiva, exclusão física, E2E e decisão formal do Gate MVP.
