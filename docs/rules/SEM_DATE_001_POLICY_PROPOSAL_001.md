# SEM-DATE-001 — Política proposta 001

**Estado:** não executável; aguarda autorização explícita de Chris.  
**Versão pretendida:** `0.1.0-provisional.1`.  
**Escopo:** uma coluna por avaliação.  
**Fonte recuperada:** o blueprint oficial define a classificação ampla de colunas de data, prioridade P0, escopo por coluna, dependência de profiling e saída `semantic_type`. O Plano Mestre exige que a inferência semântica seja explicável e submetida à validação humana. O profiler já possui gramáticas estritas para datas textuais, mas o contrato canônico atual não projeta classificações semânticas.

## Proposta A — classificação `date_generic` com cobertura total e formatos fechados

Esta proposta atribui a classificação semântica provisória `date_generic` somente quando uma coluna tiver pelo menos 10 valores físicos não ausentes e **todos** forem reconhecidos como data física (`date` ou `datetime`, excluídos booleanos) ou como texto válido em uma das três gramáticas já autorizadas: `AAAA-MM-DD`, `DD-MM-AAAA` e `DD/MM/AAAA`. O texto é normalizado apenas por `strip` antes de uma validação estrita de calendário; nenhuma outra interpretação de locale é permitida.

| Elemento | Política proposta |
|---|---|
| Base mínima | Pelo menos 10 valores físicos não ausentes. Ausências são ignoradas para a cobertura, mas continuam tratadas pelas regras de qualidade. |
| Valores reconhecidos | `date` ou `datetime` físicos, ou texto válido exatamente em `AAAA-MM-DD`, `DD-MM-AAAA` ou `DD/MM/AAAA`, após `strip`. |
| Condição | Pelo menos 10 valores físicos não ausentes e proporção de valores de data reconhecidos igual a 100%. |
| Saída | Classificação semântica `date_generic`, confiança moderada, evidências agregadas e pergunta humana genérica de confirmação. |
| Evidência | Contagem de valores físicos não ausentes, datas físicas, textos ISO válidos, textos pt-BR com hífen válidos, textos pt-BR com barra válidos e razão reconhecida; sem valores, cabeçalhos, posições, exemplos ou títulos de aba. |
| Projeção canônica | Nova coleção `semantic_classifications` no fragmento canônico, separada de findings e questions, com `semantic_type`, confiança, evidência agregada, regra e entidades afetadas. |
| Intervenção | Não converte, corrige, preenche, normaliza, altera timezone, calcula calendário, move ou reordena dados. |

## Exclusões obrigatórias

A proposta exclui números seriais de Excel, timestamps textuais, horas isoladas, `AAAA/MM/DD`, períodos como `2026-08`, datas escritas por extenso, valores não finitos, booleanos, fórmulas, números em texto, formatações de célula, nomes de coluna, inferência de timezone, granularidade de data, papel de negócio da data e qualquer conversão automática. Uma coluna com um único valor não reconhecido não recebe classificação, mesmo que todos os demais valores sejam datas.

> A classificação `date_generic` significa apenas que os valores apresentam cobertura total de formatos de data estritamente reconhecidos. Ela não decide se a data é de pedido, vencimento, referência, admissão, competência ou outra semântica de negócio.

## Evidências exigidas antes da ativação draft

Após autorização, a implementação deverá oferecer perfil imutável agregado, classificador determinístico, projeção `semantic_classifications` versionada no contrato, pergunta humana, testes positivos, negativos, limítrofes, de privacidade, de contrato e de integração, golden dataset sem valores brutos, manifesto SHA-256, relatório reprodutível de TP/FP/FN, gate individual de calibração e prova documental. A produção permanece bloqueada mesmo após eventual ativação draft.
