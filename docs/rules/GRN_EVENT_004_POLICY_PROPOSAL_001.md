# GRN-EVENT-004 — Política Proposta 001: Evento por linha

## Estado e finalidade

Esta é uma proposta **não executável** para a `GRN-EVENT-004`. Ela não autoriza perfil, classificador, registro, versão contratual, integração no pipeline, allowlist, testes executáveis, calibração ou produção. A fonte oficial recuperada define a regra como P0, por aba, dependente de tipagem semântica e com saída de granularidade, mas não prescreve sua condição operacional. Portanto, esta proposta cria uma alternativa draft conservadora, ainda sujeita à aprovação explícita de Chris.

## Proposta A — hipótese de evento por linha com marcador, chave e tempo

A regra poderá emitir a hipótese `event_per_row_candidate` somente se todos os critérios abaixo forem satisfeitos na mesma aba. A hipótese descreve um padrão estrutural; ela não confirma um evento de negócio, uma transação, uma tabela fato, uma chave primária ou um relacionamento.

| Critério | Proposta A |
|---|---|
| Base mínima | Pelo menos **20 linhas observadas** na aba. |
| Marcador de evento | Exatamente uma coluna cujo cabeçalho, após normalização transitória NFKC, `casefold`, remoção de acentos e colapso de espaços, seja exatamente `evento`, `transacao` ou `ocorrencia`. |
| Chave por linha | Exatamente uma hipótese prévia `explicit_key_candidate` da `GRN-EXPL-002`; a regra não reavalia cabeçalho, valores ou unicidade. |
| Sinal temporal | Exatamente uma coluna de data reconhecida pela `SEM-DATE-001`; uma data de competência da `SEM-COMP-002` não conta como marcador temporal do evento. |
| Exclusões | O marcador de evento não pode ser sensível, descritivo, uma data, conter fórmula ou ter tipo físico divergente do texto. |
| Ambiguidade | Zero ou mais de um marcador, chave ou sinal temporal bloqueia a hipótese. |
| Evidência | Somente booleanos e contagens agregadas de linhas, candidatos, exclusões, fórmulas e ambiguidades. |
| Saída | Hipótese `event_per_row_candidate`. |
| Confiança | `0.80`. |
| Revisão | Pergunta humana bloqueante. |

A pergunta vinculada deverá solicitar confirmação de que cada linha representa um evento pontual identificável no processo de negócio. A resposta humana governará qualquer promoção posterior; sem resposta, a hipótese não habilita classificação de fato, relacionamento ou métrica.

## Alternativa B — pergunta guiada sem hipótese automática

Como alternativa de menor inferência, a regra poderá apenas abrir uma pergunta bloqueante quando houver simultaneamente uma chave explícita e uma data não vinculada à competência, sem interpretar um marcador de evento. Essa opção reduz o risco de chamar de evento uma linha de cadastro, mas fornece menos orientação estruturada ao diagnóstico.

## Exclusões e precedência

Cabeçalhos fora do vocabulário fechado, incluindo `pedido`, `nota`, `movimento`, `lancamento`, `registro`, `atividade`, `data` e `periodo`, não serão inferidos por esta proposta. O motor não interpreta valores, textos livres, títulos de abas, contexto externo, formatos visuais, nomes de arquivos ou regras de negócio. Colunas sensíveis, descritivas, de data, com fórmulas, tipos físicos divergentes, menos de 20 linhas ou qualquer multiplicidade de sinais bloqueiam a saída.

A `GRN-EXPL-002` e a `SEM-DATE-001` permanecem independentes e são apenas pré-condições de sinais já classificados. A `SEM-COMP-002` tem precedência para excluir datas de competência. A proposta pode coexistir com achados de qualidade e classificações semânticas não conflitantes, mas não substitui a validação humana nem confirma que a aba seja uma tabela fato.

## Privacidade e controles preservados

O cabeçalho será avaliado somente de modo transitório para derivar `header_eligible`. O perfil futuro não poderá reter ou projetar cabeçalhos normalizados, valores, rótulos, tokens, exemplos, frequências por valor, posições, identificadores de coluna, títulos de aba, fórmulas ou hashes de conteúdo. O mascaramento de CPF, e-mail, nomes e títulos de abas permanece um controle independente, assim como a `SEM-SENS-015`.

## Pré-condições de ativação

Esta proposta exige escolha explícita de Chris entre as alternativas A e B. Depois da escolha, serão necessários gate de reconstrução, perfil privado imutável, classificador determinístico, registro de granularidade, integração canônica protegida por catálogo, testes unitários e de pipeline, golden dataset sintético, SHA-256, calibração reproduzível e gate individual de calibração. A produção permanece bloqueada.

## Referências internas

| Artefato | Uso nesta proposta |
|---|---|
| `PM-MVP-PBI-001`, seção de princípios e fase de regras | Separa evidência de hipótese e exige validação humana. |
| `PM-MVP-PBI-RULE-BP-001` | Registra prioridade P0, escopo por aba, dependência e saída oficiais. |
| `GRN-EXPL-002` e `SEM-DATE-001/SEM-COMP-002` | Delimitam os sinais pré-existentes e suas precedências. |
