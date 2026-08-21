# SEM-DATE-001 — Especificação lógica proposta 001

**Estado:** não executável; depende da autorização da política proposta.  
**Versão pretendida:** `0.1.0-provisional.1`.  
**Escopo:** uma coluna por avaliação.

## Contrato de entrada e saída proposto

O profiler receberá valores de coluna e classificará cada valor transitoriamente como ausente, data física, texto ISO válido, texto pt-BR hífen válido, texto pt-BR barra válido ou não reconhecido. O perfil imutável `SemanticDateProfile` expõe somente `non_missing_count`, `physical_date_count`, `iso_text_count`, `br_hyphen_text_count`, `br_slash_text_count`, `recognized_date_count`, `recognized_date_ratio` e `basis`; ele não aceita ou serializa valores, cabeçalhos, posições, exemplos ou títulos de aba.

O classificador recebe apenas `column_id` interno e o perfil agregado. Quando a base for menor que 10 ou a razão reconhecida for inferior a 1,0, não produz classificação. Caso contrário, devolve um registro `semantic_type = "date_generic"`, confiança moderada, evidência agregada e uma pergunta humana não bloqueante.

## Projeção canônica proposta

O fragmento retornado pelo motor será estendido com uma coleção opcional `semantic_classifications`, preservando `findings` e `questions` existentes. Cada registro terá `classification_id`, `semantic_type`, `confidence`, `evidence`, `rule_id`, `rule_version`, `affected_entities`, `created_at` e a pergunta vinculada será mantida na coleção canônica de questions. Não haverá conteúdo bruto, cabeçalho ou valor na projeção.

| Etapa | Operação determinística |
|---|---|
| 1 | Ignorar ausências pelo classificador privado já utilizado em profiling. |
| 2 | Contar `date` e `datetime` físicos não booleanos como datas reconhecidas. |
| 3 | Para texto, aplicar somente `strip`, exigir uma das três gramáticas autorizadas e validar o calendário com parser determinístico. |
| 4 | Contar qualquer outro valor físico como não reconhecido, sem registrar seu conteúdo. |
| 5 | Calcular a razão `recognized_date_count / non_missing_count`, com zero quando a base for vazia. |
| 6 | Emitir `date_generic` somente com base de pelo menos 10 e razão exatamente 1,0. |
| 7 | Projetar a classificação e pergunta humana no contrato sem transportar dados brutos. |

## Invariantes

O algoritmo não interpreta serial de Excel, formato visual, locale automático, timezone, hora, granularidade, periodicidade ou contexto de negócio. Ele não converte texto para data, não corrige valores, não altera a planilha e não emite classificação parcial. A QLT-BADDATE-006 continua responsável por sinalizar candidatos estritos inválidos; a SEM-DATE-001 apenas classifica colunas integralmente reconhecidas.

## Casos previstos para calibração

| Caso | Resultado esperado |
|---|---|
| 10 datas físicas | Classificação `date_generic`, confiança moderada e pergunta humana. |
| 10 textos ISO válidos; 10 textos pt-BR hífen válidos; 10 textos pt-BR barra válidos | Classificação em cada cenário. |
| Mistura de datas físicas e textos válidos autorizados | Classificação. |
| Nove valores reconhecidos, um texto inválido, timestamp textual, número serial, booleano, fórmula ou valor não reconhecido | Sem classificação. |
| Perfil serializado | Não contém valor, cabeçalho, posição, exemplo ou título de aba. |
