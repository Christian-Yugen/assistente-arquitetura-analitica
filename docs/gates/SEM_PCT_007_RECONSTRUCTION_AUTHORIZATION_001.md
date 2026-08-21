# SEM-PCT-007 — Gate de Reconstrução 001

## Decisão

Chris aprovou a Proposta A para a classificação semântica conservadora de percentual.

## Escopo autorizado

Está autorizada exclusivamente a implementação draft que exige vocabulário fechado `percentual`, `percentagem`, `pct` ou `%`, tipo físico numérico, base mínima de 10 números físicos finitos, todos os valores no intervalo fechado de zero a um, ausência de fórmulas, números textuais, ambiguidades numéricas e classificação de data genérica. A saída deve usar `percentage_candidate`, confiança `0.75`, evidência agregada e confirmação humana bloqueante.

## Limites

Não está autorizado o reconhecimento de escala de zero a cem, moeda, índices, indicadores, preços, saldos, códigos ou sinônimos abertos como percentual. A implementação não pode expor valores, cabeçalhos, posições, títulos de aba, hashes ou dados sensíveis; o cabeçalho só poderá existir transitoriamente como booleano de elegibilidade. A ativação exige testes, golden dataset, calibração, gate individual e allowlist explícita. Produção permanece bloqueada.
