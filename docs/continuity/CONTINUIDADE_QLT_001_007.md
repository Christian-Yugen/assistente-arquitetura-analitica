# Continuidade Controlada — QLT-001 a QLT-007

## Objetivo

Este documento inicia a continuidade do projeto de diagnóstico e recomendação de modelagem dimensional para Power BI. O objetivo imediato é revisar a baseline cumulativa de qualidade `QLT-001` a `QLT-006`, sem alterar silenciosamente os artefatos aprovados, e somente então autorizar e desenvolver a `QLT-NUMTEXT-007`.

## Baseline de entrada

| Elemento | Versão ou estado | Decisão de continuidade |
|---|---:|---|
| Ruleset de qualidade | `PM-MVP-PBI-RULESET-QUALITY-006` v`0.6.0` | Permanece em *draft* durante a revisão. |
| Contrato do diagnóstico | v`1.0.0` | Nenhum novo payload pode violar o contrato canônico. |
| Contexto de análise | v`1.6.0` | Deve preservar os caminhos já aprovados e a extensão temporal da QLT-BADDATE-006. |
| Regras na baseline | `QLT-NULL-001` a `QLT-BADDATE-006` | Devem ser revisadas de maneira cumulativa e não isolada. |
| Gate G6.5 | Aprovado para fechamento documental | Não autoriza ativação produtiva nem a regra 007 sem checkpoint global. |

## Fontes de evidência

O trabalho parte dos documentos e dos artefatos técnicos compartilhados no projeto: Plano Mestre do MVP, Documento de Requisitos, Contrato JSON Oficial da Fase 2, Metamodelo Oficial de Regras da Fase 3, Checkpoint QLT-001 a QLT-005, a documentação da QLT-BADDATE-006 e os arquivos de aprovação G6.4 e G6.5.

## Controles inegociáveis

Toda regra deve ser versionada, rastreável, explicável e testável. A execução deve preservar a distinção entre evidência e hipótese; recomendações de baixa confiança devem ser apresentadas como perguntas ou alertas, não como conclusões. O motor deve produzir JSON estruturado e manter compatibilidade com o contrato oficial.

Não serão alteradas regras anteriores, seus hashes de evidência ou dívidas técnicas documentadas sem uma decisão explícita e versionada. A calibração com *golden datasets* continua pendente e, por isso, nenhuma regra de qualidade será tratada como habilitada para produção nesta etapa.

## Sequência autorizada

| Ordem | Entrega | Critério para prosseguir |
|---:|---|---|
| 1 | Checkpoint global QLT-001 a QLT-006 | Verificação cumulativa de versão, dependência, saída, testes, regressão, dívida técnica e compatibilidade. |
| 2 | Gate global de checkpoint | Decisão documentada, com pendências e eventuais ações corretivas delimitadas. |
| 3 | QLT-NUMTEXT-007 | Especificação e implementação iniciadas somente se o gate global autorizar explicitamente. |
| 4 | Integração e validação | Inclusão no ruleset, testes de interação e registro de novo gate. |

## Limite desta continuidade

Esta etapa estabelece a fundação executável do catálogo de regras e do motor de análise. A expansão para as demais regras, os *golden datasets* completos, o pipeline de upload privado, a interface e a ativação produtiva continuarão seguindo os gates posteriores previstos no Plano Mestre.
