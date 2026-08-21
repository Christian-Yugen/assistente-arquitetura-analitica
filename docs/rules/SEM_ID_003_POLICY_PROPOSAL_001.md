# SEM-ID-003 — Proposta de Política 001

**Regra:** `SEM-ID-003` — Identificador  
**Estado:** proposta não executável; implementação bloqueada.  
**Dependência:** qualidade.  
**Finalidade:** formar a fonte semântica controlada para a GRN-COMP-001.

## Lacuna recuperada

O blueprint oficial requer “evidências convergentes”, mas não materializa quais evidências, limites, exclusões, confiança ou saída. Esta proposta reconstrói uma alternativa draft deliberadamente conservadora. Ela não confirma chave de negócio, não interpreta domínio e não altera dados.

## Proposta A — identificador ou componente elegível

Uma coluna será classificada como `identifier` apenas quando houver, simultaneamente, um sinal nominal fechado e sinais estruturais privados. O sinal nominal será calculado transitoriamente a partir de um vocabulário fechado normalizado: `id`, `codigo`, `cod`, `chave`, `matricula`, `numero` e `num`; o cabeçalho original não será retido nem projetado. Os sinais estruturais serão: pelo menos 20 valores observados, cobertura não ausente de pelo menos 90%, tipo físico exclusivamente textual ou numérico, e diversidade de pelo menos 10% entre os valores não ausentes.

Colunas que atendam a todos os critérios serão emitidas como `identifier`, com confiança de **0,75**. Se a cobertura for 100% e a diversidade também 100%, a evidência registrará que a coluna é individualmente única; caso contrário, registrará somente que é componente elegível de identificador. Essa segunda condição é precisamente o que permite que a GRN-COMP-001 avalie pares sem presumir que cada componente seja uma chave individual.

São excluídos booleanos, datas, tipos mistos, fórmulas, colunas sensíveis, cobertura inferior a 90%, bases inferiores a 20, diversidade inferior a 10%, valores não finitos e qualquer inferência baseada em formato, regex, tamanho, prefixo ou conteúdo de valores. A saída sempre terá pergunta humana não bloqueante: “Esta coluna representa um identificador ou componente de identificador no contexto da aba?”.

| Elemento | Política proposta |
|---|---|
| Base mínima | 20 valores observados |
| Evidência nominal | Vocabulário fechado, normalizado e transitório |
| Cobertura mínima | 90% não ausente |
| Diversidade mínima | 10% de valores distintos entre não ausentes |
| Tipos aceitos | Texto ou número físico, sem mistura |
| Classificação | `identifier`, não confirmação de chave |
| Confiança | 0,75 |
| Saída | `semantic_classifications` existente, agregada e versionada |
| Pergunta | Não bloqueante; valida o papel de identificador |

## Alternativa B — somente unicidade individual

Uma alternativa ainda mais restritiva classificaria apenas colunas 100% completas e individualmente únicas. Ela reduz falsos positivos, mas não habilita a GRN-COMP-001 para componentes repetidos de uma chave composta, contrariando a finalidade da decisão A1.

## Limites de ativação

Nenhuma política nesta proposta autoriza código. A aprovação explícita de Chris deverá autorizar somente perfil, classificador, testes, golden dataset e calibração em draft; a ativação dependerá de gate individual posterior. Produção permanece bloqueada.
