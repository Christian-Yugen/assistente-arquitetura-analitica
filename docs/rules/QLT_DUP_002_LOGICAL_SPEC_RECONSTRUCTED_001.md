# QLT-DUP-002 — Especificação Lógica Reconstruída

**Versão:** `0.1.0-reconstructed.1`
**Dependência:** `profiling`
**Saída primária:** finding agregado por aba

## Contrato de entrada

O executor recebe um `DuplicateRowsProfile` por aba. O perfil contém apenas `non_empty_row_count`, `duplicate_group_count`, `duplicate_row_count`, `largest_duplicate_group`, `duplicate_row_ratio` e sinalizadores de elegibilidade. Nenhuma sequência de células, assinatura, hash, índice de linha ou título bruto de aba integra o contrato de saída do profiler.

| Campo agregado | Regra de uso |
|---|---|
| `non_empty_row_count` | Denominador da proporção e critério mínimo de duas linhas |
| `duplicate_group_count` | Deve ser maior que zero para emitir finding |
| `duplicate_row_count` | Numerador da proporção afetada |
| `largest_duplicate_group` | Ajusta confiança e evidencia concentração |
| `duplicate_row_ratio` | Determina severidade |

## Algoritmo determinístico

1. O profiler percorre as linhas de cada aba no processo do servidor e descarta linhas inteiramente vazias.
2. Cada célula recebe uma representação técnica com tag de tipo. Textos passam somente pela normalização autorizada; os demais tipos preservam sua semântica de leitura.
3. O profiler agrupa assinaturas integrais de linha apenas em memória e calcula contagens agregadas por grupo.
4. A regra emite finding quando há pelo menos um grupo com duas ou mais linhas e calcula `duplicate_row_ratio = duplicate_row_count / non_empty_row_count`.
5. Em severidade alta, emite pergunta que pede confirmação de que as linhas repetidas representam eventos ou registros distintos antes de qualquer tratamento.

A recomendação derivada é: **“Investigar a origem das linhas integralmente repetidas e definir com o responsável de negócio se há duplicidade operacional antes de qualquer retenção ou deduplicação.”**

## Invariantes e testes exigidos

O executor não pode comparar subconjuntos de colunas, inferir chaves, usar similaridade aproximada, reter assinaturas, cruzar abas ou emitir ação corretiva. A matriz mínima inclui: grupo duplicado simples, linhas diferenciadas apenas por caixa, linhas diferenciadas apenas por acento, linhas vazias excluídas, nulos posicionais, tipos distintos com mesma apresentação visual, limiares de severidade e ausência de valores brutos no finding.

O finding deve declarar `rule_id`, versão, severidade, confiança, evidência agregada, recomendação derivada e pergunta quando aplicável. A regra não emite dimensão, fato, relacionamento, métrica ou qualquer decisão de modelagem dimensional.
