# SEM-DUR-008 — Política Proposta 001: Duração

## Estado e finalidade

Esta é uma proposta não executável para a `SEM-DUR-008`. Ela existe para viabilizar decisão humana e não autoriza registro, classificador, integração, allowlist ou produção.

## Proposta A — Conservadora, unitária e sem valores retidos

A regra poderá emitir `duration_candidate` somente quando todos os critérios abaixo forem verdadeiros.

| Critério | Proposta A |
|---|---|
| Vocabulário fechado | Após normalização transitória NFKC, casefold, remoção de acentos e colapso de espaços: `duracao`, `duracao (horas)`, `duracao (minutos)`, `duracao (segundos)` ou `duracao (dias)` |
| Base numérica | Ao menos 10 números físicos finitos |
| Cobertura física | Todos os valores não ausentes são números físicos finitos; números armazenados como texto não contam |
| Fórmulas | Nenhuma fórmula é permitida |
| Datas | Nenhuma data reconhecida é permitida |
| Ambiguidade | Nenhum valor booleano, serial de data, timestamp, texto, vazio intermediário ou tipo físico divergente é permitido |
| Evidência | Somente `header_eligible`, contagens agregadas de números físicos, não ausentes, fórmulas e datas reconhecidas, além de indicador de ambiguidade |
| Saída | `semantic_type: duration_candidate` |
| Confiança | `0.80` |
| Revisão | Pergunta humana bloqueante |

Não há inferência de unidade pelo valor, magnitude, frequência, distribuição, formato visual ou posição. A regra classifica uma candidata a duração; não converte nem presume unidade de medida.

## Exclusões e precedência

O cabeçalho deve conter explicitamente a palavra `duracao`; `tempo`, `horas`, `minutos`, `segundos`, `dias`, `idade`, `prazo`, `intervalo`, `periodo`, `meses`, `anos`, `tempo de ciclo` e sinônimos livres são excluídos. A regra também não será emitida quando houver SEM-DATE-001, SEM-COMP-002, SEM-PCT-007, SEM-QTY-005 ou SEM-CURR-006 elegíveis para a mesma coluna.

`duration_candidate` poderá coexistir com a saída de qualidade e com candidatos semânticos não conflitantes, mas não tomará decisões automáticas de fato, dimensão, métrica, relacionamento, granularidade ou modelagem Power BI.

## Privacidade e controles preservados

O cabeçalho será normalizado somente em memória para derivar um booleano. Nenhum cabeçalho, valor, token, exemplo, valor mínimo ou máximo, média, distribuição, posição, título de aba, fórmula, formato de célula ou hash de conteúdo poderá ser persistido ou incluído em evidência.

O mascaramento existente de cabeçalhos e títulos de abas permanece controle independente. Esta proposta não autoriza inspeção de conteúdo nem altera a SEM-SENS-015.

## Pré-condições de ativação

Exigem-se aprovação explícita de Chris, gate de reconstrução, perfil agregado imutável, classificador determinístico, integração canônica guardada por catálogo, testes unitários e de pipeline, golden dataset sintético, SHA-256, calibração reproduzível e gate individual. A produção continua bloqueada.
