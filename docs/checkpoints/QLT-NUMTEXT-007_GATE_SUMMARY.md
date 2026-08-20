# Resumo de Gates — QLT-NUMTEXT-007

| Gate | Escopo | Decisão | Estado de produção |
|---|---|---|---|
| G7.3 | Implementação isolada e testes Python | Aprovado para integração draft | Bloqueado |
| G7.4 | Ruleset, registro e fragmento de saída | Aprovado somente no ruleset draft | Bloqueado |
| G7.4-R1 | Revalidação contra contrato reconstruído e allowlist draft | Aprovado para MVP draft | Bloqueado |
| G7.5 | Golden dataset, calibração e fechamento | Bloqueado por pré-condições | Bloqueado |

A aprovação de G7.3 e G7.4 é **controlada e limitada**: ela permite que a regra participe do repositório e do ruleset `0.7.0-draft`, mas não habilita análise de uploads reais, conversão automática de dados ou promoção de ambiente. A QLT-NUMTEXT-007 só poderá sair de draft após calibração documentada, regressão cumulativa e recuperação do arquivo canônico da QLT-NULL-001.

As evidências verificadas nesta etapa incluem vinte e um testes do motor Python, sete testes Vitest e a checagem TypeScript sem erros. A revalidação G7.4-R1 cobre perfil agregado, contexto, executor, JSON Schema Draft 2020-12, modelos Pydantic, objeto raiz completo, linhagem de perguntas por aba e a allowlist integral de marcadores do modo draft. Os detalhes e caminhos exatos estão nos artefatos G7.3, G7.4, G7.4-R1 e G7.5.
