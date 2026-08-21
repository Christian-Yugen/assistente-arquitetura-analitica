# MDL-FACTPER-001 — Proposta de Política 001

**Status:** proposta não executável, pendente de aprovação explícita de Chris.  
**Escopo oficial recuperado:** classificação por aba, P0, dependente de `grain`, com saída `classification_or_table`.

## Objetivo

Produzir uma hipótese conservadora de **fato periódica**. A hipótese descreve uma tabela que tende a registrar um estado ou medida de negócio por entidade e por período de referência; não cria fatos, dimensões, chaves ou relacionamentos, e nunca substitui a validação humana.

## Proposta A — recomendada

A aba recebe a classificação `fact_periodic_candidate` somente quando todos os sinais abaixo convergirem: existe uma hipótese de granularidade válida; há ao menos 20 linhas observadas; existe um campo temporal reconhecido por tipagem semântica; o profiling transitório identifica ao menos dois períodos de referência distintos; e há ao menos uma medida física numérica não booleana, não fórmula e não identificadora. A classificação tem confiança inicial de `0.70` e gera uma pergunta obrigatória para que a pessoa confirme se cada linha representa o estado ou a medida de uma entidade em um período.

O perfil pode reter exclusivamente contagens agregadas de linhas, períodos distintos, colunas temporais elegíveis, medidas elegíveis e razões de completude. Valores, cabeçalhos, posições, títulos de abas, nomes de entidades, hashes e buckets de períodos são descartados antes da saída canônica.

## Exclusões e limites

A regra não classifica uma aba sem granularidade, sem campo temporal reconhecido, sem medida elegível, com menos de 20 linhas, com apenas um período observado ou quando houver sinais de fato transacional mais específicos em regra posterior. Não infere periodicidade por nome de aba, não pressupõe mês, ano ou calendário fiscal e não tenta corrigir dados.

## Alternativa B — não recomendada

Emitir apenas uma pergunta genérica para qualquer aba que contenha data e número. Essa opção reduz o risco de classificação, mas é pouco produtiva e não aproveita a dependência de granularidade recém-validada.

## Condição de autorização

Após aprovação explícita de Chris, a implementação será restrita ao perfil draft e exigirá gate de reconstrução, testes unitários e de privacidade, golden dataset assinado, calibração reprodutível, gate individual e sincronização de catálogo e indicadores. Produção continua bloqueada.
