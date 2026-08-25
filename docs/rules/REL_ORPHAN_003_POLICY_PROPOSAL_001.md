# REL-ORPHAN-003 — Proposta de Política 001

## Estado não executável

Esta proposta recupera somente os limites ausentes do blueprint para a regra **Registros órfãos**. Ela não cria perfil, classificador, registro, contrato, pipeline, catálogo, testes executáveis, dataset golden, calibração ou ativação draft. A regra e a produção permanecem bloqueadas até decisão humana posterior.

## Proposta A — alerta conservador de cobertura referencial parcial

Um **par opaco de abas distintas** poderá receber, no futuro, a hipótese `orphan_reference_candidate` somente quando uma aba já tiver classificação draft de dimensão padrão e a outra já tiver classificação draft de fato transacional ou periódico. A futura regra exigirá exatamente uma chave física elegível no lado dimensional, completa e única; exatamente uma referência física elegível no fato, completa e não única; e uma única direção elegível.

A condição positiva exige uma cobertura referencial estritamente entre `0.0` e `1.0`, com contagem agregada positiva de referências distintas não cobertas. A hipótese não identifica valores órfãos, não aponta linhas, não enumera chaves, não calcula frequências individuais e não propõe preencher, excluir, remapear ou criar dimensões. Ela somente solicita uma revisão humana antes de qualquer orientação de modelagem.

As futuras evidências serão estritamente agregadas: classificações de tabela, quantidades de chaves e referências elegíveis, contagens de linhas observadas, completude, unicidade, cobertura referencial, quantidade agregada de referências não cobertas, quantidade de direções candidatas e indicadores de fórmulas, sensibilidade, conflito e ambiguidade. Nenhum título de aba, cabeçalho, valor, posição, par correspondente, frequência individual, exemplo, chave ou identificador poderá alcançar o perfil persistível, a saída, o contrato ou os logs.

Fórmulas, sensibilidade, chaves ou referências incompletas, cobertura igual a `0.0` ou `1.0`, ausência de correspondências, mais de uma chave ou referência elegível, mais de uma direção, autorreferência, dimensão calendário, fato sem granularidade, classificação indefinida, conflito, relação 1:1, padrão muitos-para-muitos ou qualquer ambiguidade bloqueiam a emissão. A política não usa semelhança livre de nomes, contexto de negócio, títulos de abas ou cabeçalhos para inferir a condição.

A hipótese proposta terá confiança `0.80`, severidade `warning` e pergunta humana bloqueante para revisar a cobertura parcial antes de qualquer recomendação de relacionamento. Ela não confirma uma chave primária ou estrangeira, não confirma erro de negócio, não cria relação e não altera o modelo Power BI. A produção permanece bloqueada.

## Alternativa B — pergunta guiada sem hipótese automática

Como alternativa mais restritiva, a regra futura poderia apenas perguntar ao revisor se há referências sem cobertura quando o par tiver classificações compatíveis, sem emitir hipótese. Essa alternativa reduz ainda mais o risco de falso positivo, mas descarta a evidência agregada que permite priorizar uma revisão objetiva.

## Controle de autorização

**A Proposta A foi aprovada explicitamente por Chris.** Esta aprovação não autoriza por si só perfil, classificador, registro, contrato, pipeline, catálogo, testes executáveis, dataset golden, calibração, ativação draft ou produção. O gate de reconstrução formalizado e uma autorização específica posterior continuam obrigatórios antes de qualquer implementação.
