# QLT-CATVAR-008 — Especificação Lógica Provisória

**Versão:** `0.1.0-provisional.1`  
**Dependência:** `profiling`  
**Saída primária:** `finding` agregado por coluna

## Contrato de entrada

O executor recebe um `CategoricalVariationProfile` por coluna, composto somente por contagens agregadas: número de textos observados, valores distintos, grupos de colisão, células afetadas, variantes máximas por grupo e sinalizadores de elegibilidade. O perfil não transporta valores de células, rótulos normalizados, exemplos nem nomes brutos de abas.

| Campo agregado | Regra de uso |
|---|---|
| `text_value_count` | Denominador da proporção afetada |
| `distinct_text_count` | Limite de elegibilidade de 100 |
| `collision_group_count` | Deve ser maior que zero |
| `affected_value_count` | Numerador da proporção afetada |
| `max_variants_in_group` | Ajusta a confiança |
| `high_cardinality` | Exclui a coluna do finding |

## Algoritmo determinístico

1. O profiler coleta valores textuais não vazios somente durante a execução em memória.
2. Para cada texto, aplica a normalização autorizada na política e conta grafias distintas por chave normalizada.
3. Um grupo existe quando uma chave possui duas ou mais grafias brutas distintas. O `affected_value_count` soma as ocorrências pertencentes a esses grupos.
4. A regra emite finding quando a coluna é elegível e possui pelo menos um grupo. A severidade deriva da proporção `affected_value_count / text_value_count`.
5. Em severidade alta, emite pergunta de validação que solicita confirmação de equivalência de negócio e definição de padrão de origem; nenhuma resposta altera retroativamente a versão atual.

A recomendação derivada é: **“Validar se as grafias tecnicamente similares representam a mesma categoria de negócio e, se confirmado, definir uma padronização na fonte ou dimensão controlada.”**

## Invariantes e exclusões

O executor não usa distância de edição, embeddings, LLM, fonética, pluralização, lematização, sinônimos ou listas implícitas. O arquivo de dicionário é opcional e deve estar vazio nesta versão. Se qualquer mapeamento for adicionado, a execução deve falhar até que uma versão de política e um novo gate o autorizem.

O finding deve declarar `rule_id`, severidade, confiança, evidência agregada, recomendação derivada e, quando aplicável, pergunta. A regra não emite proposta de dimensão, relacionamento, métrica ou decisão de modelagem dimensional.
