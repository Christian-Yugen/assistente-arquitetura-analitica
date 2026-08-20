# Gate QLT-CATVAR-008-DRAFT-CALIBRATION-001

## Decisão

> **Aprovada para execução no perfil draft, sem promoção produtiva.** A QLT-CATVAR-008 é incluída na allowlist com versão `0.1.0-provisional.1` exclusivamente porque a política provisória, a implementação determinística, os testes e a calibração agregada estão disponíveis e coerentes.

| Critério | Evidência | Resultado |
|---|---|---|
| Política e limite semântico | `QLT_CATVAR_008_POLICY_PROVISIONAL_001.md` | Conforme |
| Especificação lógica | `QLT_CATVAR_008_LOGICAL_SPEC_PROVISIONAL_001.md` | Conforme |
| Autorização humana | `QLT-CATVAR-008-PROVISIONAL-AUTHORIZATION-001` — Chris | Conforme |
| Golden dataset | `GD-QLT-CATVAR-008-001`, seis cenários agregados e SHA-256 no manifesto | Conforme |
| Calibração | `CAL-QLT-CATVAR-008-001`: 4 TP, 0 FP, 0 FN; 6/6 cenários sem divergência | Conforme |
| Privacidade | Ausência de valores brutos, chaves normalizadas e exemplos nos artefatos de saída | Conforme |
| Catálogo | `DRAFT_RULE_AUTHORIZATIONS[QLT-CATVAR-008]` vinculado a este gate | Conforme |

## Escopo aprovado

A regra detecta colisões de grafia sob a normalização técnica aprovada e produz finding agregado. A recomendação orienta validação humana e eventual padronização na fonte ou em dimensão controlada. Ela não altera workbook, não escolhe categoria canônica e não funde categorias.

O dicionário de domínio permanece vazio. Siglas, abreviações, singular/plural, sinônimos, proximidade textual e fonética continuam bloqueados até que Chris forneça uma política de domínio versionada e aprove gate específico.

## Bloqueios persistentes

Esta decisão não aprova produção, inferência semântica, modelagem dimensional ou uso de LLM. A promoção continua condicionada ao Gate MVP 1.0, à calibração com dados reais autorizados, à cobertura restante do catálogo e à disponibilidade de exclusão física no armazenamento.
