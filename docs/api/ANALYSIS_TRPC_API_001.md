# ANALYSIS-TRPC-API-001 — API de Análise do MVP Draft

A interface de servidor utiliza tRPC em `/api/trpc`. Os procedimentos de análise são `protectedProcedure`: o proprietário autenticado é obtido no contexto de sessão e não é aceito como parâmetro controlável pelo cliente. O contrato de entrada é validado por Zod no servidor antes do processamento.

| Procedimento | Tipo | Entrada | Resultado | Isolamento |
|---|---|---|---|---|
| `analysis.listProjects` | Query | Sem parâmetros. | Projetos e versões do proprietário. | Consulta filtrada por `ctx.user.id`. |
| `analysis.getDiagnostic` | Query | `{ diagnosticId: UUID }`. | Diagnóstico canônico persistido. | Consulta por diagnóstico e proprietário; retorna `NOT_FOUND` se ausente. |
| `analysis.analyzeWorkbook` | Mutation | Nome de projeto, objetivo, nome do arquivo, MIME e base64. | `{ projectId, diagnosticId, version }`. | Criação, atualização e leitura sempre no proprietário autenticado. |

O arquivo é aceito apenas quando atende às validações de `.xlsx`, MIME, base64, assinatura ZIP, máximo de 25 MB e abertura real como workbook legível, com 1 a 10 abas. A mutation retorna `BAD_REQUEST` para falha de upload conhecida e `INTERNAL_SERVER_ERROR` com mensagem genérica para falhas de processamento. Mensagens internas, conteúdo do arquivo e detalhes de exceção não são devolvidos ao cliente.

O resultado persistido é um JSON compatível com `PM-MVP-PBI-CON-001`, versão incremental dentro do projeto. A exportação no cliente consulta o diagnóstico por esse mesmo caminho owner-scoped; não existe endpoint público para download da planilha nem para acessar diagnósticos de terceiros.

## Limites de API no perfil atual

A API não oferece exclusão física do objeto de armazenamento, interpretação semântica por LLM, proposta dimensional completa, exportação PDF ou operação administrativa de bypass de proprietário. Essas ausências são limites deliberados do draft, e não rotas ocultas ou funcionalidades parcialmente ativadas.
