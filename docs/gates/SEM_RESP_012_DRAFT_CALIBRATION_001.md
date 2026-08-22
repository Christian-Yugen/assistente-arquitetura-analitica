# SEM-RESP-012 — Gate de Calibração Draft 001

## Decisão

O gate individual de calibração aprova a `SEM-RESP-012@0.1.0-provisional.1` para execução **exclusivamente** no perfil `executable_draft`. A promoção produtiva permanece bloqueada.

## Evidências de calibração

| Elemento | Evidência |
|---|---|
| Dataset | `GD-SEM-RESP-012-001` — `artifacts/golden/sem-resp-draft-golden-v1.json` |
| SHA-256 | `a5a2b4a7ade69ed6bad2936238f43fe879fc28de13267fe73ded3a704496db65` |
| Avaliador | `python3 -m engine.calibration.evaluate_sem_resp_draft_golden` |
| Resultado | `{"tp": 3, "fp": 0, "fn": 0}` |
| Perfil | `executable_draft` |
| Saída | `responsible_candidate`, confiança `0.70`, pergunta humana bloqueante |

O dataset usa somente tokens sintéticos e não contém nome, e-mail, CPF, identificador, cargo, equipe, responsável real, dado pessoal ou título de aba. A avaliação projeta apenas métricas agregadas e não retorna cabeçalho, rótulo ou conteúdo de célula.

## Limites preservados

A regra permanece limitada ao vocabulário fechado `responsavel`, após normalização transitória. Ela exige no mínimo 10 textos físicos, 2 a 50 distintos agregados, razão de distintos até `0.90` e ausência de fórmulas, datas reconhecidas e ambiguidades. Não identifica pessoa, equipe, área, cargo, titularidade ou papel por conteúdo, nem toma decisão de modelagem automática.

O catálogo executor é a única autorização de despacho. Produção, vocabulário adicional e decisões sem confirmação humana continuam bloqueados.
