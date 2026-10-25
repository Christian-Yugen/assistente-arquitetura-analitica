# Explicação de Amostra Insuficiente — 001

**Estado:** melhoria de explicação no perfil draft; não reduz limiares de regra, não cria classificação estrutural e não promove produção.

## Regra de apresentação

Quando um diagnóstico não emitir perguntas, classificações semânticas, relacionamentos, métricas ou tabelas propostas e uma ou mais abas tiverem menos de **dez linhas observadas**, a interface deverá explicar o limite usando somente contagens agregadas. A explicação nunca exibirá valores, títulos, posições, pares, exemplos ou conteúdo do workbook.

## Justificativa analítica

Com menos de dez observações, medidas como distintividade, cardinalidade, consistência temporal, distribuição numérica e estabilidade de categoria são frágeis. Por isso, o motor mantém seus limiares conservadores e não transforma uma amostra curta em hipótese de dimensão, fato, chave, relacionamento ou métrica.

| Elemento exibido | Forma permitida |
|---|---|
| Motivo | Intervalo agregado de linhas observadas e limiar mínimo de dez. |
| Risco | Possibilidade de conclusões instáveis por evidência limitada. |
| Próxima ação | Usar ao menos dez registros não vazios em cada aba relevante, com estrutura e colunas efetivamente preenchidas. |
| Limites | Não relaxar regras, não fabricar hipótese estrutural, não liberar produção. |

## Critério de aceitação

A explicação será mostrada somente quando a ausência de saídas de modelagem coincidir com amostra insuficiente. Se já houver perguntas ou hipótese emitida, a interface não deverá substituir o diagnóstico real por esse aviso.
