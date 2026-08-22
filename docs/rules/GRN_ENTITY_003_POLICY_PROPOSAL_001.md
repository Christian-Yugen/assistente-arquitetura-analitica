# GRN-ENTITY-003 — Política Proposta 001: Entidade por linha

## Estado e finalidade

Esta é uma proposta **não executável** para a `GRN-ENTITY-003`. Chris aprovou a **Proposta A** e autorizou somente a formalização do gate de reconstrução; essa decisão não permite perfil, classificador, registro, versão contratual, pipeline, allowlist, testes executáveis, calibração ou produção. A fonte oficial define a regra como P1, por aba, dependente de tipagem semântica e com saída de granularidade, mas não determina uma condição operacional.

## Decisão registrada

Chris aprovou a **Proposta A — hipótese conservadora de entidade estável por linha**. A aprovação é limitada à política e ao próximo gate de reconstrução `GRN-ENTITY-003-RECONSTRUCTION-AUTHORIZATION-001`. A implementação draft requer autorização explícita posterior; a produção permanece bloqueada.

## Proposta A — hipótese conservadora de entidade estável por linha

A regra poderá emitir a hipótese `entity_per_row_candidate` somente se todos os critérios abaixo forem satisfeitos na mesma aba. A hipótese descreve uma estrutura candidata; ela não confirma entidade de negócio, tabela dimensão, chave primária, SCD, relacionamento ou modelo dimensional.

| Critério | Proposta A |
|---|---|
| Base mínima | Pelo menos **20 linhas observadas** na aba. |
| Marcador de entidade | Exatamente uma coluna cujo cabeçalho, após normalização transitória NFKC, `casefold`, remoção de acentos e colapso de espaços, seja exatamente `cliente`, `produto`, `fornecedor`, `colaborador`, `funcionario`, `paciente`, `aluno` ou `conta`. |
| Chave por linha | Exatamente uma hipótese prévia `explicit_key_candidate` da `GRN-EXPL-002`; a regra não reavalia cabeçalho, valores ou unicidade. |
| Atributo descritivo | Pelo menos uma classificação prévia de descrição, categoria, localização ou status; a regra conta somente sinais agregados já emitidos, sem reavaliar a coluna. |
| Ausência temporal | Zero datas não competência reconhecidas pela `SEM-DATE-001`; data de competência da `SEM-COMP-002` também não habilita a hipótese. |
| Ausência de evento ou medida | Zero marcadores de evento, sinais de quantidade, moeda, percentual, meta ou realizado já classificados. |
| Exclusões | O marcador de entidade não pode ser sensível, descritivo, uma data, conter fórmula ou ter tipo físico divergente do texto. |
| Ambiguidade | Zero ou mais de um marcador, chave, data, evento ou medida bloqueia a hipótese. |
| Evidência | Somente booleanos e contagens agregadas de linhas, candidatos, exclusões, fórmulas e ambiguidades. |
| Saída | Hipótese `entity_per_row_candidate`. |
| Confiança | `0.75`. |
| Revisão | Pergunta humana bloqueante. |

A pergunta vinculada deverá solicitar confirmação de que cada linha representa uma entidade estável de cadastro, e não um evento, período, relacionamento ou medida. Sem resposta humana, a hipótese não habilita classificação de dimensão, relacionamento, métrica ou SCD.

## Alternativa B — pergunta guiada sem hipótese automática

Como alternativa de menor inferência, a regra poderá abrir apenas uma pergunta bloqueante quando houver uma chave explícita, um marcador fechado de entidade e ao menos um atributo descritivo, sem emitir `entity_per_row_candidate`. Essa alternativa reduz o risco de interpretar uma lista operacional como cadastro, mas oferece menos orientação estrutural ao diagnóstico.

## Exclusões e precedência

Cabeçalhos fora do vocabulário fechado, incluindo `cadastro`, `registro`, `pessoa`, `item`, `documento`, `pedido`, `nota`, `movimento`, `atividade`, `data` e `periodo`, não serão inferidos por esta proposta. O motor não interpreta valores, textos livres, títulos de abas, contexto externo, formatos visuais, nomes de arquivos ou regras de negócio. Marcadores sensíveis, descritivos, de data, com fórmulas, tipos físicos divergentes, menos de 20 linhas ou qualquer multiplicidade de sinais bloqueiam a saída.

A `GRN-EXPL-002` é apenas uma pré-condição de chave já classificada. `SEM-DATE-001` e `SEM-COMP-002` têm precedência sobre qualquer leitura temporal. A `GRN-EVENT-004` e os sinais de medida têm precedência negativa: suas presenças bloqueiam a hipótese. A proposta pode coexistir com achados de qualidade e classificações semânticas não conflitantes, mas não substitui a validação humana nem confirma uma dimensão.

## Privacidade e controles preservados

O cabeçalho será avaliado somente de modo transitório para derivar `header_eligible`. O perfil futuro não poderá reter ou projetar cabeçalhos normalizados, valores, rótulos, tokens, exemplos, frequências por valor, posições, identificadores de coluna, títulos de aba, fórmulas ou hashes de conteúdo. O mascaramento de CPF, e-mail, nomes e títulos de abas permanece um controle independente, assim como a `SEM-SENS-015`.

## Pré-condições de ativação

Antes de qualquer implementação, esta proposta exige escolha explícita de Chris, gate de reconstrução `GRN-ENTITY-003-RECONSTRUCTION-AUTHORIZATION-001` e autorização explícita posterior para execução draft. Após esses controles, ainda serão necessários perfil privado imutável, classificador determinístico, registro de granularidade, integração canônica protegida por catálogo, testes unitários e de pipeline, golden dataset sintético, SHA-256, calibração reproduzível e gate individual de calibração. A produção permanece bloqueada.

## Referências internas

| Artefato | Uso nesta proposta |
|---|---|
| `PM-MVP-PBI-001`, princípios e fase de regras | Separa evidência de hipótese e exige validação humana. |
| `PM-MVP-PBI-RULE-BP-001` | Registra prioridade P1, escopo por aba, dependência e saída oficiais. |
| `GRN-EXPL-002`, `GRN-EVENT-004` e regras semânticas existentes | Delimitam os sinais pré-existentes e suas precedências. |
