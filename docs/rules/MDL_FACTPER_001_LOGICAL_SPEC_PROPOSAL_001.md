# MDL-FACTPER-001 — Especificação Lógica Proposta 001

**Status:** não executável. Esta especificação não autoriza código.

## Perfil privado por aba

`PeriodicFactProfile` conterá somente `observed_row_count`, `eligible_temporal_column_count`, `distinct_period_count`, `eligible_measure_column_count`, `grain_available`, `basis` e razões agregadas necessárias à decisão. O acumulador processará valores em memória apenas para reconhecer período e elegibilidade; não os serializará nem os transportará entre camadas.

## Algoritmo proposto

1. Receber a hipótese de `grain` já validada no perfil draft.
2. Exigir pelo menos 20 linhas observadas.
3. Examinar tipagens semânticas de data e identificar campo temporal elegível sem expor seu nome.
4. Derivar e descartar buckets temporais para contar períodos distintos.
5. Contar medidas numéricas físicas elegíveis, excluindo booleanos, fórmulas e identificadores.
6. Emitir `fact_periodic_candidate` apenas quando todas as condições da Proposta A forem verdadeiras.
7. Projetar evidência agregada, confiança `0.70` e pergunta humana obrigatória no fragmento canônico de classificação de tabela.

## Invariantes

A saída não conterá valores, cabeçalhos, posições, títulos de abas, bucket de período, identificadores, hashes ou fórmulas. A classificação não é uma recomendação de relacionamento e não tem efeito automático no modelo Power BI.

## Matriz de calibração proposta

Os cenários golden incluirão: fato periódica positivo; sem granularidade; somente um período; sem medida; base abaixo do mínimo; e possível fato transacional. A ativação draft exige zero falsos positivos e zero falsos negativos nesses cenários controlados.
