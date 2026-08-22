# SEM-LOC-011 — Política Proposta 001: Localização

## Estado e finalidade

Esta é uma proposta **não executável** para a `SEM-LOC-011`. Ela estabelece uma hipótese deliberadamente conservadora para revisão humana e não autoriza perfil, classificador, registro, contrato, pipeline, allowlist, testes executáveis, calibração ou produção.

## Proposta A — Localização textual explícita por cabeçalho fechado

A regra poderá emitir `location_candidate` somente quando todos os critérios a seguir forem atendidos.

| Critério | Proposta A |
|---|---|
| Vocabulário fechado | Após normalização transitória NFKC, casefold, remoção de acentos e colapso de espaços: exatamente `cidade`, `municipio`, `pais`, `regiao` ou `localizacao` |
| Base mínima | Pelo menos 10 observações não ausentes |
| Tipo físico | Todos os valores não ausentes são textos físicos não vazios; números, datas, booleanos e seriais não são permitidos |
| Fórmulas | Nenhuma fórmula é permitida |
| Datas | Nenhuma data reconhecida é permitida |
| Cardinalidade | Entre 2 e 50 valores distintos agregados e `distinct_ratio <= 0.90` |
| Evidência | Apenas booleanos e contagens agregadas de presença, textos físicos, distintos, fórmulas, datas reconhecidas e ambiguidades |
| Saída | `semantic_type: location_candidate` |
| Confiança | `0.75` |
| Revisão | Pergunta humana bloqueante |

A proposta não interpreta, grava, geocodifica ou valida rótulos de localização. Portanto, não inferirá país, município, cidade, região, endereço, CEP, coordenada, unidade federativa, hierarquia territorial ou domínio geográfico a partir dos valores; o cabeçalho fechado e sinais estruturais agregados são os únicos fatores autorizados.

## Exclusões e precedência

`estado`, `uf`, `endereco`, `logradouro`, `bairro`, `cep`, `latitude`, `longitude`, `coordenada`, `unidade`, `responsavel`, `categoria`, `status`, `situacao`, `nome`, `descricao`, textos livres e qualquer cabeçalho não exatamente incluído no vocabulário permanecem excluídos. `estado` e `uf` não entram nesta proposta porque são ambíguos em relação ao domínio e ao vocabulário já reservado à `SEM-STATUS-009`; seu tratamento exigirá política independente.

A regra também não será emitida com menos de duas ou mais de cinquenta localidades agregadas, razão de distintos acima de `0.90`, fórmula, data reconhecida, texto vazio, tipo físico divergente ou qualquer ambiguidade estrutural. `location_candidate` não decidirá automaticamente endereço, dimensão geográfica, relacionamento, granularidade, chave, métrica, entidade ou taxonomia territorial.

## Privacidade e controles preservados

O cabeçalho será avaliado apenas transitoriamente para derivar `header_eligible`. O perfil proposto não reterá valores, rótulos, cabeçalhos normalizados, tokens, exemplos, frequências por rótulo, ordem, posições, títulos de abas, formatos de célula, fórmulas ou hashes de conteúdo.

O mascaramento de CPF, e-mail, nomes e títulos de abas continua obrigatório e independente. A proposta não altera a `SEM-SENS-015`; eventual sinal de sensibilidade permanece segregado em `sensitivity_classifications`.

## Pré-condições de ativação

Exigem-se aprovação explícita de Chris para a Proposta A, gate de reconstrução, perfil agregado imutável, classificador determinístico, registro semântico, integração canônica guardada por catálogo, testes unitários e de pipeline, golden dataset sintético, SHA-256, calibração reproduzível e gate individual de calibração. A produção permanece bloqueada.
