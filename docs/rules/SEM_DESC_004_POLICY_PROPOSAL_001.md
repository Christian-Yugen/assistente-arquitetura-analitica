# SEM-DESC-004 — Política Proposta A 001

## Objetivo e decisão solicitada

Esta proposta reconstrói de forma conservadora a `SEM-DESC-004 — Nome ou descrição` para o perfil draft. Ela não cria código executável, não altera o catálogo e não autoriza produção. A decisão solicitada a Chris é limitada à emissão de `name_or_description_candidate` quando os sinais agregados abaixo convergirem, sempre com revisão humana bloqueante.

## Condição proposta

O classificador só poderá emitir uma hipótese se todos os requisitos forem atendidos.

| Sinal privado agregado | Regra proposta |
|---|---|
| Cabeçalho elegível | Após normalização transitória, exatamente `nome`, `descricao` ou `descrição` |
| Base observada | Pelo menos 10 valores não ausentes |
| Cobertura textual física | 100% dos valores não ausentes são textos físicos; nenhum valor numérico, data, booleano ou serial Excel |
| Fórmulas | `formula_count = 0` |
| Distinção agregada | Pelo menos 2 valores distintos e razão de distintos de pelo menos 0,20 |
| Data reconhecida | `recognized_date_count = 0` |
| Resultado | `semantic_type: name_or_description_candidate` |
| Confiança | `0.70` |

Os sinais serão reduzidos a booleanos, contagens e razões. Nenhum texto, token, cabeçalho, valor, exemplo, posição, título de aba, formato de célula ou assinatura será persistido, projetado ou incluído em evidências.

## Exclusões e precedência

A saída fica bloqueada para cabeçalho fora do vocabulário, base insuficiente, fórmulas, tipos físicos mistos, datas reconhecidas, menos de dois valores distintos ou razão de distintos abaixo do limiar. Não haverá inferência por conteúdo, comprimento de texto, idioma, padrões de palavras, frequência, posição, domínio, título de aba ou formatação visual.

`SEM-ID-003`, `SEM-DATE-001`, `SEM-COMP-002`, `SEM-QTY-005`, `SEM-CURR-006`, `SEM-PCT-007`, `SEM-TARGET-013` e `SEM-ACTUAL-014` têm precedência por seus próprios bloqueios físicos. A hipótese desta regra pode coexistir com outra classificação semântica apenas quando ambas sobreviverem às respectivas exclusões; ela não altera, remove nem consolida classificações automaticamente.

O cabeçalho `nome` continuará a acionar `SEM-SENS-015` independentemente desta regra. A presença de `personal_data_candidate` não é suprimida, nem reduz sua confiança, e a revisão humana deverá validar os dois outputs em separado. O mascaramento preexistente permanece obrigatório e independente.

## Evidência, pergunta e limites

A evidência canônica conterá somente o identificador da regra, versão, base de sinais agregados, contagens, razões, exclusões satisfeitas e confiança. A pergunta bloqueante será:

> A coluna deve ser tratada como **nome ou descrição**, e, quando o cabeçalho for `nome`, há dado pessoal que exige a política aplicável?

A resposta humana é obrigatória antes de qualquer recomendação de dimensão, exposição, relacionamento, métrica ou transformação. A regra não determina entidade, chave, atributo descritivo, dimensão, qualidade do texto, idioma, dado pessoal real ou finalidade de tratamento.

## Testes e calibração exigidos antes da ativação

Se a proposta for aprovada, a implementação exigirá testes positivos para `Nome`, `Descrição` e `Descricao`; negativos para cabeçalho fora do vocabulário, base insuficiente, fórmula, tipo físico misto, data reconhecida, baixa distinção e ausência; prova de que nenhum conteúdo de entrada é projetado; golden dataset totalmente sintético; avaliador reprodutível de TP/FP/FN; SHA-256; gate individual de calibração; allowlist draft e regressões completas.

> Produção permanece bloqueada. A aprovação desta política somente habilita a formalização do gate de reconstrução; não autoriza código nem ativação.
