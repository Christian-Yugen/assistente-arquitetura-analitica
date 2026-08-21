# RULE-DEVELOPMENT-LIFECYCLE-001 — Desenvolvimento Governado de Regras

O catálogo possui 95 regras de referência, mas o perfil draft só executa regras que tenham artefatos completos e autorização explícita. A execução não é um atalho para completar o catálogo: cada regra precisa de uma cadeia de evidências própria e reprodutível.

| Etapa | Evidência mínima | Condição de avanço |
|---|---|---|
| Intake | ID oficial, origem, lacunas, dependências e status não executável. | A regra está identificada, mas ainda bloqueada. |
| Política e especificação | Condição, exclusões, evidências, limiares, severidade, confiança, perguntas e contrato. | Revisão do escopo e autorização de implementação. |
| Implementação | Código determinístico no motor e registro de versão. | A regra permanece não executável até o gate aprovado. |
| Testes | Casos positivos, negativos, limítrofes e integração do contrato. | A implementação é verificável sem valores brutos. |
| Golden dataset | Fixture, manifesto/hash, expectativas e avaliador reprodutível. | Falsos positivos e negativos são mensurados no escopo declarado. |
| Gate | Decisão, responsável, evidências, limites e próximos passos. | A regra pode entrar na allowlist draft, se essa for a decisão formal. |

`QLT-NUMTEXT-007` percorreu esse ciclo com o gate `G7.4-R1`. `QLT-NULL-001` foi reconstruída após a perda declarada do artefato canônico e recebeu versão própria, baseline novo e gate `QLT-NULL-RECONSTRUCTION-001`; ela não pode ser apresentada como recuperação do artefato original. Ambas são calibradas somente contra `GD-QUALITY-DRAFT-001` e não habilitam produção.

> Uma regra sem política, especificação, testes, dataset de referência e gate permanece catalogada, mas não executável. Nenhuma dependência de regra futura pode ser tratada como cumprida apenas por constar no blueprint.

O próximo ciclo de Qualidade começa por intake formal, como o registro `QLT-CATVAR-008_INTAKE.md`. As categorias semânticas, modelagem, relacionamentos, métricas, alertas e granularidade só avançam por ciclos equivalentes, sem ampliar a semântica do executor por conveniência.
