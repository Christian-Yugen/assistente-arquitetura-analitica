# Plano Mestre Operacional — MVP de Arquitetura Analítica

## Princípio de execução

O catálogo de regras é o **cérebro** do produto, mas não é o produto completo. A conclusão do MVP depende de duas trilhas governadas que convergem somente após validação: a evolução auditável das 95 regras e a implementação segura da plataforma que recebe planilhas, executa o diagnóstico no servidor, apresenta os resultados, controla versões e protege os dados dos usuários.

| Trilha | Resultado esperado | Critério de avanço |
|---|---|---|
| Catálogo de regras | 95 regras com contexto, evidências, precedência, confiança, testes e rastreabilidade. | Gate por regra, por integração e por categoria. |
| Motor de diagnóstico | Profiling, contexto normalizado, executor, supressão, agregação e JSON canônico. | Regressão e golden datasets aprovados. |
| Plataforma do MVP | Upload seguro, isolamento por usuário, processamento no servidor, histórico, interface e exportação. | Testes ponta a ponta, segurança, privacidade e operação documentada. |

## Ordem obrigatória

O projeto seguirá a ordem abaixo. Nenhuma nova regra será implementada antes do checkpoint imediatamente anterior, e nenhuma ativação produtiva ocorrerá antes da calibração em dados de referência.

1. **Checkpoint Global QLT-001 a QLT-006**: auditoria cumulativa de coerência, contexto, findings, confiança, precedência, interação, regressão e dívidas técnicas.
2. **Hardening controlado**: somente correções explicitamente autorizadas, sempre com nova versão, testes e registro de impacto.
3. **Blueprint das 95 regras**: estrutura única, versionada e congelada antes da produção em escala.
4. **Ciclos de desenvolvimento de regras**: cada regra terá escopo, política, contexto, rastreabilidade, evidências, outcomes, testes, integração, regressão e fechamento.
5. **Motor completo**: execução das regras sobre um Analysis Context canônico e produção do diagnóstico estruturado.
6. **Golden datasets e calibração**: redução comprovada de falsos positivos e falsos negativos antes da promoção de confiança ou status.
7. **Pipeline e plataforma**: upload, parsing, profiler, contexto, executor, agregador, recomendações, interface, exportação e versão.
8. **Teste ponta a ponta, segurança e documentação**: gate formal de MVP 1.0.

## Distribuição do catálogo

| Categoria | Total planejado | Regras concluídas na baseline | Regras restantes |
|---|---:|---:|---:|
| Qualidade | 15 | 6 | 9 |
| Tipagem semântica | 15 | 0 | 15 |
| Fato e dimensão | 20 | 0 | 20 |
| Relacionamentos | 10 | 0 | 10 |
| Métricas | 15 | 0 | 15 |
| Alertas | 10 | 0 | 10 |
| Granularidade | 10 | 0 | 10 |
| **Total** | **95** | **6** | **89** |

## Definição de pronto do MVP 1.0

O MVP 1.0 somente poderá ser aprovado quando o catálogo de 95 regras estiver implementado e integrado, o executor estiver estável, o contexto e o ruleset estiverem versionados, e o diagnóstico apresentar qualidade, semântica, granularidade, fatos, dimensões, relacionamentos, métricas e alertas. A plataforma deverá receber Excel, processar o arquivo automaticamente no servidor, apresentar recomendações e permitir a exportação do diagnóstico.

Além disso, deverão estar aprovados golden datasets, testes unitários, de interação, regressão e ponta a ponta, assim como controles de segurança, privacidade, versionamento, manifestos, hashes, rastreabilidade, documentação, gates formais e registro de dívida técnica.

## Limitação de disponibilidade atual

Os documentos de origem definem a quantidade e a governança das 95 regras, mas não trazem neste pacote o nome e a política detalhada das 89 regras restantes. O blueprint será preparado para receber esses itens sem inventar critérios de negócio ou regras que não tenham sido autorizadas.
