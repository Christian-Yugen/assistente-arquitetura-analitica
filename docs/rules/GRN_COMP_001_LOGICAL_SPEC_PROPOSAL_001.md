# GRN-COMP-001 — Especificação Lógica Proposta 001

**Estado:** rascunho de desenho; não executável e sem autorização de implementação.

Caso Chris aprove a Proposta A, o motor deverá operar sobre um perfil por aba e por pares elegíveis, sem materializar conteúdo das células. O algoritmo proposto é: receber da camada de tipagem os candidatos elegíveis; limitar o conjunto a dez pares; contar linhas observadas, ausências por componente, cardinalidades individuais e cardinalidade conjunta; aplicar os limiares; produzir apenas uma hipótese agregada e uma pergunta humana. O algoritmo deve falhar fechado: se a tipagem semântica não estiver disponível, se não houver 20 linhas, se os campos forem sensíveis ou se houver ambiguidade, não emite hipótese.

O perfil previsto contém `observed_row_count`, `eligible_pair_count`, `examined_pair_count`, `complete_pair_row_count`, `left_distinct_count`, `right_distinct_count`, `joint_distinct_count` e `joint_uniqueness_ratio`. O vocabulário é fechado e não inclui valores, nomes, índices, hashes nem dados da aba.

Uma implementação futura deverá decidir separadamente a projeção canônica: preferencialmente um fragmento de hipótese de granularidade vinculado à aba, sem sobrecarregar o finding de qualidade. Essa decisão dependerá de revisão do contrato existente e não é tomada por este rascunho.

## Bloqueio técnico de dependência identificado

A implementação atual possui somente a classificação semântica de data. Não há classificador semântico de identificador que possa fornecer, de forma canônica, os pares elegíveis exigidos pela Proposta A. O perfil de completude de identificadores existente é uma regra de qualidade orientada por vocabulário de cabeçalhos e não é uma tipagem semântica equivalente.

Assim, a GRN-COMP-001 não deve usar esse sinal como substituto silencioso. Antes de qualquer código, Chris deve escolher entre aguardar uma regra de tipagem de identificador ou autorizar explicitamente, como exceção draft, um vocabulário fechado de cabeçalhos não sensíveis apenas para a elegibilidade inicial. A implementação permanece bloqueada até essa decisão.
