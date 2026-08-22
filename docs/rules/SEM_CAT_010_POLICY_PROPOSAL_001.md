# SEM-CAT-010 — Política Proposta 001: Categoria

## Estado e finalidade

Esta é uma proposta **não executável** para a `SEM-CAT-010`. Ela estabelece um limite de decisão deliberadamente conservador para apreciação humana e não autoriza perfil, classificador, registro, contrato, pipeline, allowlist, testes executáveis, calibração ou produção.

## Proposta A — Categoria textual explícita de baixa cardinalidade

A regra poderá emitir `category_candidate` somente quando todos os critérios a seguir forem atendidos.

| Critério | Proposta A |
|---|---|
| Vocabulário fechado | Após normalização transitória NFKC, casefold, remoção de acentos e colapso de espaços: exatamente `categoria` |
| Base mínima | Pelo menos 10 observações não ausentes |
| Tipo físico | Todos os valores não ausentes são textos físicos não vazios; números, datas, booleanos e seriais não são permitidos |
| Fórmulas | Nenhuma fórmula é permitida |
| Datas | Nenhuma data reconhecida é permitida |
| Cardinalidade | Entre 2 e 20 valores distintos agregados e `distinct_ratio <= 0.50` |
| Evidência | Apenas booleanos e contagens agregadas de presença, textos físicos, distintos, fórmulas, datas reconhecidas e ambiguidades |
| Saída | `semantic_type: category_candidate` |
| Confiança | `0.70` |
| Revisão | Pergunta humana bloqueante |

A proposta não interpreta, grava ou agrupa rótulos de categoria. Portanto, não inferirá categoria por nomes de produtos, unidades, classes, segmentos, famílias, estados, localidades, responsáveis ou outros valores; o cabeçalho fechado e sinais estruturais agregados são os únicos fatores autorizados.

## Exclusões e precedência

`categorias`, `classificacao`, `classe`, `grupo`, `segmento`, `familia`, `tipo`, `fase`, `etapa`, `status`, `situacao`, `estado`, `nome`, `descricao`, textos livres e qualquer cabeçalho não exatamente incluído no vocabulário permanecem excluídos. A regra também não será emitida com menos de duas ou mais de vinte categorias agregadas, razão de distintos acima de `0.50`, fórmula, data reconhecida, texto vazio, tipo físico divergente ou qualquer ambiguidade estrutural.

`category_candidate` poderá coexistir com findings de qualidade e classificações não conflitantes, mas não decidirá automaticamente uma taxonomia de negócio, domínio de categorias, dimensão, relacionamento, métrica, entidade, chave, granularidade ou tratamento de dados. Não se deve adicionar vocabulário aberto nem usar conteúdo de valores para reduzir ambiguidades.

## Privacidade e controles preservados

O cabeçalho será avaliado apenas transitoriamente para derivar `header_eligible`. O perfil proposto não reterá valores, rótulos, cabeçalhos normalizados, tokens, exemplos, frequências por rótulo, ordem, posições, títulos de abas, formatos de célula, fórmulas ou hashes de conteúdo.

O mascaramento de CPF, e-mail, nomes e títulos de abas continua obrigatório e independente. A proposta não altera a `SEM-SENS-015`; qualquer candidato de sensibilidade seguirá exclusivamente na coleção `sensitivity_classifications`.

## Pré-condições de ativação

Exigem-se aprovação explícita de Chris para a Proposta A, gate de reconstrução, perfil agregado imutável, classificador determinístico, registro semântico, integração canônica guardada por catálogo, testes unitários e de pipeline, golden dataset sintético, SHA-256, calibração reproduzível e gate individual de calibração. A produção permanece bloqueada.
