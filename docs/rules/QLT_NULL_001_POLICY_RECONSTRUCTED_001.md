# QLT-NULL-001 — Política Reconstruída de Nulos

**Versão candidata:** `0.1.0-reconstructed.1`.  
**Status:** rascunho para revisão de governança; **não executável**.

Esta política define uma regra de qualidade equivalente para revelar colunas parcialmente preenchidas. Ela foi criada depois da perda declarada da fonte original e não a substitui como artefato canônico. O objetivo é fornecer evidência agregada sobre ausência de dados antes de inferir fatos, dimensões, relacionamentos ou métricas.

| Classe observada | Tratamento | Justificativa |
|---|---|---|
| Célula estrutural nula (`None`) | Conta como ausente. | É ausência determinística no fluxo de leitura do workbook. |
| Texto em branco ou somente espaços | Conta como ausente. | É ausência explícita de conteúdo após normalização mínima. |
| `NaN` numérico | Conta como ausente. | É ausência numérica detectável sem reter valor bruto. |
| Sentinela textual, como `N/A`, `NA`, `null`, `unknown`, `0` ou `-` | Não conta nesta regra. | O significado depende do domínio; uma política específica é necessária. |
| Fórmula carregada como expressão | Não conta nesta regra. | Não é permitido inferir o resultado de uma fórmula sem política de cálculo aprovada. |

O denominador é o número de células observadas abaixo do cabeçalho para a coluna analisada. A regra só se aplica quando há ao menos uma célula ausente e uma não ausente. Assim, colunas totalmente vazias permanecem fora de escopo para evitar sobreposição com diagnósticos específicos de coluna vazia.

| Razão de ausência | Severidade | Tratamento de confiança |
|---|---|---|
| Maior que 0% e menor que 5% | Baixa | Confiança-base de 0,90, reduzida em amostras pequenas ou classes de ausência mistas. |
| De 5% a menor que 20% | Média | Confiança-base de 0,90, reduzida em amostras pequenas ou classes de ausência mistas. |
| Igual ou superior a 20% | Alta | Exige pergunta de validação quando a amostra tiver pelo menos 20 células observadas. |

As evidências permitidas são apenas contagens, proporção e distribuição por classe de ausência. Valores de células, títulos de abas originais e sentinelas textuais não são persistidos como evidência. A recomendação deverá solicitar a definição do significado de negócio da ausência e seu tratamento explícito antes da modelagem.

> A implementação continua bloqueada até que a especificação lógica, a matriz de testes e o baseline da reconstrução sejam aprovados pelo gate `QLT-NULL-RECONSTRUCTION-001`.
