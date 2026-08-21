# QLT-WHITESPACE-009 — Especificação Lógica Proposta 001

**Estado:** não executável e dependente de aprovação explícita da política proposta.  
**Regra-alvo:** `QLT-WHITESPACE-009`.  
**Versão pretendida após gate:** `0.1.0-provisional.1`.

## Contrato de entrada e saída

O profiler pode receber valores de células durante a leitura transitória do workbook, mas deverá descartar cada valor após atualizar o acumulador. O contexto de coluna deverá conservar somente `WhitespaceProfile`, imutável, com `non_blank_text_count`, `leading_or_trailing_space_count`, `hidden_character_count`, `affected_text_count`, `affected_text_ratio` e `normalization_basis`. Nenhum valor, amostra, posição, nome de coluna, título de aba ou fórmula pode ser serializado.

O avaliador recebe uma estrutura de perfil por coluna exclusivamente para compor findings canônicos. Caso a regra seja autorizada e a evidência alcance o gatilho, a saída conterá as contagens agregadas e uma recomendação de validação humana sem prescrever alteração automática.

## Algoritmo proposto

| Etapa | Operação determinística |
|---|---|
| 1 | Ignorar todo valor que `missing_class` classifique como ausência. |
| 2 | Ignorar qualquer valor que não seja `str`. |
| 3 | Para texto remanescente, incrementar `non_blank_text_count`. |
| 4 | Marcar espaço marginal se o primeiro ou último caractere for `U+0020` ou `U+00A0`. |
| 5 | Marcar invisível explícito se o texto contiver algum de `U+200B`, `U+200C`, `U+200D`, `U+2060` ou `U+FEFF`. |
| 6 | Incrementar cada contador de sinal aplicável; incrementar `affected_text_count` uma única vez se houver qualquer sinal. |
| 7 | Calcular `affected_text_ratio` como `affected_text_count / non_blank_text_count`, ou zero se não houver denominador. |
| 8 | Emitir finding apenas se `non_blank_text_count >= 3` e `affected_text_count > 0`. |

## Invariantes obrigatórias

| Invariante | Condição |
|---|---|
| Contagem de união | `affected_text_count` não pode exceder a soma dos dois contadores de sinal e não pode exceder `non_blank_text_count`. |
| Privacidade | Todo texto e identificador recebido pelo profiler deve ser descartado antes da saída. |
| Determinismo | O resultado depende apenas da sequência de valores e do conjunto explícito de caracteres. |
| Não sobreposição | Textos ausentes ou inteiramente em branco não entram no denominador desta regra. |
| Não intervenção | O avaliador não executa modificação de célula, planilha ou arquivo. |

## Matriz mínima de validação futura

| Cenário | Resultado esperado |
|---|---|
| Três ou mais textos limpos | Sem finding. |
| Espaço ASCII no início ou fim | Finding agregado conforme proporção. |
| Espaço não separável no início ou fim | Finding agregado conforme proporção. |
| Invisível explícito interno | Finding agregado conforme proporção. |
| Um texto com ambos os sinais | Uma ocorrência em `affected_text_count`; uma em cada contador de sinal. |
| Texto vazio, tabulação isolada ou quebra de linha isolada | Excluído por ausência; sem finding desta regra. |
| Tabulação ou quebra de linha dentro de texto não vazio | Sem finding desta política. |
