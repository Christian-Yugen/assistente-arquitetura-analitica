# MDL-DIMCAL-006 — Proposta de Política 001

**Regra:** `MDL-DIMCAL-006` — Dimensão calendário.  
**Estado:** proposta não executável; execução bloqueada.  
**Escopo oficial recuperado:** regra P0, por aba, na etapa `table_classification`, dependente de `grain` e com saída `classification_or_table`.

## Lacuna oficial e princípio de segurança

O blueprint oficial define a finalidade de classificar ou propor uma dimensão calendário, mas não materializa a condição, as exclusões, a confiança, as evidências, as perguntas ou a calibração. A política abaixo é uma proposta draft conservadora: não reconhece calendários com base em título de aba, cabeçalhos, valores textuais, formatos de identificador, regex ou conteúdo semântico não autorizado.

O objetivo é identificar uma estrutura temporal explícita que possa representar uma tabela de referência de dias. Quando os sinais não forem convergentes, a regra não deverá emitir candidato. Essa escolha reduz falso positivo e mantém a classificação ambígua sob validação humana.

## Proposta A — dimensão calendário candidata

Uma aba será classificada como `dimension_calendar_candidate` somente quando todas as condições forem satisfeitas: há granularidade válida; existem ao menos 20 linhas observadas; ao menos uma coluna de data física é integralmente reconhecida pelos formatos estritos autorizados; cada data reconhecida é distinta; as datas formam uma sequência diária contínua no perfil transitório; e não há medida numérica física elegível.

O teste de continuidade poderá ser feito somente durante o profiling: o perfil persistido reterá contagens agregadas de datas reconhecidas, datas distintas e transições diárias consecutivas, sem guardar datas, mínimos, máximos, valores, posições, cabeçalhos, títulos de aba ou hashes. A confiança inicial proposta é **0,75**. A emissão deverá incluir a pergunta humana obrigatória e bloqueante: **“Esta aba representa um calendário de referência, com uma linha por dia, usado para analisar outras tabelas?”**

| Elemento | Política proposta |
|---|---|
| Base mínima | 20 linhas observadas |
| Dependência | Hipótese de granularidade válida |
| Sinal temporal | Coluna física de data reconhecida integralmente |
| Unicidade temporal | Número de datas distintas igual ao número de datas reconhecidas |
| Continuidade | Todas as transições entre datas distintas são de um dia no perfil transitório |
| Exclusão de fato | Nenhuma medida numérica física elegível |
| Classificação | `dimension_calendar_candidate` |
| Confiança | `0.75` |
| Pergunta | Obrigatória e bloqueante |
| Saída | Fragmento canônico `classification_or_table` e evidência apenas agregada |

## Exclusões, privacidade e coexistência

Ficam excluídas abas sem granularidade, com menos de 20 linhas, sem data integralmente reconhecida, com repetição temporal, com qualquer lacuna entre dias distintos, com medida numérica física elegível, com fórmula nos sinais usados ou que exijam semântica derivada de texto. Ausência de candidato não é uma conclusão negativa e não bloqueia outras hipóteses draft por aba; a precedência canônica e a confirmação humana permanecem responsáveis por resolver concorrências.

## Alternativa B — série temporal sem continuidade

Uma alternativa seria aceitar datas únicas sem exigir continuidade. Ela amplia cobertura para calendários mensais, fiscais ou incompletos, mas aumenta o risco de confundir tabelas de eventos sem medidas e cadastros com vigência temporal. A Proposta A privilegia precisão; categorias temporais adicionais poderão ser consideradas em regras próprias e autorizadas.

## Condição de avanço

Esta proposta não autoriza perfil, classificador, registro, versão de contrato, integração de pipeline ou allowlist. O avanço exige aprovação explícita de Chris para a Proposta A, seguida de gate de reconstrução, testes unitários positivos/negativos/limítrofes, golden dataset assinado, avaliador reprodutível, calibração, gate individual e ativação exclusivamente no perfil draft. Produção permanece bloqueada.

## Referências internas

1. `artifacts/catalogs/official-rule-blueprint-95.json`, sequência 46, `MDL-DIMCAL-006`.
2. `artifacts/catalogs/rule-implementation-readiness-v1.json`, registro da `MDL-DIMCAL-006`.
3. `PM-MVP-PBI-001 v1.0` e `PM-MVP-PBI-REQ-001 v1.0`, pacote compartilhado do projeto.
