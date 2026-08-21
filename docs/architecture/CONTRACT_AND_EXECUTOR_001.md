# CONTRACT-AND-EXECUTOR-001 — Diagnóstico Canônico e Executor Draft

**Contrato:** `PM-MVP-PBI-CON-001`, schema `1.0.0`.  
**Perfil de execução:** `PM-MVP-PBI-DRAFT-EXECUTION-001`, versão `1.0.0`.

O diagnóstico é a saída de integração entre motor, persistência e interface. A fonte estrutural é `artifacts/contracts/PM-MVP-PBI-CON-001/diagnosis.schema.json`; a semântica de transição e os marcadores permitidos no resultado parcial estão no perfil `draft-execution-profile-v1.json`. `engine/contracts/validation.py` valida schema e regras cruzadas antes que o runner devolva o payload ao servidor.

| Bloco canônico | Origem no MVP draft | Tratamento atual |
|---|---|---|
| `analysis`, `file`, `execution` | Metadados validados e execução observada. | Preenchidos com rastreabilidade de versão, correlação e status. |
| `sheets` | Profiler agregado de workbook. | Abas anonimizadas e colunas com perfil sem valores brutos. |
| `findings` | Regras executáveis autorizadas. | Evidência agregada, impacto, recomendação e entidade afetada. |
| `questions` | Regras que exigem validação humana. | Perguntas bloqueantes rastreáveis às regras afetadas. |
| `summary` | Agregação dos findings e marcadores do perfil. | Indica cobertura parcial, riscos e próxima ação governada. |
| `proposed_model`, `relationships`, `metrics` | Perfil draft. | Sem inferência livre; status de insuficiência e coleções vazias autorizadas. |

## Derivação de recomendações

Cada finding interno contém a recomendação prevista na sua especificação. `to_diagnosis_fragment` transporta esse texto para `findings[].recommendation`, preservando o `rule_id`, a versão, a evidência agregada e a coluna afetada. A recomendação da `QLT-NUMTEXT-007` orienta a confirmação do significado de negócio antes de converter um valor numérico armazenado como texto; a recomendação da `QLT-NULL-001` orienta o tratamento explícito da ausência antes de modelar agregações ou relações dependentes da coluna.

O campo `summary.next_recommended_action` não é uma recomendação de modelagem. Ele é um marcador controlado pelo perfil parcial e deve ser lido em conjunto com as limitações do diagnóstico. A prova de separação entre esses dois conceitos está em `engine/tests/test_recommendation_derivation.py` e na documentação [DIAGNOSIS-RECOMMENDATION-DERIVATION-001](DIAGNOSIS_RECOMMENDATION_DERIVATION_001.md).

## Invariantes do executor

O executor não pode chamar regra ausente de `DRAFT_RULE_AUTHORIZATIONS`, preencher caminhos governados com valores internos, expor valores brutos, ou emitir estrutura fora do schema. Esses limites são verificados por `engine/catalog.py`, `engine/contracts/execution_profile.py` e pelos testes de perfil draft. A regra só é contada como executável após seu registro, versão e gate de autorização estarem presentes na allowlist.
