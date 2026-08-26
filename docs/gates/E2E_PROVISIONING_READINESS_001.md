# Prontidão para E2E Provisionado — 001

**Estado:** documentação preparatória; não autoriza provisionar ambiente, executar E2E, receber dados não sintéticos, alterar runtime, alterar regras, alterar allowlist ou promover produção.

## Propósito e limite

Este gate descreve a evidência que será exigida para um futuro teste ponta a ponta em ambiente provisionado. Ele existe porque a regressão atual comprova unidades, integrações, motor Python e fixtures sintéticas, mas não comprova a execução completa em um ambiente provisionado independente. O documento não cria credenciais, banco, objetos de armazenamento, contas de teste, jobs, listeners, uploads ou chamadas a serviços externos.

O escopo permanece no perfil **draft controlado**. A cobertura de **95 regras executáveis draft** não é evidência produtiva, nem libera qualquer regra, recomendação, dado ou fluxo para produção.

## Evidência atual e lacuna

| Tema | Evidência atual | Limite que permanece |
|---|---|---|
| Entrada XLSX | Validações de formato, tamanho, assinatura, abertura e máximo de dez abas são cobertas nas suítes locais. | Não há prova executada contra ambiente provisionado. |
| Motor de diagnóstico | O processo Python produz contexto agregado e descarta valores brutos no escopo draft. | Não há prova E2E independente do ciclo local. |
| Isolamento | Há testes de acesso owner-scoped nas procedures e persistência. | Ainda falta demonstrar isolamento entre contas sintéticas em ambiente provisionado. |
| Retenção | A referência privada é removida após a análise. | Não existe deleção física oficial de storage; não se pode afirmar que o objeto foi apagado. |
| Produção | O Gate MVP mantém produção bloqueada. | Este documento não é um gate de promoção. |

## Pré-condições para futura execução

Nenhum cenário abaixo poderá ser executado antes de existir um ambiente provisionado e descartável, formalmente identificado para testes. Esse ambiente deverá usar somente identidades de teste e workbooks gerados sinteticamente, sem dados pessoais, dados de clientes, títulos reais, cabeçalhos reais, valores reais ou conteúdo de produção.

| Pré-condição | Evidência mínima exigida | Falha fechada |
|---|---|---|
| Ambiente isolado | Identificador do ambiente, banco separado e configuração que não aponte para produção. | Ausência de ambiente isolado bloqueia a execução. |
| Identidades sintéticas | Duas identidades de teste distintas, sem vínculo com usuários ou clientes reais. | Ausência de separação de owners bloqueia os cenários de isolamento. |
| Workbook sintético | Fixture gerada, versão e hash verificável; conteúdo sem PII. | Qualquer origem não sintética bloqueia upload e processamento. |
| Observabilidade sanitizada | Logs e evidências compostos apenas por IDs opacos, estados e contagens agregadas. | Presença de valores, cabeçalhos, amostras, pares ou PII bloqueia a coleta de evidências. |
| Retenção declarada | Evidência da remoção de referência e declaração explícita de que isso não comprova deleção física. | Alegação de deleção física sem suporte oficial bloqueia o gate. |
| Autorização de execução | Autorização explícita de Chris para o ambiente e a janela de teste. | Nenhuma execução automatizada ocorrerá sem autorização específica. |

## Matriz de cenários E2E futuros

Os cenários são requisitos de prova; não são testes executados por este gate. Todos deverão registrar somente resultado de aprovação/reprovação, IDs opacos e contagens agregadas.

| ID | Cenário sintético futuro | Prova mínima esperada | Limite obrigatório |
|---|---|---|---|
| E2E-SYN-001 | Fluxo autorizado de workbook XLSX sintético. | Validação, análise draft, persistência owner-scoped e diagnóstico canônico agregado. | Não exibir, persistir em logs ou exportar conteúdo bruto. |
| E2E-SYN-002 | Rejeição de entrada inválida sintética. | Falha controlada para formato, base64, assinatura, tamanho ou abas fora do limite. | Nenhum arquivo inválido é encaminhado ao motor. |
| E2E-SYN-003 | Isolamento entre dois owners sintéticos. | Owner A não lê nem modifica projeto, diagnóstico ou referência de Owner B. | Não usar identidade, cookie ou dado de usuário real. |
| E2E-SYN-004 | Retenção pós-análise. | Referência privada removida; auditoria mínima preservada. | Declarar que a remoção de referência não equivale a deleção física. |
| E2E-SYN-005 | Sinais independentes indisponíveis. | Regras dependentes de sinal externo permanecem sem finding quando o sinal for zero. | O conteúdo do workbook não pode fabricar sinal independente. |
| E2E-SYN-006 | Contrato e perfil draft. | Saída compatível com contrato canônico e perfil `executable_draft`. | Não alterar rule engine, catálogo ou allowlist para fazer o cenário passar. |

## Critérios de decisão futura

Uma futura execução E2E deverá ser considerada **reprovada** se qualquer cenário revelar vazamento entre owners, dado não sintético, conteúdo bruto em evidência, execução fora do perfil draft, derivação de sinal independente a partir de workbook, alteração não autorizada de runtime ou alegação de deleção física.

Mesmo que todos os cenários acima sejam aprovados, a decisão continuará limitada ao escopo testado. A produção permanecerá bloqueada até, no mínimo, calibração produtiva aprovada, mecanismo oficial de exclusão física e respectiva prova owner-scoped, resolução ou aceite formal da linhagem da `QLT-NULL-001` e gate produtivo separado.

## Próximo gate

Depois de um ambiente descartável ser provisionado e antes de qualquer execução, deverá existir um gate de execução com: identificação do ambiente, autorização explícita de Chris, hashes das fixtures sintéticas, escopo de owners sintéticos, critérios de sanitização, janela de retenção, procedimento de encerramento e plano de resposta a falha. Este documento não concede essa autorização.

## Referências internas

| Artefato | Uso neste gate |
|---|---|
| `docs/gates/MVP_1_0_READINESS_001.md` | Registra a ausência atual de prova E2E provisionada e o bloqueio produtivo. |
| `docs/gates/PHYSICAL_DELETION_AVAILABILITY_001.md` | Delimita a indisponibilidade de deleção física. |
| `docs/gates/PRODUCTION_CALIBRATION_READINESS_001.md` | Mantém a calibração produtiva e qualquer conjunto não sintético bloqueados. |
| `server/storage.ts` | Expõe o conjunto atual de operações de armazenamento e não autoriza alegação de deleção física. |
