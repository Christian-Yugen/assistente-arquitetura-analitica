# Gate de Calibração Draft — SEM-STATUS-009

## Decisão

Após a Proposta A e o Gate de Reconstrução aprovados por Chris, a `SEM-STATUS-009@0.1.0-provisional.1` está autorizada exclusivamente como `executable_draft`. Esta decisão não autoriza produção, dicionário de estados, normalização, inferência de domínio ou retenção de rótulos.

| Evidência | Registro |
|---|---|
| Golden dataset | `artifacts/golden/sem-status-draft-golden-v1.json` (`GD-SEM-STATUS-009-001`) |
| SHA-256 | `03be251ac2bab794293e5987551f360fb6d456a71f7450cfdde85d320352493a` |
| Avaliador reproduzível | `python3 -m engine.calibration.evaluate_sem_status_draft_golden` |
| Resultado | `{"tp": 3, "fp": 0, "fn": 0}` |
| Perfil privado | `SemanticStatusProfile` com elegibilidade agregada de cabeçalho e contagens, sem retenção de conteúdo |

A regra exige vocabulário fechado `status`, `situação` ou `estado`, ao menos dez textos físicos, entre duas e doze categorias agregadas, razão de distintos de até `0,50` e ausência de fórmulas, datas reconhecidas e ambiguidades. Ela emite somente `status_candidate`, com confiança `0,75` e confirmação humana bloqueante. Cabeçalhos são processados transitoriamente; valores, rótulos, tokens, frequências individuais, posições, exemplos, títulos de abas e formatos de célula não são retidos ou projetados. O mascaramento existente permanece independente e obrigatório.
