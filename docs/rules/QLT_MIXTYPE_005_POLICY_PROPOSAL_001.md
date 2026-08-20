# QLT-MIXTYPE-005 — Política Proposta 001: Tipos mistos

**Estado:** proposta não autorizada para execução.  
**Regra:** `QLT-MIXTYPE-005`.  
**Versão pretendida:** `0.1.0-provisional.1`, se aprovada.  
**Decisão requerida:** aprovação explícita de Chris para a política abaixo antes de qualquer código, teste executável, golden dataset ou inclusão em allowlist.

## Fonte e escopo recuperados

O blueprint oficial registra a regra como **Tipos mistos**, com propósito de **detectar coexistência incompatível de tipos**, prioridade `P0`, escopo `column`, dependência de `profiling`, saída primária `finding` e estado de implementação `planned`. O arquivo `engine/profiling/workbook.py` já mantém, por coluna, contagens agregadas de booleanos, números, textos e outros valores não ausentes; ele ainda não possui um perfil semântico específico para esta regra.

## Proposta conservadora — Opção A

A regra deve emitir um finding **somente** quando uma coluna contiver pelo menos dois grupos fisicamente incompatíveis entre valores não ausentes, com evidência agregada suficiente para reduzir sinais de amostras triviais. A proposta considera os grupos `boolean`, `numeric`, `text` e `temporal`; valores estruturais ausentes, texto em branco e `NaN` numérico ficam fora do denominador e continuam sob a QLT-NULL-001.

Para não duplicar a QLT-NUMTEXT-007, cadeias numéricas canônicas não devem, isoladamente, gerar a coexistência `numeric` + `text` nesta regra: elas continuam sendo evidência exclusiva da regra de números armazenados como texto. A regra também não tentará interpretar textos como datas, nem corrigirá ou converterá tipos; essas decisões permanecem fora de seu escopo.

O finding será proposto apenas quando houver ao menos **cinco valores não ausentes**, pelo menos **dois grupos incompatíveis**, e cada grupo participante tiver pelo menos **dois valores**. A exigência de dois valores por grupo é deliberadamente conservadora: um único valor atípico ficará fora desta primeira versão, evitando interpretar ruído operacional ou uma célula de exceção como mistura confirmada.

| Situação | Resultado proposto | Justificativa |
|---|---|---|
| Números e textos não numéricos, ambos com pelo menos dois valores | Finding | Coexistência física incompatível observada com base mínima. |
| Booleanos e números, ambos com pelo menos dois valores | Finding | Os grupos são distintos e não devem ser fundidos automaticamente. |
| Números e cadeias numéricas canônicas | Sem finding nesta regra | A evidência pertence à QLT-NUMTEXT-007. |
| Um único valor de tipo divergente | Sem finding nesta versão | Política conservadora; não infere erro a partir de exceção isolada. |
| Apenas valores ausentes, vazios ou `NaN` | Sem finding | Fora do escopo; coberto pela semântica de ausência. |
| Fórmulas, objetos não suportados ou textos de data | Sem finding até perfil próprio | Não há base agregada suficiente para classificação segura. |

## Privacidade, evidência e não intervenção

O finding, se aprovado, deverá conter somente contagens por grupo, total de valores não ausentes, proporções e uma base de normalização versionada. Não poderá conter valores de células, exemplos, posições, nomes de abas, nomes de colunas ou fórmulas. A regra não removerá, converterá, preencherá, normalizará ou reordenará dados.

Uma pergunta de validação deverá existir apenas para coexistência material (severidade média ou alta), solicitando confirmação de que os grupos representam significados distintos ou um problema de origem. Nenhuma resposta humana produzirá alteração automática no workbook.

## Limites e alternativas rejeitadas nesta proposta

A proposta não infere o tipo de negócio da coluna, não trata códigos numéricos como medidas, não parseia datas em texto, não identifica sentinelas e não estabelece chave ou granularidade. Essas interpretações exigem regras próprias das categorias de qualidade e semântica.

> Esta política é uma proposta de controle. A autorização de início do ciclo não equivale à autorização de implementação, calibração ou ativação da QLT-MIXTYPE-005.

## Decisão solicitada

Chris deve escolher uma das alternativas abaixo.

| Alternativa | Efeito |
|---|---|
| **Aprovar Opção A** | Autoriza criar o gate de reconstrução e implementar somente a política conservadora documentada. |
| Solicitar ajuste | Mantém a regra não executável e devolve a política para revisão. |
| Rejeitar | Encerra este ciclo sem alterar o catálogo executável. |
