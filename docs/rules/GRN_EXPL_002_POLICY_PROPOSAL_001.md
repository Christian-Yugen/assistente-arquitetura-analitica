# GRN-EXPL-002 — Política Proposta 001: Chave explícita

## Estado e finalidade

Esta é uma proposta **não executável** para a `GRN-EXPL-002`. Ela estabelece uma hipótese de granularidade deliberadamente conservadora e não autoriza perfil, classificador, registro, contrato, pipeline, allowlist, testes executáveis, calibração ou produção.

## Proposta A — Hipótese de chave explícita única por aba

A regra poderá emitir uma hipótese `explicit_key_candidate` somente quando todos os critérios a seguir forem atendidos para **exatamente uma** coluna elegível na aba.

| Critério | Proposta A |
|---|---|
| Vocabulário fechado | Após normalização transitória NFKC, casefold, remoção de acentos e colapso de espaços: exatamente `id`, `chave` ou `key` |
| Elegibilidade | A coluna deve ter classificação semântica prévia de identificador e não pode ser classificada como sensível, descrição ou data |
| Base mínima | Pelo menos 20 linhas observadas na aba |
| Completude | `non_missing_count == observed_row_count` |
| Unicidade | `distinct_non_missing_count == observed_row_count` |
| Fórmulas | Nenhuma fórmula é permitida na coluna candidata |
| Ambiguidade | Exatamente um candidato pode atender à condição; zero ou dois ou mais candidatos bloqueiam a saída |
| Evidência | Apenas booleanos e contagens agregadas de linhas, completude, distintos, fórmulas, candidatos e ambiguidades |
| Saída | Hipótese de granularidade `explicit_key_candidate` |
| Confiança | `0.85` |
| Revisão | Pergunta humana bloqueante |

A hipótese não declara chave primária, não altera dados, não cria relacionamento e não substitui validação humana. O motor não revelará nem registrará o cabeçalho ou os valores da coluna; a decisão humana é necessária para confirmar se a coluna candidata representa o identificador único da linha no contexto de negócio.

## Exclusões e precedência

`codigo`, `codigo cliente`, `numero`, `sequencia`, `registro`, `cpf`, `email`, `chave composta`, `id cliente`, `id produto`, qualquer cabeçalho fora do vocabulário fechado e qualquer coluna sem classificação semântica de identificador permanecem excluídos. Fórmulas, datas, descrições, colunas sensíveis, campos com ausências, duplicidades, menos de 20 linhas ou mais de um candidato elegível também bloqueiam a hipótese.

A `GRN-COMP-001` permanece independente: esta proposta não combina colunas e não avalia pares. A saída `explicit_key_candidate` pode coexistir com findings de qualidade e classificações semânticas não conflitantes, mas não promove automaticamente granularidade, relacionamento, dimensão, fato ou métrica.

## Privacidade e controles preservados

O cabeçalho será avaliado apenas transitoriamente para derivar `header_eligible`. O perfil proposto não reterá valores, cabeçalhos normalizados, rótulos, tokens, exemplos, frequências por valor, posições, identificadores de coluna, títulos de aba, fórmulas ou hashes de conteúdo.

O mascaramento de CPF, e-mail, nomes e títulos de abas continua obrigatório e independente. Colunas classificadas como sensíveis são exclusões rígidas; esta regra não modifica a `SEM-SENS-015` nem a coleção `sensitivity_classifications`.

## Pré-condições de ativação

Exigem-se aprovação explícita de Chris para a Proposta A, gate de reconstrução, perfil agregado imutável, classificador determinístico, registro de granularidade, integração canônica guardada por catálogo, testes unitários e de pipeline, golden dataset sintético, SHA-256, calibração reproduzível e gate individual de calibração. A produção permanece bloqueada.
