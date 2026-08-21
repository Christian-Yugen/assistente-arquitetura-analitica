# SEM-COMP-002 — Especificação Lógica Proposta 001

**Estado:** não executável; depende da aprovação da Política Proposta 001 e do gate de reconstrução.  
**Versão pretendida:** `0.1.0-provisional.1`.  
**Escopo:** uma coluna por avaliação.

## Contrato de entrada proposto

O futuro `SemanticCompetenceProfile` deverá ser um objeto imutável e agregado, derivado de sinais transitórios. Ele poderá expor somente `header_eligible`, `non_missing_count`, `recognized_date_count`, `recognized_date_ratio`, `formula_count` e uma versão de base. O cabeçalho será normalizado somente durante o profiling para obter o booleano `header_eligible`; nem o texto original nem o normalizado poderão ser serializados, registrados em logs ou projetados no diagnóstico.

Os sinais temporais deverão ser reutilizados da SEM-DATE-001, sem reinspecionar valores. O perfil de fórmulas também deverá expor apenas a contagem agregada já existente. Não há nova leitura de planilha, persistência de valores, dependência de formatação de célula ou regra de conversão.

## Algoritmo determinístico proposto

| Etapa | Operação |
|---|---|
| 1 | Normalizar o cabeçalho transitoriamente e definir `header_eligible` apenas para os três termos fechados da política. |
| 2 | Reutilizar os contadores e a razão de datas estritamente reconhecidas pela SEM-DATE-001. |
| 3 | Reutilizar `formula_count` do perfil agregado de consistência de fórmula. |
| 4 | Não emitir saída se o cabeçalho não for elegível, a base for menor que 10, a razão for diferente de `1.0` ou houver fórmula. |
| 5 | Emitir somente `semantic_type = "competence_date_candidate"` com confiança `0.85`, evidência agregada, versão da regra e entidades internas afetadas. |
| 6 | Projetar pergunta de confirmação humana bloqueante, sem valor, cabeçalho, posição, exemplo ou título de aba. |

## Projeção canônica proposta

A regra reutilizará exclusivamente a coleção canônica já existente `semantic_classifications`. Cada candidato deverá manter `semantic_type`, `confidence`, `evidence`, `rule_id`, `rule_version` e `affected_entities`. A pergunta vinculada será mantida em `questions` com `blocking: true`, `affected_modules: ["semantic_typing"]` e `affected_rule_ids: ["SEM-COMP-002"]`.

A SEM-COMP-002 não criará coleção nova, não emitirá `finding`, não modificará `sensitivity_classifications` e não alterará a saída da SEM-SENS-015. A coexistência com `date_generic` é permitida, pois a decisão humana é responsável por validar ou rejeitar a especialização de competência.

## Invariantes de privacidade e governança

O algoritmo não pode reter ou expor valores de célula, cabeçalho, título de aba, posição, amostra, serial de Excel, formato visual ou dados identificáveis. Ele não realiza inferência de período fiscal, competência contábil, origem do fato, timezone, granularidade ou calendário. A execução fica indisponível até que o catálogo contenha uma autorização draft explícita vinculada ao gate individual de calibração.

## Matriz de calibração planejada

| Cenário sintético | Resultado esperado |
|---|---|
| Cabeçalho `Competência`, 10 datas físicas reconhecidas e zero fórmulas | `competence_date_candidate`, confiança `0.85` e pergunta bloqueante. |
| Cabeçalho `Data de competência`, 10 textos estritos em formato autorizado e zero fórmulas | Classificação candidata. |
| Cabeçalho `data competencia`, mistura integral de datas físicas e textos estritos válidos | Classificação candidata. |
| Cabeçalho fora do vocabulário, base menor que 10, uma data não reconhecida ou uma fórmula | Sem classificação. |
| Perfil e diagnóstico serializados | Não contêm valores, cabeçalho, posições, exemplos ou títulos de aba. |
