# SEM-DESC-004 — Gate de Calibração Draft 001

## Decisão

A `SEM-DESC-004@0.1.0-provisional.1` está aprovada exclusivamente para `executable_draft`, após a Proposta A e o gate de reconstrução autorizados por Chris. A regra não está autorizada para produção.

| Evidência | Referência | Resultado |
|---|---|---|
| Golden dataset | `GD-SEM-DESC-004-001` — `artifacts/golden/sem-desc-draft-golden-v1.json` | Sintético, sem dados pessoais |
| SHA-256 | `2c68ab5f0119b2cd5e7dca65dac417e24ab26c36ce649de38caac871454ef4bd` | Integridade registrada |
| Avaliador | `engine/calibration/evaluate_sem_desc_draft_golden.py` | Reproduzível |
| Calibração | `{"tp": 3, "fp": 0, "fn": 0}` | Aprovada para draft |
| Perfil | `SemanticDescriptionProfile` | Apenas elegibilidade transitória de cabeçalho; demais sinais são agregados |

A classificação exige vocabulário fechado, dez ou mais textos físicos, zero fórmulas, ausência de data reconhecida e distinção agregada mínima. Ela emite `name_or_description_candidate` com confiança `0.70` e confirmação humana bloqueante. Para o cabeçalho `nome`, a SEM-SENS-015 continua emitindo `personal_data_candidate` em coleção segregada, enquanto o mascaramento existente permanece independente. Nenhum valor, cabeçalho ou conteúdo textual é persistido ou projetado.
