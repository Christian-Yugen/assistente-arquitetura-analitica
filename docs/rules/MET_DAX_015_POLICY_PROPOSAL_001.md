# MET-DAX-015 — Proposta A de Política 001

## Mudança de escopo autorizada

Chris autorizou a **Opção B** para que seja analisada uma política específica de DAX. Essa autorização permite este documento e seus controles; ela **não** aprova código executável, alteração de contrato, geração de DAX, allowlist, golden, calibração ou produção.

## Saída draft proposta

Uma futura implementação poderá produzir somente um **template DAX abstrato e não executável**, vinculado a exatamente uma fórmula conceitual previamente confirmada por uma pessoa. O template deverá empregar somente tokens estáveis, como `[CONFIRMED_MEASURE]`, e padrões de agregação aprovados. Ele não poderá usar cabeçalhos, valores, nomes de abas, identificadores de colunas, posições, pares, frequências ou qualquer texto do workbook.

> Exemplo de formato permitido: `SUM([CONFIRMED_MEASURE])`. O token é uma lacuna humana; não representa seleção automática de campo.

## Condição e salvaguardas propostas

A futura regra só poderá emitir um template quando houver exatamente uma fórmula conceitual elegível, uma confirmação humana explícita de intenção, granularidade única definida e nenhum sinal de sensibilidade, fórmula de origem, classificação indefinida, fato sem grão, conflito ou ambiguidade. O mecanismo não executará nem validará DAX contra modelos, não chamará fontes externas e não aceitará texto DAX arbitrário como entrada.

## Limites de segurança e privacidade

O template não definirá medida, entidade, tabela, relacionamento, unidade, população, período, filtro, agregação contextual, convenção de sinal ou arredondamento. Ele não produzirá Power Query/M, não persistirá conteúdo privado e exigirá validação humana bloqueante antes de qualquer uso. A evidência continuará limitada a flags e contagens agregadas.

## Autorização ainda necessária

Esta Proposta A exige aprovação explícita de Chris quanto ao seu texto e uma autorização posterior, também explícita, para qualquer perfil, classificador, contrato, pipeline, allowlist, teste executável, golden, calibração ou emissão de template DAX. **Produção permanece bloqueada.**
