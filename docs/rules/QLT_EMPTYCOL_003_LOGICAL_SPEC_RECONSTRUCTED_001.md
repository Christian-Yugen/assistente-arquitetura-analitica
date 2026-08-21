# QLT-EMPTYCOL-003 — Especificação Lógica Reconstruída

**Regra:** `QLT-EMPTYCOL-003`  
**Versão:** `0.1.0-reconstructed.1`  
**Política vinculada:** `QLT_EMPTYCOL_003_POLICY_RECONSTRUCTED_001.md`  
**Escopo:** coluna, por aba anonimizada, no estágio `quality`.

## Entradas e pré-condições

| Entrada agregada | Uso | Proibido persistir |
|---|---|---|
| Contagem de linhas de dados não inteiramente vazias | Base de avaliação e confiança | Índices ou conteúdo das linhas |
| Contagem de células vazias segundo a política | Identificar coluna integralmente vazia | Valores de célula |
| Identificador sanitizado de coluna e aba anonimizada | Localizar o finding | Título bruto da aba |

A avaliação é elegível somente quando a aba possui pelo menos uma linha de dados não inteiramente vazia. A primeira linha é tratada como cabeçalho pelo profiler do MVP draft e não integra o denominador. A regra deve receber contexto agregado, sem coleções de valores de células.

## Algoritmo determinístico

1. O profiler exclui linhas inteiramente vazias e contabiliza as linhas de dados restantes.
2. Para cada coluna, contabiliza valores nulos/ausentes e textos que se tornam vazios após `strip()`.
3. Se a contagem de vazios for igual à quantidade de linhas de dados e essa quantidade for maior que zero, emite um finding para a coluna.
4. O finding inclui somente contagens, proporção `1.0`, aba anonimizada e coluna sanitizada.
5. A severidade segue a faixa de linhas da política; somente a faixa alta cria pergunta de validação.
6. A recomendação derivada orienta validar a finalidade da coluna antes de removê-la ou transformá-la. Não há mutação do workbook.

## Saída contratual

O adaptador canônico deve emitir `rule_id`, versão, severidade, confiança, localização no nível de coluna, evidência agregada, recomendação derivada e, quando aplicável, pergunta de validação. A saída não pode conter conteúdo de célula, número de linha, fórmulas, títulos brutos de aba ou sugestão de exclusão automática.

## Casos obrigatórios de teste

| Caso | Resultado esperado |
|---|---|
| Coluna integralmente `null` em aba com 20 linhas de dados | Finding médio |
| Coluna com somente espaços em aba com 5 linhas de dados | Finding baixo |
| Coluna com `0`, `false`, data ou fórmula | Sem finding |
| Coluna vazia em aba com mais de 100 linhas | Finding alto e pergunta |
| Aba sem linhas de dados | Sem finding |
| Contexto persistido | Sem valores brutos, fórmulas, índices ou títulos brutos |
