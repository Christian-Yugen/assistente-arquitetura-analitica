# QLT-NULL-RECONSTRUCTION-001 — Linhagem e Limites da Reconstrução

**Status:** implementação validada e execução autorizada somente no perfil draft; produção bloqueada.  
**Regra-alvo:** `QLT-NULL-001`.  
**Versão candidata:** `0.1.0-reconstructed.1`.

Chris informou que o artefato canônico da `QLT-NULL-001` foi perdido e autorizou a criação de uma regra nova equivalente, adequada ao MVP draft. Como a fonte original e o seu hash de baseline não estão disponíveis, esta reconstrução não pode alegar recuperação, equivalência histórica comprovada ou continuidade de versão do artefato perdido.

| Aspecto | Decisão governada |
|---|---|
| Linhagem | Artefato novo, identificado como reconstruído. |
| Referências permitidas | Contrato PM-MVP-PBI-CON-001 reconstruído, catálogo oficial de regras e padrões disponíveis das regras de qualidade. |
| Baseline | `QLT-NULL-001-BASELINE-RECONSTRUCTED-001`, com manifesto SHA-256 verificável; criado exclusivamente para a reconstrução. |
| Execução | Autorizada somente para implementar e testar a versão candidata no perfil draft. |
| Produção | Continua bloqueada pelos critérios gerais do MVP e não é autorizada por este intake. |
| Fonte perdida | Registrada em `QLT_NULL_RECOVERY_BLOCKER_001.md` como evidência histórica; não será apagada nem reinterpretada como recuperada. |

> A reconstrução deve priorizar um comportamento explicável, conservador e testável. Nulos, valores vazios e sentinelas não podem ser tratados como sinônimos sem política aprovada, pois essa decisão altera a interpretação dimensional do dado.

## Aceite de implementação controlada

Chris aprovou a continuidade após a apresentação da política, especificação e baseline pré-implementação. O aceite autoriza somente a criação do código, os testes unitários e a integração controlada da versão `0.1.0-reconstructed.1`.

> “ok. continue” — Chris, interpretado como aceite do gate solicitado para implementação controlada no perfil draft.

| Critério de gate | Situação |
|---|---|
| Linhagem reconstruída e sem alegação de recuperação canônica | Aprovado. |
| Política de nulos, vazios, `NaN`, sentinelas e fórmulas | Aprovada para implementação draft. |
| Especificação lógica e matriz de testes | Aprovadas para implementação draft. |
| Baseline pré-implementação com hash verificável | Aprovado. |
| Escopo de autorização | Implementação e testes controlados somente. |
| Produção e expansão de catálogo | Bloqueadas. |

## Decisão final de reconstrução

A implementação da `QLT-NULL-001` reconstruída foi validada contra a política aprovada, a especificação lógica e o baseline pré-implementação. O motor avalia ausências por meio de contagens agregadas, produz evidência canônica sem valores brutos e registra a versão reconstruída em cada finding. A allowlist de execução agora exige gate explícito para as duas regras habilitadas no draft: `QLT-NUMTEXT-007` e `QLT-NULL-001`.

| Evidência de encerramento | Resultado |
|---|---|
| Testes do motor | 36 testes Python aprovados, incluindo regra, profiling, pipeline, catálogo e runner com workbook real temporário. |
| Regressão da aplicação | 48 testes Vitest aprovados e verificação TypeScript aprovada. |
| Execução do runner | Workbook com 20% de ausências produziu finding `QLT-NULL-001` de severidade alta sem reter conteúdo de células. |
| Proteção de catálogo | Uma entrada adicionada ao registry sem gate explícito continua bloqueada. |
| Regras executáveis draft | 2 de 95: `QLT-NUMTEXT-007` e `QLT-NULL-001`. |

> **Decisão:** aprovada a execução da `QLT-NULL-001@0.1.0-reconstructed.1` no MVP draft. Esta decisão não altera a linhagem do artefato canônico perdido, não autoriza produção e não promove nenhuma outra regra do catálogo.

Os próximos bloqueios permanecem a calibração com golden datasets, o ciclo formal das regras ainda pendentes e a exclusão física de arquivos quando houver operação oficial suportada.
