# SEM-STATUS-009 — Política Proposta 001: Status

## Estado e finalidade

Esta é uma proposta não executável para a `SEM-STATUS-009`. Ela estabelece um limite de decisão conservador para apreciação humana e não autoriza classificador, registro, contrato, pipeline, allowlist ou produção.

## Proposta A — Status textual de baixa cardinalidade

A regra poderá emitir `status_candidate` somente quando todos os critérios a seguir forem atendidos.

| Critério | Proposta A |
|---|---|
| Vocabulário fechado | Após normalização transitória NFKC, casefold, remoção de acentos e colapso de espaços: `status`, `situacao` ou `estado` |
| Base mínima | Pelo menos 10 observações não ausentes |
| Tipo físico | Todos os valores não ausentes são textos físicos não vazios; números, datas, booleanos e seriais não são permitidos |
| Fórmulas | Nenhuma fórmula é permitida |
| Datas | Nenhuma data reconhecida é permitida |
| Cardinalidade | Entre 2 e 12 valores distintos agregados e `distinct_ratio <= 0.50` |
| Evidência | Apenas booleanos e contagens agregadas de presença, textos físicos, distintos, fórmulas, datas reconhecidas e ambiguidades |
| Saída | `semantic_type: status_candidate` |
| Confiança | `0.75` |
| Revisão | Pergunta humana bloqueante |

A proposta não interpreta nem grava os rótulos do status. Portanto, não inferirá semântica de valores como “ativo”, “concluído”, “cancelado” ou equivalentes; o cabeçalho fechado e os sinais estruturais agregados são os únicos fatores autorizados.

## Exclusões e precedência

`situacao atual`, `estado civil`, `status de pagamento`, `fase`, `etapa`, `categoria`, `tipo`, `resposta`, `nome`, `descricao`, textos livres e qualquer outro cabeçalho não exatamente incluído no vocabulário permanecem excluídos. A regra também não será emitida com menos de duas categorias agregadas, acima de 12 categorias agregadas, razão de distintos acima de 0,50, fórmula, data reconhecida, texto vazio, tipo físico divergente ou candidato de nome/descrição elegível.

`status_candidate` poderá coexistir com findings de qualidade e com classificações não conflitantes, mas não decidirá automaticamente estado de processo, métrica, relacionamento, entidade, chave, dimensão, granularidade ou tratamento de dados.

## Privacidade e controles preservados

O cabeçalho será avaliado apenas transitoriamente para derivar `header_eligible`. O perfil não reterá valores, rótulos, cabeçalhos normalizados, tokens, exemplos, frequências por rótulo, posições, títulos de abas, formatos de célula, fórmulas ou hashes de conteúdo.

O mascaramento de cabeçalhos e títulos de abas continua obrigatório e independente. A proposta não altera a SEM-SENS-015, e qualquer candidato de sensibilidade seguirá exclusivamente na coleção `sensitivity_classifications`.

## Pré-condições de ativação

Exigem-se aprovação explícita de Chris, gate de reconstrução, perfil agregado imutável, classificador determinístico, registro semântico, integração canônica guardada por catálogo, testes unitários e de pipeline, golden dataset sintético, SHA-256, calibração reproduzível e gate individual de calibração. A produção permanece bloqueada.
