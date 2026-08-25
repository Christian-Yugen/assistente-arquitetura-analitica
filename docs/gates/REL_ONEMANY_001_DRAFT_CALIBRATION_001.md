# Gate de Calibração Draft — REL-ONEMANY-001

**Status:** aprovado exclusivamente para o perfil draft controlado.

O gate registra a calibração `CAL-REL-ONEMANY-001-001` contra o dataset exclusivamente sintético `GD-REL-ONEMANY-001-001`, registrado no manifesto `MANIFEST-GD-REL-ONEMANY-001-001` e assinado com SHA-256 `f76403acdc27339f2195ee9f043e8a74ff5e1938972c71a52bb5b01ef4dbd5a2`. O avaliador reproduzível `engine.calibration.evaluate_rel_onemany_draft_golden.evaluate` reporta **3 verdadeiros positivos, 0 falsos positivos e 0 falsos negativos**.

A regra somente emite `one_to_many_relationship_candidate` para uma direção opaca entre abas distintas quando a origem já é hipótese de dimensão padrão e o destino já é hipótese de fato transacional ou periódico. A direção deve ter exatamente uma chave única e completa, exatamente uma referência completa e não única, cobertura referencial agregada integral e direção elegível única. Fórmulas, sensibilidade, classificação indefinida, fato sem grão, calendário, conflito, autorreferência, padrão 1:1, padrão N:N, cobertura parcial e ambiguidade bloqueiam a emissão.

O profiler mantém assinaturas técnicas somente durante a execução do request para calcular cobertura. Antes do retorno, elimina essas assinaturas e transmite ao pipeline apenas IDs opacos de abas e colunas, contagens, booleanos de completude/unicidade, cobertura agregada e sinais de bloqueio. A projeção final preserva somente IDs opacos de abas, tipo, confiança, severidade, evidências agregadas, regra, versão e a pergunta humana bloqueante. Ela não contém nomes de abas, cabeçalhos, valores, posições, pares de correspondência, exemplos, frequências individuais, chaves ou identificadores de origem.

Esta ativação decorre da Proposta A aprovada por Chris, do `REL-ONEMANY-001-RECONSTRUCTION-AUTHORIZATION-001` e da autorização explícita posterior para implementação draft. A confirmação humana continua obrigatória. `SEM-SENS-015` e o mascaramento permanecem controles independentes: qualquer sinal de sensibilidade bloqueia a hipótese REL. O perfil é um experimento controlado; nenhuma relação é criada automaticamente e a produção permanece bloqueada.
