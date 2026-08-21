# QLT-HEADERS-014 — Política proposta 001

**Estado:** não executável; aguarda autorização explícita de Chris.  
**Versão pretendida:** `0.1.0-provisional.1`.  
**Escopo:** uma aba por avaliação.  
**Fonte recuperada:** o blueprint oficial define a detecção de cabeçalhos ausentes, duplicados ou multinível, prioridade P0, escopo por aba, dependência de profiling e saída `finding`. O Plano Mestre exige que o diagnóstico não converta hipóteses em alterações automáticas. Não foi recuperada uma especificação materializada para os três sinais.

## Proposta A — primeira linha, sinais estruturais limitados e evidência agregada

Esta proposta trata exclusivamente a primeira linha materializada de cada aba como candidata a cabeçalho. Ela cria finding somente se detectar pelo menos um dos três sinais autorizados: célula de cabeçalho ausente, texto duplicado após normalização técnica ou candidato a cabeçalho multinível representado por range mesclado horizontal iniciado na primeira linha e segunda linha com pelo menos duas células físicas não vazias dentro da largura daquele range. Textos e posições são usados de forma transitória e descartados antes do perfil.

| Elemento | Política proposta |
|---|---|
| Linha analisada | Somente a primeira linha materializada da aba, sem procurar automaticamente outra linha de cabeçalho. |
| Ausência | Célula `None`, texto que se reduz a vazio após `strip`, ou fórmula no cabeçalho é contada como ausente. Zero numérico, data, booleano e texto não vazio são tratados como presentes. |
| Duplicidade | Somente texto não vazio, normalizado por NFKC, `casefold`, remoção de acentos e colapso de espaços, repetido em duas ou mais colunas. O texto não é emitido. |
| Multinível | Range mesclado horizontal iniciado na primeira linha, largura de ao menos duas colunas e ao menos duas células físicas não vazias na segunda linha, dentro de seu intervalo. É um candidato estrutural, não uma confirmação de erro. |
| Evidência | Quantidade de colunas, cabeçalhos ausentes, grupos duplicados normalizados, cabeçalhos envolvidos em duplicidade e candidatos multinível; sem títulos, abas, posições, ranges ou valores. |
| Severidade | Alta quando há candidato multinível; média quando há ausência ou duplicidade; baixa somente quando não há finding. |
| Confiança | Moderada, pois os sinais são determinísticos, mas a intenção estrutural da aba continua dependente de confirmação humana. |
| Pergunta humana | Em todo finding, solicitar confirmação genérica da linha correta de cabeçalho, das duplicidades intencionais e da estrutura de cabeçalho de múltiplas linhas. |
| Intervenção | Não renomear, preencher, deduplicar, desmesclar, mover, excluir, inserir ou reordenar células, linhas, colunas ou abas. |

## Exclusões obrigatórias

A proposta exclui busca de cabeçalhos em linhas posteriores, inferência de nomes semânticos, comparação de títulos entre abas, títulos de aba, cabeçalhos de tabelas Excel internas, ranges mesclados fora da primeira linha, multilinearidade sem mesclagem horizontal, conteúdo de fórmulas, estilos, cores, comentários, valores abaixo da segunda linha e qualquer correção automática.

> Um finding indica uma hipótese estrutural para validação humana. Ele não determina que uma célula deve ser preenchida, que uma duplicidade deve ser renomeada ou que uma estrutura multinível deve ser achatada.

## Evidências exigidas antes da ativação draft

Após autorização, a implementação deverá fornecer perfil imutável agregado, inspeção transitória de texto e ranges, testes positivos, negativos, limítrofes, de privacidade e de integração, golden dataset sem títulos ou ranges identificáveis, manifesto SHA-256, relatório reprodutível de TP/FP/FN, gate individual de calibração e prova documental. A produção permanece bloqueada mesmo após eventual ativação draft.
