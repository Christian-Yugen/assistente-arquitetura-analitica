# Inventário Auditável — QLT-001 a QLT-006

## Critério de inventário

Esta matriz separa o **estado lógico aprovado pela baseline** do **estado material disponível no pacote recebido**. Essa separação evita tratar um arquivo de exemplo ou de versão anterior como se fosse a fonte canônica de uma regra aprovada.

| Regra | Versão lógica no ruleset | Estado lógico | Contrato | Escopo | Dependência de estágio | Outcomes verificados | Estado da evidência material |
|---|---:|---|---:|---|---|---|---|
| QLT-NULL-001 | 1.0.0 | Draft no ruleset v0.6.0 | 1.0.0 | Coluna | Não confirmado no artefato canônico | Não confirmado no artefato canônico | O pacote contém somente um exemplo Fase 3, schema 1.0.0 e estado `active`; não é equivalente ao hash de baseline G6.4. |
| QLT-DUP-002 | 1.0.0 | Draft | 1.0.0 | Aba | `profiling` | Baixo, médio e alto; inclui pergunta bloqueante no caso alto | Materializado e compatível com o ruleset. |
| QLT-EMPTYCOL-003 | 1.0.0 | Draft | 1.0.0 | Coluna | `profiling` | Finding de coluna estruturalmente vazia | Materializado e compatível com o ruleset. |
| QLT-EMPTYROW-004 | 1.0.0 | Draft | 1.0.0 | Aba | `profiling` | Baixo, médio e alto | Materializado e compatível com o ruleset. |
| QLT-MIXTYPE-005 | 1.0.0 | Draft | 1.0.0 | Coluna | `profiling` | Baixo, médio e alto; inclui pergunta de alto impacto | Materializado e compatível com o ruleset. |
| QLT-BADDATE-006 | 1.0.0 | Draft | 1.0.0 | Coluna | `profiling`, com contexto temporal v1.6.0 | Outcomes de revisão conforme intenção e falha temporal | Materializado e compatível com o ruleset. |

## Dependências e compatibilidade

As cinco regras materializadas adotam o contrato de diagnóstico `1.0.0` e dependem de métricas de profiling, sem requerer a ocorrência prévia de outra regra. A ausência de ciclos de dependência está registrada no G6.4. A QLT-BADDATE-006 adiciona dependência prática do perfil temporal versionado no Analysis Context v1.6.0; por isso, qualquer downgrade de contexto é incompatível.

Os outcomes das regras materializadas emitem findings e, em cenários de maior risco, podem emitir perguntas que bloqueiam inferências dependentes. A QLT-DUP-002, por exemplo, não remove registros: solicita confirmação quando duplicidades integrais podem alterar granularidade e métricas. A QLT-BADDATE-006 evita concluir sobre invalidade sem intenção temporal e tentativa de parsing suficientes.

## Limitação e ação exigida

O hash canônico da QLT-NULL-001 registrado no G6.4 não corresponde ao único JSON de QLT-NULL materializado neste pacote. O JSON disponível é um exemplo anterior do metamodelo, com schema `1.0.0` e status `active`; portanto, não serve para comprovar os outcomes ou as dependências da baseline v0.6.0. A divergência não anula os gates G6.4 e G6.5, mas impede uma reconfirmação integral dos seis arquivos nesta cópia dos anexos.

> **Decisão:** manter o checkpoint aprovado apenas para continuidade governada, sem alterar a regra. A recuperação do JSON canônico de QLT-NULL-001 e a nova conferência de hash ficam registradas como pré-condição de hardening antes de qualquer promoção de ambiente.

## Referências internas

| Referência | Evidência |
|---|---|
| Baseline de regras | `quality-ruleset-v0.6.0.json` |
| Validação de integração | `g6.4-validation-report.json` |
| Fechamento documental | `g6.5-closure-report.json` |
| Regras materializadas | `qlt_dup_002.json` a `qlt_baddate_006.json` |
| Exemplo não canônico | `Fase_3_Metamodelo_Regras_v1.0/.../qlt_null_001.json` |
