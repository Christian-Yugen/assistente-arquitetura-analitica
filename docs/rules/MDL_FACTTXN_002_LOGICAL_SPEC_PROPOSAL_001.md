# MDL-FACTTXN-002 — Especificação Lógica Proposta 001

## Condição

1. Receber a hipótese de granularidade canônica da aba.
2. Exigir `row_count >= 20`.
3. Identificar sinal temporal apenas por perfil agregado de data estrita ou física.
4. Exigir variabilidade temporal alta, com razão de distintos não faltantes de pelo menos 0,80.
5. Exigir ao menos uma medida numérica física elegível.
6. Emitir `fact_transactional` apenas se todos os sinais forem satisfeitos.

## Saída e privacidade

A saída canônica terá classificação, confiança, evidência agregada e pergunta humana obrigatória. Perfis e fragmentos não podem reter dados brutos, identificadores, cabeçalhos, posições ou títulos de aba.

## Bloqueio

Não há código executável ou ativação permitidos antes do gate de reconstrução aprovado por Chris.
