# MDL-DIMSTD-004 — Proposta de Política 001

**Regra:** `MDL-DIMSTD-004` — Dimensão cadastral.  
**Estado:** proposta não executável; implementação bloqueada.  
**Escopo oficial recuperado:** regra P0, por aba, na etapa `table_classification`, dependente de `grain` e com saída `classification_or_table`.

## Lacuna e princípio conservador

O blueprint oficial determina a finalidade de classificar ou propor uma dimensão cadastral, mas não materializa condição, limiares, exclusões, confiança ou formato de evidência. A presente proposta define uma hipótese draft conservadora; não confirma chave de negócio, não cria modelo Power BI e não infere entidades a partir de conteúdo textual.

O plano e os requisitos do MVP exigem evidências positivas e negativas, confiança e preservação de uma classificação indefinida em situações ambíguas. Portanto, a regra só deverá emitir uma hipótese quando os sinais estruturais convergirem; nos demais casos, ela permanecerá silenciosa.

## Proposta A — dimensão cadastral candidata

Uma aba será classificada como `dimension_standard_candidate` somente quando todos os critérios abaixo forem verdadeiros: existe hipótese de granularidade válida; há ao menos 20 linhas observadas; existe pelo menos um identificador semântico individualmente completo e único; existe ao menos um atributo textual físico, não sensível, não identificador e não temporal, com diversidade relativa entre 5% e 90%; e não há medida numérica física elegível nem coluna temporal integralmente reconhecida.

O objetivo é caracterizar, de modo estritamente estrutural, uma tabela que descreve entidades estáveis em vez de eventos, medições ou estados ao longo do tempo. A classificação receberá confiança inicial de **0,70** e sempre produzirá uma pergunta humana bloqueante: **“Cada linha representa uma entidade relativamente estável, identificada por uma chave e descrita por atributos, sem registrar medidas ou eventos?”**

| Elemento | Política proposta |
|---|---|
| Base mínima | 20 linhas observadas |
| Chave candidata | Pelo menos um identificador semântico com cobertura e unicidade de 100% |
| Atributo descritivo | Pelo menos um texto físico, não sensível, não identificador e não temporal; diversidade entre 5% e 90% |
| Exclusão de fato | Nenhuma medida numérica física elegível e nenhuma coluna temporal integralmente reconhecida |
| Classificação | `dimension_standard_candidate` |
| Confiança | `0.70` |
| Pergunta | Obrigatória e bloqueante |
| Saída | Fragmento canônico `classification_or_table`, evidência agregada e sem dados brutos |

## Exclusões e privacidade

Ficam excluídas abas com menos de 20 linhas, sem granularidade, sem identificador individualmente único, sem atributo descritivo, com medidas numéricas elegíveis, com data integralmente reconhecida, com fórmulas nos sinais usados, ou cuja hipótese dependa de título de aba, valores, formatos de identificadores, regex, nomes de pessoas, CPF, e-mail, telefone, endereço ou outro dado sensível.

O perfil futuro poderá reter somente contagens e razões agregadas: linhas observadas, quantidade de identificadores individuais elegíveis, quantidade de atributos descritivos elegíveis, quantidade de medidas excluentes e quantidade de colunas temporais excluentes. Valores, nomes de cabeçalhos, posições, títulos de abas, hashes, chaves e nomes de entidades devem ser descartados antes da projeção canônica.

## Alternativa B — pergunta sem classificação

Uma alternativa seria emitir apenas uma pergunta para qualquer aba com identificador e texto. Ela reduz o risco de falso positivo, mas não produz a hipótese estruturada exigida para a classificação de tabelas quando os sinais são suficientemente convergentes.

## Condição de avanço

Esta política não autoriza implementação. O avanço exige aprovação explícita de Chris para a Proposta A, seguida de gate de reconstrução, branch isolada, perfil privado, classificador determinístico, testes positivos/negativos/limítrofes, golden dataset assinado, calibração reprodutível, gate individual e ativação exclusiva em draft. A produção continuará bloqueada.

## Referências internas

1. `artifacts/catalogs/official-rule-blueprint-95.json`, registro 44 da `MDL-DIMSTD-004`.
2. `docs/governance/RULE_DEVELOPMENT_LIFECYCLE_001.md`.
3. `PM-MVP-PBI-001 v1.0` e `PM-MVP-PBI-REQ-001 v1.0`, fontes do pacote compartilhado do projeto.
