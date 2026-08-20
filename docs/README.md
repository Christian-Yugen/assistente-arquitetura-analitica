# Documentação do Assistente de Arquitetura Analítica

Este índice reúne a documentação verificável do **MVP draft**. O produto está apto apenas a uso controlado no perfil autorizado: ele executa duas regras de qualidade, gera diagnóstico JSON canônico e mantém bloqueios explícitos para produção, modelagem dimensional completa e exclusão física de objetos privados.

| Área | Documento principal | Escopo |
|---|---|---|
| Arquitetura | [Arquitetura do MVP draft](architecture/MVP_DRAFT_ARCHITECTURE_001.md) | Componentes, fluxos e fronteiras de confiança. |
| Contrato e executor | [Contrato e executor](architecture/CONTRACT_AND_EXECUTOR_001.md) | JSON canônico, perfil draft e derivação de resultados. |
| Regras | [Ciclo de desenvolvimento de regras](governance/RULE_DEVELOPMENT_LIFECYCLE_001.md) | Intake, especificação, calibração e gates. |
| API | [API tRPC de análise](api/ANALYSIS_TRPC_API_001.md) | Procedimentos autenticados, entradas, saídas e erros. |
| Testes | [Estratégia de validação](testing/TEST_STRATEGY_001.md) | Suítes, evidências e critérios de regressão. |
| Segurança | [Controles de privacidade](security/PRIVACY_CONTROLS_001.md) | Minimização, sanitização, retenção e limites. |
| Uso | [Manual do usuário](user/MANUAL_DO_USUARIO_MVP_DRAFT_001.md) | Fluxo de análise e limitações visíveis ao usuário. |

Os documentos de governança, decisões históricas e gates específicos permanecem em `docs/governance`, `docs/checkpoints` e `docs/gates`. Este índice não altera esses registros; ele organiza a leitura do estado atual e aponta para a evidência de implementação correspondente.
