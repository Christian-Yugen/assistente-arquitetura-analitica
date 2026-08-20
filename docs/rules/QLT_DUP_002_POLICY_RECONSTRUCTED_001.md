# QLT-DUP-002 — Política Reconstruída de Linhas Duplicadas

**Versão candidata:** `0.1.0-reconstructed.1`.
**Estado:** autorizada por Chris para especificação e implementação draft; permanece não executável até o gate de calibração próprio.

## Origem, objetivo e limite de decisão

O artefato materializado de política da `QLT-DUP-002` não está disponível no repositório. O blueprint oficial preserva, contudo, o identificador, o título, a prioridade `P0`, o escopo de aba e o propósito de detectar linhas totalmente duplicadas. Esta política reconstrói somente esse núcleo verificável, sob a alternativa **A** aprovada por Chris.

| Aspecto | Decisão reconstruída |
|---|---|
| Regra | `QLT-DUP-002` — Registros duplicados |
| Unidade de avaliação | Linha dentro de uma única aba |
| Condição | Duas ou mais linhas não vazias possuem a mesma assinatura técnica integral |
| Saída | Um finding agregado por aba elegível |
| Ação automática | Proibida: não remover, mesclar, corrigir ou escolher registros |
| Inferência de chave | Proibida: não avalia unicidade parcial, chave natural ou chave de negócio |

## Normalização técnica autorizada

A comparação mantém distinções de tipo e de conteúdo de negócio. Para células textuais, ela aplica somente Unicode `NFKC`, padronização de quebras de linha e remoção de espaços nas extremidades. A regra **preserva** caixa, acentuação, pontuação interna, zeros à esquerda e a diferença entre texto, número, data, booleano e nulo. Assim, uma linha somente é candidata quando todos os seus valores são tecnicamente iguais sem aproximação semântica.

Linhas inteiramente vazias são excluídas antes do cálculo. Células vazias em uma linha com conteúdo permanecem parte da assinatura e só correspondem a células vazias na mesma posição. Fórmulas são avaliadas por seu valor lido pelo workbook; o texto da fórmula não é persistido como evidência.

> Uma assinatura técnica repetida é evidência de duplicidade potencial, não prova de que um dos registros possa ser removido ou de que exista uma chave de negócio.

## Evidência, limiares e privacidade

O profiler pode usar assinaturas efêmeras em memória, mas o contexto, finding e banco retêm somente contagens agregadas, proporções, quantidade de grupos duplicados, tamanho máximo de grupo e identificador anonimizado da aba. Valores de células, assinaturas, hashes, números de linha, títulos brutos de aba e exemplos de registros são proibidos na saída persistida.

| Proporção de linhas não vazias em grupos duplicados | Severidade | Pergunta de validação |
|---|---|---|
| Maior que 0% e menor que 5% | Baixa | Não obrigatória |
| De 5% a menor que 20% | Média | Não obrigatória |
| Igual ou superior a 20% | Alta | Obrigatória |

A confiança-base é `0,92`. Ela é reduzida para `0,78` quando a aba possui somente duas linhas não vazias, pois a evidência é pequena, e para `0,82` quando o maior grupo possui mais de 100 linhas, pois o resultado pode refletir uma exportação repetida que exige investigação de processo. Não há aumento de confiança por heurística externa.

## Exclusões, governança e promoção

A regra não compara linhas entre abas, não tenta comparar subconjuntos de colunas, não faz fuzzy matching, não usa LLM, não consulta dicionários e não produz modelagem dimensional. A recomendação é apenas investigar o processo de origem e definir a ação de retenção ou deduplicação com o responsável de negócio.

A execução permanece bloqueada fora do perfil draft. A promoção exige implementação reproduzível, testes de privacidade, golden dataset, calibração, gate explícito e a remoção dos bloqueios aplicáveis do Gate MVP 1.0.
