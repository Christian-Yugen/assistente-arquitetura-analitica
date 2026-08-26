# Proposta de Migração de Linhagem dos Intakes — 001

**Estado:** proposta documental não executável. **Base:** `PRODUCTION_LINEAGE_RECONCILIATION_001`. **Produção:** bloqueada.

## Objetivo

Estabelecer uma migração exclusivamente documental para que cada regra indicada como `executable_draft` no índice governado possua uma prova de linhagem consultável, preservando o histórico de autorizações, gates, golden sintético, calibração e bloqueio produtivo. A proposta não altera a allowlist, o contrato, o pipeline, os perfis, os classificadores, as contagens de execução ou o comportamento de qualquer regra.

## Estratégia A — normalização aditiva e versionada

Cada intake legado, ausente ou com prontidão defasada receberá uma **ficha de reconciliação aditiva** identificada por regra. A ficha apontará para os artefatos de evidência já existentes, registrará o status do índice como fonte operacional draft e declarará explicitamente que produção segue bloqueada. Ela não sobrescreverá o intake histórico nem reinterpretará autorizações.

| Ordem | Grupo | Ação documental permitida | Proibido sem novo gate |
|---:|---|---|---|
| 1 | Nove regras sem intake individual | Criar ficha de linhagem com referências rastreáveis a gate, golden, calibração e testes existentes. | Criar ou modificar uma regra, alterar outputs, restaurar conteúdo canônico ou promover ambiente. |
| 2 | Dez intakes legados | Criar mapa de equivalência entre campos históricos e a ficha versionada. | Reescrever o intake original, inferir autorização ausente ou alterar runtime. |
| 3 | Quinze intakes com prontidão defasada | Registrar reconciliação para a evidência de ativação já existente. | Tratar a atualização documental como autorização de produção. |
| 4 | Sessenta e uma entradas sem booleano histórico | Documentar a ausência de campo como diferença de esquema e testar a fonte operacional. | Assumir que a ausência é confirmação de execução produtiva. |

## Critérios de aceite documental

Uma ficha de reconciliação deverá conter o ID da regra, a fonte operacional de prontidão, referências aos gates e evidências existentes, a descrição de diferenças de esquema, o bloqueio explícito de produção e a ausência de alteração de executabilidade. O ciclo será aprovado somente por validações documentais e regressão; ele continuará **não executável** no sentido de não modificar comportamento de runtime.

## Gate para mudança posterior

Qualquer automação de migração, edição de intakes históricos, alteração de allowlist, calibração com dados aprovados para produção, exclusão física, execução E2E provisionada ou promoção de ambiente exige autorização explícita de Chris, design técnico próprio, testes e gate individual. Esta Proposta A não concede essa autorização.
