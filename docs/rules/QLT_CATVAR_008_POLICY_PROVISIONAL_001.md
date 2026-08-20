# QLT-CATVAR-008 — Política Provisória de Variações de Categoria

**Versão candidata:** `0.1.0-provisional.1`.  
**Estado:** executável **somente no perfil draft**, após o gate `QLT-CATVAR-008-DRAFT-CALIBRATION-001`.

## Objetivo e escopo

A regra revela grupos de grafias textuais que se tornam tecnicamente equivalentes após uma normalização delimitada. Ela produz um **candidato à validação**, e nunca corrige células, funde categorias, reescreve o workbook ou declara equivalência semântica de negócio.

| Aspecto | Decisão provisória |
|---|---|
| Regra | `QLT-CATVAR-008` — Variações de categoria |
| Escopo | Coluna, após profiling do workbook |
| Entrada admitida | Valores textuais não vazios, avaliados em memória no servidor |
| Evidência persistida | Contagens agregadas, proporções, quantidade de grupos e máximo de variantes; nenhum valor textual bruto |
| Saída | Um finding por coluna elegível e pergunta de validação em severidade alta |
| Ação automática | Proibida: não há padronização, fusão, substituição nem escolha de rótulo canônico |

## Normalização técnica autorizada

O comparador provisório aplica, nesta ordem, normalização Unicode `NFKD`, remoção de marcas diacríticas, `casefold`, conversão de pontuação delimitadora em espaço e colapso de espaços. Assim, a regra pode apontar variações como maiúsculas/minúsculas, acentos, hifens e espaços múltiplos como um mesmo **candidato técnico**.

> A igualdade após normalização é uma evidência de grafia potencialmente relacionada, não uma conclusão de que as categorias possuem o mesmo significado de negócio.

Abreviações, siglas, singular/plural, distância de edição, sinônimos e aproximação fonética permanecem **fora da heurística automática**. Um dicionário versionado pode descrevê-los depois, mas inicia vazio em `artifacts/rules/QLT-CATVAR-008/provisional-domain-dictionary-v1.json`; qualquer preenchimento requer revisão de domínio, nova versão do artefato e gate próprio.

## Elegibilidade, limiares e exclusões

São elegíveis apenas colunas com ao menos dois valores textuais não vazios, duas grafias brutas distintas que normalizem para a mesma chave e até 100 valores distintos no perfil textual. Colunas de alta cardinalidade, sem colisão técnica ou com menos de dois textos permanecem fora de escopo, pois a regra não deve inferir categorias a partir de texto livre.

| Proporção de células afetadas por colisões técnicas | Severidade | Pergunta |
|---|---|---|
| Maior que 0% e menor que 5% | Baixa | Não obrigatória |
| De 5% a menor que 20% | Média | Não obrigatória |
| Igual ou superior a 20% | Alta | Obrigatória |

A confiança-base é `0,88`. Ela é reduzida para `0,70` quando o grupo técnico possui mais de três grafias ou quando a coluna possui mais de 50 valores distintos; não aumenta por semelhança aproximada ou por dicionário vazio.

## Privacidade, governança e promoção

O profiler e a regra não persistem exemplos de células, chaves normalizadas, rótulos de categoria ou títulos brutos de abas. O finding usa apenas identificadores anonimizados de aba e coluna, contagens e proporções. A recomendação pede reconciliação no sistema de origem ou em uma dimensão de categorias validada pelo responsável de negócio.

A regra permanece bloqueada para produção. Sua inclusão na allowlist draft foi aprovada pelo gate de calibração local; a habilitação produtiva continua dependente dos bloqueios do Gate MVP 1.0.
