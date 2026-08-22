# SEM-LOC-011 — Gate de Calibração Draft 001

## Decisão

O gate individual de calibração aprova a `SEM-LOC-011@0.1.0-provisional.1` para execução **exclusivamente** no perfil `executable_draft`. A promoção produtiva permanece bloqueada.

## Evidências de calibração

| Elemento | Evidência |
|---|---|
| Dataset | `GD-SEM-LOC-011-001` — `artifacts/golden/sem-loc-draft-golden-v1.json` |
| SHA-256 | `4d7023655fc0d6dc7a6667ab7e50e67bc7fa8d0db0112627b4ce4891ee28b02b` |
| Avaliador | `python3 -m engine.calibration.evaluate_sem_loc_draft_golden` |
| Resultado | `{"tp": 3, "fp": 0, "fn": 0}` |
| Perfil | `executable_draft` |
| Saída | `location_candidate`, confiança `0.75`, pergunta humana bloqueante |

O dataset usa somente tokens sintéticos e não contém localização real, endereço, CEP, coordenada, nome, dado pessoal ou título de aba. A avaliação projeta apenas métricas agregadas e não retorna cabeçalho, rótulo ou conteúdo de célula.

## Limites preservados

A regra permanece limitada ao vocabulário fechado `cidade`, `municipio`, `pais`, `regiao` e `localizacao`, após normalização transitória. Ela exige no mínimo 10 textos físicos, 2 a 50 distintos agregados, razão de distintos até `0.90` e ausência de fórmulas, datas reconhecidas e ambiguidades. Não realiza geocodificação, consulta externa, inferência por valor, hierarquia territorial ou decisão de modelagem automática.

O catálogo executor é a única autorização de despacho. Produção, vocabulário adicional e decisões sem confirmação humana continuam bloqueados.
