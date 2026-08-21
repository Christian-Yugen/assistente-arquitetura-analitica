# Gate de Reconstrução — MDL-FACTPER-001

**ID do gate:** `MDL-FACTPER-001-RECONSTRUCTION-AUTHORIZATION-001`  
**Estado:** aprovado para implementação draft controlada  
**Decisor:** Chris  
**Decisão:** Proposta A aprovada em 21 de agosto de 2026.

## Escopo autorizado

Implementar uma hipótese `fact_periodic_candidate` por aba apenas quando houver granularidade disponível, pelo menos 20 linhas observadas, campo temporal reconhecido, dois ou mais períodos derivados transitoriamente e medida física numérica elegível. A saída terá confiança inicial de `0.70` e pergunta humana obrigatória.

## Controles obrigatórios

O perfil e a projeção canônica não podem reter valores, cabeçalhos, posições, títulos de abas, identificadores, hashes, fórmulas ou buckets temporais. A regra não poderá criar fatos, dimensões, chaves ou relacionamentos; não poderá ser ativada fora do perfil draft; e exigirá teste unitário, golden dataset assinado, calibração reprodutível, gate individual e allowlist explícita antes da execução.

## Limites de produção

Esta autorização não promove a regra a produção, não remove os bloqueios do Gate MVP 1.0 e não autoriza nenhuma regra diferente da MDL-FACTPER-001.
