# QLT-DUP-002-RECONSTRUCTION-AUTHORIZATION-001

**Data:** 20 de agosto de 2026.
**Decisão:** autorizado para reconstrução provisória e implementação draft; execução permanece bloqueada até calibração.

## Contexto e decisão humana

O checkpoint global registra a `QLT-DUP-002` como regra histórica de duplicidades, mas o artefato materializado de política/especificação não está disponível. Chris aprovou a alternativa **A**: detectar apenas linhas integralmente idênticas após normalização técnica, ignorando linhas inteiramente vazias e sem inferir chaves de negócio.

| Controle | Decisão |
|---|---|
| Fonte histórica indisponível | Preservar a perda e criar versão `0.1.0-reconstructed.1`, sem alegar recuperação canônica |
| Normalização | Técnica, delimitada e sem equivalência semântica |
| Chaves candidatas | Fora de escopo |
| Ação sobre linhas | Proibida |
| Dados pessoais e valores brutos | Proibidos em contexto, finding, pergunta e persistência |
| Produção | Bloqueada |

## Pré-requisitos para ativação draft

Antes de adicionar a regra à allowlist draft, o ciclo deve entregar implementação no servidor, perfil agregado, adaptação ao contrato canônico, testes positivos/negativos/de privacidade, fixture golden com manifesto verificável, calibração reprodutível, regressão integral e gate de calibração documentado.

> Esta autorização não corrige as referências históricas de namespace, não recupera o artefato original, não autoriza deduplicação de dados e não remove nenhum bloqueio do Gate MVP 1.0.
