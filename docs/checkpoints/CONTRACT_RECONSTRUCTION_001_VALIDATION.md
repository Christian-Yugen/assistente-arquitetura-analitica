# Validação — CONTRACT-RECONSTRUCTION-001

O contrato `PM-MVP-PBI-CON-001` foi reconstruído de forma governada porque os arquivos `diagnosis.schema.json` e os modelos Pydantic originais não estavam entre os materiais compartilhados. O documento DOCX da Fase 2 foi mantido como fonte primária; a nova representação registra sua linhagem, seções de origem e lacunas diretamente no schema JSON.

| Verificação | Resultado | Evidência |
|---|---|---|
| Estrutura JSON Schema Draft 2020-12 | Aprovada | Schema reconstruído e exemplo mínimo/completo válidos. |
| Rejeição de propriedade raiz desconhecida | Aprovada | Exemplo inválido rejeitado. |
| Tipos, UUIDs, datas, enums e limites | Aprovados | Schema e modelos Pydantic. |
| Referências de arquivo, aba, finding e pergunta | Aprovadas | Validação cruzada nos modelos Pydantic. |
| Metadados sem valores genéricos arbitrários | Aprovada | Teste de executor com metadados de entrada e contexto. |
| Validação do projeto | Aprovada | 17 testes Python, 7 testes Vitest e checagem TypeScript. |

> **Decisão:** o contrato reconstruído é referência canônica operacional exclusivamente para o desenvolvimento e a validação interna do MVP. A promoção de produção continua bloqueada, pois o JSON original não foi recuperado e os módulos de segurança, persistência e pipeline real ainda não passaram por seus próprios gates.
