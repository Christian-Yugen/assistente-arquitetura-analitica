# MDL-FACTNOGRAIN-019 — Proposta de Política 001

## Proposta A — hipótese conservadora de fato sem granularidade definida

Uma aba será classificada como candidata a `fact_without_defined_grain_candidate` somente quando tiver pelo menos 20 linhas observadas, uma ou mais medidas numéricas físicas elegíveis, sinais de fato agregados e **nenhuma** hipótese de granularidade ativa. O resultado não confirma uma tabela fato nem cria uma granularidade: registra a ausência de granularidade evidenciada para validação humana.

As evidências serão exclusivamente agregadas: contagem de linhas, contagem de medidas elegíveis, presença agregada de sinais de fato e ausência agregada de hipóteses de granularidade. A regra não projeta valores, cabeçalhos, posições, títulos de abas, fórmulas, rótulos ou exemplos. Fórmulas, dados sensíveis, tabela dimensional candidata, menos de 20 linhas, sinais temporais incompatíveis e qualquer ambiguidade bloqueiam a emissão.

A hipótese proposta tem confiança 0,75 e inclui pergunta bloqueante para definição humana da granularidade. Produção permanece bloqueada.

## Estado

**Proposta A aprovada explicitamente por Chris.** Esta aprovação autoriza exclusivamente a formalização do gate de reconstrução. Não autoriza perfil, classificador, registro, contrato, pipeline, catálogo, teste, dataset golden, calibração ou ativação. A implementação continua dependente do gate de reconstrução e de autorização explícita posterior de Chris.
