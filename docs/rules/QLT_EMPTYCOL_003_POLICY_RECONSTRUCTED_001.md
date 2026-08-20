# QLT-EMPTYCOL-003 — Política Reconstruída de Colunas Vazias

**Versão candidata:** `0.1.0-reconstructed.1`.  
**Estado:** autorizada por Chris para especificação e implementação no perfil draft; não executável até o gate de calibração próprio.

## Origem, objetivo e limite de decisão

O inventário registra a `QLT-EMPTYCOL-003` como regra materializada, mas sua fonte de política não está presente nesta cópia do repositório. O blueprint oficial preserva o identificador, título **Colunas vazias**, prioridade `P1`, escopo de coluna e o objetivo de detectar colunas sem informação útil. Esta reconstrução se limita à **opção A**, aprovada por Chris, e não reivindica recuperação do artefato original.

| Aspecto | Decisão reconstruída |
|---|---|
| Regra | `QLT-EMPTYCOL-003` — Colunas vazias |
| Unidade de avaliação | Coluna dentro de uma aba |
| População avaliada | Linhas de dados não inteiramente vazias |
| Condição | Todas as células da coluna na população avaliada são nulas/vazias ou texto composto somente por espaços |
| Saída | Um finding agregado por coluna elegível |
| Ação automática | Proibida: não excluir, ocultar, renomear ou preencher colunas |

## Definição de vazio autorizada

Uma célula é considerada vazia somente quando seu valor é nulo, ausente ou um texto cujo conteúdo, após remoção de espaços nas extremidades, é vazio. Linhas inteiramente vazias são excluídas antes da avaliação. Valores `0`, `false`, datas, números, booleanos, texto não vazio e fórmulas **não** são classificados como vazios por esta política, mesmo se exigirem revisão em outra regra.

> Uma coluna totalmente vazia é uma evidência de estrutura sem informação observável no workbook, não uma autorização para removê-la. Ela pode ter papel técnico, previsto ou dependente de processo externo.

## Evidência, severidade e privacidade

O contexto, finding e persistência retêm somente o identificador anonimizado da aba, o identificador sanitizado da coluna, a quantidade de linhas de dados avaliadas e a contagem agregada de células vazias. Valores de células, números de linha, títulos brutos de aba, fórmulas e amostras são proibidos.

| Condição adicional | Severidade | Pergunta de validação |
|---|---|---|
| Coluna vazia com até 10 linhas de dados | Baixa | Não obrigatória |
| Coluna vazia com 11 a 100 linhas de dados | Média | Não obrigatória |
| Coluna vazia com mais de 100 linhas de dados | Alta | Obrigatória |

A confiança-base é `0,95`, reduzida para `0,80` quando há somente uma linha de dados não vazia, pois a evidência é mínima. Não há aumento de confiança por heurística semântica.

## Exclusões, governança e promoção

A regra não usa sentinelas, não interpreta fórmulas sem resultado, não compara colunas entre abas, não infere relevância de negócio, não usa LLM e não produz modelagem dimensional. Qualquer extensão para sentinelas, fórmulas ou regras de domínio exigirá nova política e novo gate.

A execução permanece bloqueada fora do perfil draft. A promoção exige implementação reproduzível, testes de privacidade, golden dataset, calibração, gate explícito e remoção dos bloqueios aplicáveis do Gate MVP 1.0.
