# TEST-STRATEGY-001 — Estratégia de Validação do MVP Draft

O projeto trata testes como evidência de governança, não apenas como verificação de compilação. A suíte combina testes TypeScript/Vitest para API, UI, persistência e documentação, com testes `unittest` em Python para profiling, regras, contrato e calibração. A regressão deve ser executada integralmente antes de qualquer checkpoint de decisão.

| Comando | Escopo coberto | Resultado exigido |
|---|---|---|
| `pnpm test` | Servidor, persistência owner-scoped, interface, segurança e testes documentais. | Todas as suítes Vitest aprovadas. |
| `pnpm test:engine` | Regras Python, profiling, contrato, perfil draft, runner e derivações. | Todos os testes `unittest` aprovados. |
| `pnpm check` | Tipagem TypeScript. | `tsc --noEmit` sem erro. |
| `python3 -m engine.calibration.evaluate_quality_draft_golden` | Reavaliação do golden dataset de qualidade. | Relatório reproduzível compatível com a fixture aprovada. |

Os testes de segurança verificam a rejeição de ZIP que não seja XLSX legível antes de `storagePut`, o mascaramento de dados identificáveis, a ausência de payload sensível no diagnóstico, mensagens de erro genéricas, remoção owner-scoped da referência privada e impossibilidade de leitura entre proprietários. Os testes do motor verificam que as duas regras executáveis geram finding canônico, pergunta quando aplicável e recomendação derivada, sem simular classificação dimensional.

As provas documentais são testes de regressão para decisões que não podem depender apenas de memória operacional, incluindo reconstrução de artefato, exceção de retenção, calibração limitada, perfil draft e validação real de XLSX. Elas não substituem aceites humanos ou gates: confirmam apenas que o registro aprovado continua presente no repositório.
