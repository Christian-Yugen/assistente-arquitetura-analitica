# Gate QLT-EMPTYCOL-003-RECONSTRUCTION-001

## Decisão

**Aprovado por Chris para reconstrução, especificação e implementação exclusivamente draft.** A autorização é a opção **A**: detectar coluna inteiramente vazia quando todas as células das linhas de dados não inteiramente vazias forem nulas/vazias ou texto composto somente por espaços.

## Evidência de origem

| Item | Evidência |
|---|---|
| Identificador, título, prioridade e escopo | `official-rule-blueprint-95.json` |
| Dependência de profiling e saída finding | `INVENTARIO_QLT_001_006.md` |
| Fonte materializada de política | Ausente na cópia atual; reconstrução declarada |
| Decisão humana | Chris aprovou a opção A nesta continuidade |

## Limites obrigatórios

1. `0`, `false`, datas, números, fórmulas e sentinelas não são vazios.
2. Linhas inteiramente vazias são excluídas da avaliação.
3. A regra não exclui nem altera colunas e não infere a relevância de negócio.
4. Evidências são somente agregadas, com aba anonimizada e coluna sanitizada.
5. A regra permanece fora da allowlist até golden dataset, calibração, testes de privacidade e gate de ativação.

## Critérios de passagem ao gate de calibração

O próximo gate somente poderá habilitar a regra no draft após implementação determinística, testes unitários e contratuais, fixture golden sem valores brutos, manifesto SHA-256, relatório de TP/FP/FN e regressão integral aprovada. Este gate **não autoriza produção**.
