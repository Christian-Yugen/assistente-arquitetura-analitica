# REL-MANYMANY-004 — Proposta de Política 001

## Estado não executável

Esta proposta recupera somente os limites ausentes do blueprint para a regra **Muitos-para-muitos**. Ela não cria perfil, classificador, registro, contrato, pipeline, catálogo, testes executáveis, dataset golden, calibração ou ativação draft. A regra e a produção permanecem bloqueadas até decisão humana posterior.

## Proposta A — alerta conservador de cardinalidade muitos-para-muitos

Um **par opaco de abas distintas** poderá receber, no futuro, a hipótese `many_to_many_relationship_candidate` somente quando uma aba já tiver classificação draft de dimensão padrão e a outra já tiver classificação draft de fato transacional ou periódico. A futura regra exigirá exatamente uma chave física elegível no lado dimensional, completa e não única; exatamente uma referência física elegível no fato, completa e não única; cobertura referencial agregada integral e uma única direção elegível.

A hipótese não confirma uma relação muitos-para-muitos no modelo, não identifica valores repetidos, não aponta linhas, não enumera chaves e não recomenda tabela ponte, direção de filtro ou alteração no Power BI. Ela somente solicita confirmação humana antes de qualquer orientação de modelagem.

As futuras evidências serão estritamente agregadas: classificações de tabela, quantidades de chaves e referências elegíveis, contagens de linhas observadas, completude, unicidade, cobertura referencial, quantidade de direções candidatas e indicadores de fórmulas, sensibilidade, conflito e ambiguidade. Nenhum título de aba, cabeçalho, valor, posição, par correspondente, frequência individual, exemplo, chave ou identificador poderá alcançar o perfil persistível, a saída, o contrato ou os logs.

Fórmulas, sensibilidade, chaves ou referências incompletas, cobertura parcial ou zero, mais de uma chave ou referência elegível, mais de uma direção, autorreferência, dimensão calendário, fato sem granularidade, classificação indefinida, conflito, relação 1:1 ou qualquer ambiguidade bloqueiam a emissão. A política não usa semelhança livre de nomes, contexto de negócio, títulos de abas ou cabeçalhos para inferir a condição.

A hipótese proposta terá confiança `0.75`, severidade `warning` e pergunta humana bloqueante. Ela não confirma chave primária ou estrangeira, não confirma erro de negócio, não cria relação e não altera o modelo Power BI. A produção permanece bloqueada.

## Alternativa B — bloqueio silencioso

Como alternativa mais restritiva, o motor poderia apenas bloquear outras hipóteses relacionais ao perceber não unicidade dos dois lados. Essa alternativa reduz interpretações, porém esconde uma condição estrutural que merece revisão explícita.

## Controle de autorização

**A Proposta A ainda não foi aprovada por Chris.** A aprovação desta política, se ocorrer, não autorizará por si só perfil, classificador, registro, contrato, pipeline, catálogo, testes executáveis, dataset golden, calibração, ativação draft ou produção. Um gate de reconstrução e uma autorização específica posterior continuarão obrigatórios.
