# GRN-SNAP-006 — Gate individual de calibração draft

**Decisão:** aprovada exclusivamente para **draft controlado**.
**Autorização de implementação:** Chris — “sim”.

O golden `GRN-SNAP-006-DRAFT-GOLDEN-001` é estritamente sintético e possui SHA-256 `aad8c27211fddf4a2e39cc6fe77fc44fd396afa48e517f6785cf0cbf3b5b20db`. A calibração determinística registra `tp=1`, `fp=0` e `fn=0`; ela não constitui calibração produtiva.

A regra somente consolida sinal independente, opaco e agregado. O pipeline real fixa `independent_snapshot_signal_count=0`; assim, não deriva sinal de workbook e permanece fail-closed. A regra não infere período, calendário, entidade, evento, chave, fato, dimensão, relação, medida, campo, valor ou conteúdo privado.

**Produção permanece bloqueada** até cobertura aplicável, calibração produtiva, exclusão física, E2E e decisão formal do Gate MVP.
