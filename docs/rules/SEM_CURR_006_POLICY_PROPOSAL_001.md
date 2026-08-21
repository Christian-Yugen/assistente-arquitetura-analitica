# SEM-CURR-006 — Proposta de Política 001

**Regra:** `SEM-CURR-006` — Valor monetário.  
**Estado:** proposta não executável; execução bloqueada.  
**Escopo oficial recuperado:** regra P1 por coluna, na etapa `semantic_typing`, dependente de qualidade e com saída `semantic_type`.

## Lacuna oficial e princípio conservador

O blueprint oficial determina a classificação de uma coluna como valor monetário por evidências convergentes, mas não define condição, exclusões, confiança, evidência, pergunta, testes ou calibração. A Proposta A limita a inferência ao caso em que a semântica do cabeçalho e a formatação monetária explícita do Excel concordam para todos os números físicos elegíveis. Ela não infere moeda pelo valor numérico, não deduz unidade a partir de distribuição, não extrai símbolos ou códigos da saída e não aceita cabeçalho isolado como evidência suficiente.

## Proposta A — valor monetário candidato

Uma coluna será classificada como `currency_candidate` somente quando todos os critérios forem verdadeiros: o cabeçalho normalizado pertencer ao vocabulário fechado `preco`, `preco unitario`, `preco total`, `valor monetario`, `valor financeiro`, `valor total`, `receita`, `faturamento`, `custo`, `custo total`, `despesa` ou `saldo`; houver ao menos 10 números físicos finitos; todos esses números tiverem formato Excel com marcador monetário explícito; e não houver fórmulas, candidatos numéricos textuais, ambiguidades numéricas ou classificação semântica de data.

O marcador será avaliado transitoriamente no formato de número da célula e reduzido a uma contagem agregada. A proposta considera estritamente marcadores monetários explícitos como `R$`, `$`, `€`, `£`, `¥`, `₹`, `¤` e formatos locais equivalentes que os preservem. O perfil não reterá o formato, o marcador, código de moeda, valores, cabeçalho, posições, nomes de abas, identificadores ou hashes. A hipótese terá confiança inicial de **0,80** e incluirá a pergunta humana bloqueante: **“Esta coluna representa montantes monetários; a moeda e a unidade de negócio exibidas estão corretas para a modelagem?”**

| Elemento | Política proposta |
|---|---|
| Base mínima | 10 números físicos finitos |
| Tipo físico | `numeric` |
| Vocabulário fechado | `preco`, `preco unitario`, `preco total`, `valor monetario`, `valor financeiro`, `valor total`, `receita`, `faturamento`, `custo`, `custo total`, `despesa`, `saldo` |
| Evidência de formatação | Todos os números físicos com marcador monetário explícito no formato Excel |
| Integridade | Sem fórmulas, candidatos numéricos textuais ou ambiguidades numéricas |
| Exclusão temporal | Sem classificação semântica de data |
| Classificação | `currency_candidate` |
| Confiança | `0.80` |
| Pergunta | Obrigatória e bloqueante |
| Saída | Fragmento canônico `semantic_type` com evidências agregadas |

## Exclusões e privacidade

Ficam excluídas colunas com menos de 10 números físicos, tipos texto, misto, booleano ou data; números não finitos; fórmulas; números textuais ou ambíguos; cabeçalho fora do vocabulário fechado; formatação geral, numérica, percentual, contábil sem marcador monetário explícito ou inconsistente entre números físicos; e classificação de data. A proposta não interpreta valores decimais, negativos, zeros, magnitude, símbolo de moeda ou código ISO como confirmação de negócio.

## Alternativa B — cabeçalho ou valor sem formatação explícita

Uma alternativa seria classificar colunas por cabeçalho financeiro ou por magnitude e casas decimais. Ela ampliaria cobertura, mas confundiria índices, quantidades, saldos não monetários, pontuações, medidas e códigos. A Proposta A privilegia precisão e deixa qualquer ampliação para um novo intake, política, calibração e autorização explícita.

## Condição de avanço

Esta proposta não autoriza implementação. O avanço exige aprovação explícita de Chris para a Proposta A, seguida de gate de reconstrução, perfil privado que examine somente o formato da célula de modo transitório, classificador determinístico, registro semântico, versão de contrato, integração canônica, testes positivos/negativos/limítrofes, golden dataset assinado, calibração reprodutível, gate individual e ativação exclusivamente em draft. Produção permanece bloqueada.

## Referências internas

1. `artifacts/catalogs/official-rule-blueprint-95.json`, sequência 21, `SEM-CURR-006`.
2. `artifacts/catalogs/rule-implementation-readiness-v1.json`, registro `SEM-CURR-006`.
3. `artifacts/intake/SEM-CURR-006.json`, lacunas e pré-condições recuperadas.
