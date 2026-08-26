# GRN-PERIOD-005 — Gate individual de calibração draft

**Decisão:** aprovada exclusivamente para **draft controlado**.
**Autorização de implementação:** Chris — “ok. continue”.

O golden `GRN-PERIOD-005-DRAFT-GOLDEN-001` é estritamente sintético e possui SHA-256 `25ef9b21b407715f71033c15d5f4fe2fc64f66132d6724dc03143e71329bd2a6`. A calibração determinística registra `tp=1`, `fp=0` e `fn=0`; ela não constitui calibração produtiva.

A regra somente consolida sinal independente, opaco e agregado. O pipeline real fixa `independent_period_signal_count=0`; assim, não deriva sinal de workbook e permanece fail-closed. A regra não infere, valida, reconhece, extrai, converte, normaliza ou seleciona período, calendário, data, entidade, evento, chave, fato, dimensão, relação, medida, campo, valor, frequência ou conteúdo privado.

**Produção permanece bloqueada** até cobertura aplicável, calibração produtiva, exclusão física, E2E e decisão formal do Gate MVP.
