# SEM-DUR-008 — Gate de Calibração Draft 001

## Decisão

Após a Proposta A e o Gate de Reconstrução aprovados por Chris, a `SEM-DUR-008@0.1.0-provisional.1` está autorizada exclusivamente como `executable_draft`. Esta decisão não autoriza produção nem conversão, inferência ou normalização de unidade.

| Evidência | Registro |
|---|---|
| Golden dataset | `artifacts/golden/sem-dur-draft-golden-v1.json` (`GD-SEM-DUR-008-001`) |
| SHA-256 | `3346431a07880834e7dfa5487f84201a07319da6421fc00804f10664d5e4d468` |
| Avaliador reproduzível | `python3 -m engine.calibration.evaluate_sem_dur_draft_golden` |
| Resultado | `{"tp": 3, "fp": 0, "fn": 0}` |
| Perfil privado | `SemanticDurationProfile` com booleano e contagens agregadas |

A regra exige vocabulário fechado de duração, ao menos dez números físicos finitos, ausência de fórmulas, datas reconhecidas, texto numérico e ambiguidade. Ela emite somente `duration_candidate`, com confiança `0.80` e confirmação humana bloqueante. Cabeçalhos são processados transitoriamente; valores, unidade derivada, distribuição, formato e conteúdo não são retidos ou projetados. O mascaramento existente permanece independente e obrigatório.
