# MDL-FACTNOGRAIN-019 — Especificação Lógica Proposta 001

## Limites e entrada permitida

A futura regra receberá somente um perfil privado de aba com contagens e booleanos agregados: linhas observadas, quantidade de medidas numéricas físicas elegíveis, presença de sinais de fato, presença de hipótese de granularidade, presença de candidato dimensional, fórmulas, sensibilidade, temporalidade incompatível e ambiguidades. Cabeçalhos, valores, títulos de abas, posições, frequências individuais e exemplos são transitórios e proibidos no perfil persistível.

## Guardas determinísticas propostas

A emissão exige `observed_row_count >= 20`, `eligible_numeric_measure_count >= 1`, sinal agregado de fato presente e ausência de hipótese de granularidade. A emissão é bloqueada por fórmula, sinal sensível, candidato dimensional, sinal temporal incompatível ou qualquer ambiguidade. A regra não deduz nem escolhe granularidade.

## Saída proposta

Quando todas as guardas forem satisfeitas, a regra emitirá `fact_without_defined_grain_candidate`, confiança `0.75`, evidência apenas agregada e pergunta humana bloqueante para definir o grão antes de classificar a tabela. A regra não ativa produção, não cria relacionamento e não recomenda medida.

## Estado de autorização

Este documento é não executável e permanece bloqueado até aprovação específica de Chris para a Proposta A e gate de reconstrução formalizado.
