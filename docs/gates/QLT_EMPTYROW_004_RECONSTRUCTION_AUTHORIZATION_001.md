# QLT-EMPTYROW-004 — Gate de Autorização de Reconstrução

**Gate:** `QLT-EMPTYROW-004-RECONSTRUCTION-001`  
**Decisão:** aprovado para especificação e implementação draft.  
**Decisor humano:** Chris.  
**Escopo de produção:** bloqueado.

## Evidência de origem

O blueprint oficial lista `QLT-EMPTYROW-004` como regra de Qualidade, prioridade `P1`, escopo de aba, dependente de profiling e destinada a detectar linhas totalmente vazias na região tabular. A fonte materializada de política não foi localizada nesta cópia do repositório. A decisão, portanto, autoriza uma reconstrução versionada, não uma alegação de recuperação canônica.

## Política autorizada

Chris aprovou a **Opção A**: detectar somente blocos de linhas inteiramente vazias entre linhas com conteúdo, reportados em forma agregada por aba. Linhas vazias continuam excluídas dos demais cálculos. A regra não remove nem altera linhas e não interpreta dados, chaves, seções ou subtotais.

## Pré-condições para ativação draft

| Controle | Estado necessário |
|---|---|
| Política e especificação reconstruídas | Concluídas e versionadas |
| Implementação sem valores brutos | Obrigatória |
| Testes de positivos, negativos, bordas e privacidade | Obrigatórios |
| Golden dataset agregado e manifesto SHA-256 | Obrigatórios |
| Calibração reprodutível | Obrigatória |
| Gate de calibração individual | Obrigatório |
| Inclusão explícita no catálogo draft | Somente após os itens anteriores |

## Limites preservados

Esta autorização não ativa a regra em produção, não libera exclusão de dados, não autoriza inferência de granularidade e não resolve os bloqueios do Gate MVP 1.0. Qualquer extensão da definição de vazio exigirá nova decisão humana e novo gate.
