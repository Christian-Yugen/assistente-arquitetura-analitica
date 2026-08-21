# SEM-QTY-005 — Gate de Reconstrução 001

## Decisão

Chris aprovou a Proposta A para a classificação semântica conservadora de quantidade.

## Escopo autorizado

Está autorizada exclusivamente a implementação draft que exige vocabulário fechado `quantidade`, `qtd` ou `qtde`, tipo físico numérico, base mínima de 10 números físicos finitos, ausência de fórmulas, números textuais, ambiguidades numéricas e classificação de data genérica. A saída deve usar `quantity_candidate`, confiança `0.75`, evidência agregada e confirmação humana bloqueante.

## Limites

Não está autorizada a classificação de estoque, volume, idade, moeda, preço, valor, saldo, percentual, código ou sinônimos abertos como quantidade. A implementação não pode expor valores, cabeçalhos, posições, títulos de aba, hashes ou dados sensíveis; o cabeçalho só poderá existir transitoriamente como booleano de elegibilidade. A ativação exige testes, golden dataset, calibração, gate individual e allowlist explícita. Produção permanece bloqueada.
