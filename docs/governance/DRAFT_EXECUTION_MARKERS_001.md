# Marcadores Autorizados do Executor Draft — PM-MVP-PBI-DRAFT-EXECUTION-001

O contrato reconstruído exige que o diagnóstico parcial não aparente uma execução completa nem preencha valores operacionais arbitrários. Para isso, as versões de motor, ruleset e metodologia, os textos de limitação e os estados de execução autorizados foram extraídos do executor e formalizados no artefato versionado `draft-execution-profile-v1.json`.

| Grupo | Fonte operacional | Regra de uso |
|---|---|---|
| Versões do motor e do ruleset | Perfil de execução | Devem ser lidas do perfil; o executor não pode defini-las internamente. |
| Cobertura do catálogo | Perfil de execução | A completude é calculada como regras executadas sobre o total autorizado. |
| Limitações e suposições | Perfil de execução | Devem declarar que o resultado é parcial e não inferir módulos não executados. |
| Próxima ação e resumo | Perfil de execução + contagens reais | Textos só podem usar os templates aprovados com contagens derivadas do contexto. |
| Uso de IA | Perfil de execução | O perfil atual declara ausência de IA; uma ativação futura exige nova versão e revisão. |

O perfil é autorizado apenas para validação interna do MVP draft pelo gate `CONTRACT-RECONSTRUCTION-001`. Alterá-lo, ativar IA ou promover o resultado para produção requer um novo artefato e revisão de governança.

## Allowlist verificável

A allowlist `governed_output_paths` presente no perfil é fechada e deve conter exatamente os 14 caminhos abaixo: `analysis.assumptions[0]`, `analysis.limitations[0]`, `summary.completeness_ratio`, `summary.executive_summary`, `summary.next_recommended_action`, `proposed_model.status`, `proposed_model.limitations[0]`, `execution.status`, `execution.engine_version`, `execution.ruleset_version`, `execution.confidence_methodology_version`, `execution.modules[0].module`, `execution.modules[0].status` e `execution.ai_usage`.

O executor valida essa allowlist antes de devolver um diagnóstico parcial. A validação calcula os valores esperados a partir do perfil e do contexto real e falha se algum desses caminhos divergir. Os testes alteram deliberadamente valores autorizados para provar que uma reintrodução de marcador hardcoded é detectada.
