# GRN-DUP-010 — Gate individual de calibração draft

**Autorização de implementação:** Chris — “autorizado”.

O golden `GRN-DUP-010-DRAFT-GOLDEN-001` é estritamente sintético e possui SHA-256 `109c26d19fdab588af1ded9251c6aa1457ddfa50f0a92986f5a0ca58c48832fa`. A calibração determinística registra `tp=1`, `fp=0` e `fn=0`; ela não constitui calibração produtiva.

O pipeline real fixa `independent_duplicate_grain_signal_count=0`, não deriva sinal de workbook e permanece fail-closed. A regra não identifica, localiza, seleciona ou corrige duplicidades, linhas, chaves, níveis de detalhe, entidades, eventos, fatos, dimensões, relações, cardinalidades, métricas, campos, valores, pares, frequências, períodos ou conteúdo privado. **Produção permanece bloqueada.**

