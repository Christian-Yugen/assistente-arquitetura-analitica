# Retenção de Arquivo — Limitação e Controle Atual

Após a conclusão do diagnóstico, o fluxo atual executa uma remoção de referência: o `storageKey` é limpo, o status passa para `reference_removed` e o timestamp da remoção é retido para auditoria. Como todas as consultas são filtradas por proprietário, o arquivo não fica recuperável pelo produto depois dessa transição.

Antes da execução do motor e da persistência, o pipeline mascara padrões de CPF, e-mail e campos de nome explicitamente rotulados em textos de projeto, objetivo e nome de arquivo. O profiler também retém somente identificadores estruturais de abas, como `Aba 1`, e não preserva o título bruto da planilha. Falhas do motor são retornadas ao cliente por mensagens genéricas, sem detalhes de caminhos temporários ou conteúdo do workbook.

O helper de armazenamento disponível neste projeto fornece operações de escrita e leitura assinada, mas não expõe uma operação oficial documentada de deleção de objeto. Portanto, o fluxo atual **não declara exclusão física do S3**. A exclusão física permanece bloqueada como pendência obrigatória, e a promoção para produção não deve ocorrer antes da integração com uma operação de deleção oficialmente suportada.

| Controle | Estado |
|---|---|
| Armazenamento inicial privado por usuário/projeto | Implementado |
| Remoção de referência após análise | Implementado e testado |
| Metadados mínimos de auditoria | Implementados |
| Mascaramento de textos de entrada e identificadores de abas | Implementado e testado |
| Mensagens de erro sem detalhes internos | Implementado e testado |
| Exclusão física do objeto | Bloqueada pela ausência de operação oficial disponível |

## Exceção de retenção física — proposta de aceite

**Identificador:** `RETENTION-EXCEPTION-001`  
**Status:** pendente de aceite formal; não aprovada para produção.  
**Responsável proposto pelo aceite:** proprietário do produto, Chris.

| Aspecto | Definição controlada |
|---|---|
| Limitação | O projeto não dispõe de operação oficial para excluir fisicamente o objeto privado após a análise. |
| Controle compensatório | O objeto é armazenado sob chave privada owner-scoped e, após a análise, sua referência é removida do banco com `storageKey: null`, `retentionStatus: "reference_removed"` e `referenceRemovedAt`. |
| Evidência | `server/analysisRouter.flow.test.ts`, `server/db.writeScope.test.ts` e `server/analysisRetention.test.ts`. |
| Restrição | Nenhuma promoção a produção é permitida enquanto a exclusão física não tiver implementação oficial, teste de integração e gate de governança aprovado. |
| Gatilho de reavaliação | Disponibilização de operação oficial de exclusão no armazenamento, seguida de teste de deleção por proprietário e atualização desta exceção. |

Esta proposta não reduz os requisitos de proteção de dados. Ela apenas documenta o controle compensatório temporário e o bloqueio de produção que permanece ativo até a resolução técnica da exclusão física.
