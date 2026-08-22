# SEM-RESP-012 — Política Proposta 001: Responsável

## Estado e finalidade

Esta é uma proposta **não executável** para a `SEM-RESP-012`. Ela estabelece uma hipótese conservadora de coluna de responsabilidade para revisão humana e não autoriza perfil, classificador, registro, contrato, pipeline, allowlist, testes executáveis, calibração ou produção.

## Proposta A — Responsabilidade textual explícita por cabeçalho fechado

A regra poderá emitir `responsible_candidate` somente quando todos os critérios a seguir forem atendidos.

| Critério | Proposta A |
|---|---|
| Vocabulário fechado | Após normalização transitória NFKC, casefold, remoção de acentos e colapso de espaços: exatamente `responsavel` |
| Base mínima | Pelo menos 10 observações não ausentes |
| Tipo físico | Todos os valores não ausentes são textos físicos não vazios; números, datas, booleanos e seriais não são permitidos |
| Fórmulas | Nenhuma fórmula é permitida |
| Datas | Nenhuma data reconhecida é permitida |
| Cardinalidade | Entre 2 e 50 valores distintos agregados e `distinct_ratio <= 0.90` |
| Evidência | Apenas booleanos e contagens agregadas de presença, textos físicos, distintos, fórmulas, datas reconhecidas e ambiguidades |
| Saída | `semantic_type: responsible_candidate` |
| Confiança | `0.70` |
| Revisão | Pergunta humana bloqueante |

A proposta não interpreta, grava, compara ou valida os rótulos de responsabilidade. Portanto, não identificará pessoas, áreas, equipes, cargos, proprietários, gestores, autores ou papéis a partir dos valores; o cabeçalho fechado e sinais estruturais agregados são os únicos fatores autorizados.

## Exclusões e precedência

`responsaveis`, `dono`, `owner`, `gestor`, `supervisor`, `usuario`, `autor`, `analista`, `equipe`, `area`, `departamento`, `nome`, `descricao`, `status`, textos livres e qualquer cabeçalho não exatamente incluído no vocabulário permanecem excluídos. A regra também não será emitida com menos de duas ou mais de cinquenta responsabilidades agregadas, razão de distintos acima de `0.90`, fórmula, data reconhecida, texto vazio, tipo físico divergente ou qualquer ambiguidade estrutural.

`responsible_candidate` não cria nem confirma uma dimensão de pessoa, área ou equipe, e não decidirá chaves, granularidade, relacionamentos, métricas, autoridade, titularidade, classificação de dado pessoal ou tratamento de dados. A `SEM-SENS-015` e o mascaramento existente continuam independentes e não podem ser substituídos por esta regra.

## Privacidade e controles preservados

O cabeçalho será avaliado apenas transitoriamente para derivar `header_eligible`. O perfil proposto não reterá valores, rótulos, cabeçalhos normalizados, tokens, exemplos, frequências por rótulo, ordem, posições, títulos de abas, formatos de célula, fórmulas ou hashes de conteúdo.

O mascaramento de CPF, e-mail, nomes e títulos de abas continua obrigatório e independente. A proposta não infere que uma coluna contém pessoa identificável nem altera a `SEM-SENS-015`; eventuais sinais de sensibilidade permanecem segregados em `sensitivity_classifications`.

## Pré-condições de ativação

Exigem-se aprovação explícita de Chris para a Proposta A, gate de reconstrução, perfil agregado imutável, classificador determinístico, registro semântico, integração canônica guardada por catálogo, testes unitários e de pipeline, golden dataset sintético, SHA-256, calibração reproduzível e gate individual de calibração. A produção permanece bloqueada.
