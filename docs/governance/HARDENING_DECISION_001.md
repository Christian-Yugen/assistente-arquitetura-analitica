# Hardening Decision 001 — Baseline QLT-001 a QLT-006

## Decisão

Nenhuma regra da baseline será corrigida nesta etapa. O checkpoint identificou dívida de namespace e uma limitação de materialização do artefato canônico QLT-NULL-001, mas não há autorização nem evidência suficiente para editar a baseline com segurança.

| Item | Decisão | Justificativa |
|---|---|---|
| `sheet.name` em QLT-DUP-002 | Manter como dívida técnica | Exige revisão versionada de naming/contexto e regressão cumulativa. |
| `column.name` em QLT-NULL-001 | Manter como dívida técnica | O JSON canônico com hash G6.4 não está materializado neste pacote. |
| QLT-BADDATE-006 e Context v1.6.0 | Preservar sem alteração | A integração G6.4 e o fechamento G6.5 já condicionam a continuidade à compatibilidade temporal. |
| Produção | Manter bloqueada | Golden datasets e calibração ainda não foram executados. |

## Efeito

O hardening nesta etapa consiste em **congelar a governança e impedir mudanças silenciosas**, não em refatorar regras históricas. O código novo deverá respeitar a estrutura comum definida no blueprint e manter compatibilidade com o contrato de diagnóstico 1.0.0.
