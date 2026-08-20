# Retenção de Arquivo — Limitação e Controle Atual

Após a conclusão do diagnóstico, o fluxo atual executa uma remoção de referência: o `storageKey` é limpo, o status passa para `reference_removed` e o timestamp da remoção é retido para auditoria. Como todas as consultas são filtradas por proprietário, o arquivo não fica recuperável pelo produto depois dessa transição.

O helper de armazenamento disponível neste projeto fornece operações de escrita e leitura assinada, mas não expõe uma operação oficial documentada de deleção de objeto. Portanto, o fluxo atual **não declara exclusão física do S3**. A exclusão física permanece bloqueada como pendência obrigatória, e a promoção para produção não deve ocorrer antes da integração com uma operação de deleção oficialmente suportada.

| Controle | Estado |
|---|---|
| Armazenamento inicial privado por usuário/projeto | Implementado |
| Remoção de referência após análise | Implementado e testado |
| Metadados mínimos de auditoria | Implementados |
| Exclusão física do objeto | Bloqueada pela ausência de operação oficial disponível |
