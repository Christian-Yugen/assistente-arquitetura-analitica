# QLT-BADDATE-006 — Especificação Lógica Proposta 001

**Estado:** especificação não executável; dependente da aprovação da Política Proposta 001.  
**Versão prevista se autorizada:** `0.1.0-provisional.1`.

## Contrato de entrada proposto

O profiler recebe valores individuais de uma coluna somente durante a leitura em memória. Após a agregação, o contexto conserva um `BadDateProfile` imutável com `strict_date_candidate_count`, `invalid_strict_date_count`, `invalid_strict_date_ratio` e `normalization_basis`. Valores, amostras, posições, fórmulas, títulos e nomes não fazem parte desse perfil.

## Algoritmo determinístico proposto

| Etapa | Regra |
|---|---|
| 1 | Ignorar ausência estrutural, texto em branco e `NaN` numérico pela semântica comum de missingness. |
| 2 | Ignorar objetos nativos `date` e `datetime`, números, booleanos e objetos não textuais. |
| 3 | Para texto, remover somente espaços nas extremidades e verificar a correspondência integral a `^\d{4}-\d{2}-\d{2}$`, `^\d{2}-\d{2}-\d{4}$` ou `^\d{2}/\d{2}/\d{4}$`. |
| 4 | Para ISO, incrementar `strict_date_candidate_count` e executar `date.fromisoformat`; para brasileiro com hífen ou barra, incrementar a mesma contagem e executar respectivamente `datetime.strptime(valor, "%d-%m-%Y")` ou `datetime.strptime(valor, "%d/%m/%Y")`. Não aplicar locale, timezone, heurística ou correção. |
| 5 | Se o parser correspondente falhar, incrementar `invalid_strict_date_count`. |
| 6 | Calcular a razão como `invalid_strict_date_count / strict_date_candidate_count`, com zero quando o denominador for zero. |
| 7 | Emitir finding somente se a contagem inválida for superior a zero; classificar pela razão aprovada. |

## Invariantes de segurança e contrato

O perfil não pode reter nem serializar valores de célula, nomes de coluna, títulos de aba, posições de linha, posições de coluna ou detalhes da exceção do parser. O avaliador deve retornar uma lista vazia quando não houver candidato inválido e nunca deve alterar o workbook. A integração no executor deve ser condicionada ao status `executable_draft` proveniente do catálogo.

## Matriz inicial de testes exigidos

| Cenário | Resultado esperado |
|---|---|
| Datas ISO ou brasileiras de calendário válidas, com hífen ou barra | Sem finding. |
| Um ou mais dias ou meses impossíveis nos formatos estritos | Finding agregado. |
| Texto regional, código, número serial e fórmula | Excluídos; sem finding por esta regra. |
| Ausências e valores nativos de data | Excluídos do denominador. |
| Razões nos limiares de 5% e 20% | Severidade determinística. |
| Valores, nomes, abas e posições sensíveis | Ausentes do finding, da pergunta e do contrato canônico. |

> Esta especificação não autoriza implementação, registro de versão, integração de pipeline, teste de código ou alteração da allowlist enquanto a Opção A não for aceita por Chris.
