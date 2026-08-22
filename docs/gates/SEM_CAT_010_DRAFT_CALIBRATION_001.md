# Gate de Calibração Draft — SEM-CAT-010

## Decisão

Após a Proposta A e o Gate de Reconstrução aprovados por Chris, a `SEM-CAT-010@0.1.0-provisional.1` está autorizada exclusivamente como `executable_draft`. Esta decisão não autoriza produção, taxonomia de negócio, dicionário de categorias, normalização, inferência de domínio ou retenção de rótulos.

| Evidência | Registro |
|---|---|
| Golden dataset | `artifacts/golden/sem-cat-draft-golden-v1.json` (`GD-SEM-CAT-010-001`) |
| SHA-256 | `62dd2c4af50ff6b9562e188c38fb44038eb46b09ad39ca1b0438a7f54d69e774` |
| Avaliador reproduzível | `python3 -m engine.calibration.evaluate_sem_cat_draft_golden` |
| Resultado | `{"tp": 3, "fp": 0, "fn": 0}` |
| Perfil privado | `SemanticCategoryProfile` com elegibilidade agregada de cabeçalho e contagens, sem retenção de conteúdo |

A regra exige o vocabulário fechado `categoria`, ao menos dez textos físicos, entre duas e vinte categorias agregadas, razão de distintos de até `0,50` e ausência de fórmulas, datas reconhecidas e ambiguidades. Ela emite somente `category_candidate`, com confiança `0,70` e confirmação humana bloqueante. Cabeçalhos são processados transitoriamente; valores, rótulos, tokens, frequências individuais, posições, exemplos, títulos de abas e formatos de célula não são retidos ou projetados. O mascaramento existente permanece independente e obrigatório.
