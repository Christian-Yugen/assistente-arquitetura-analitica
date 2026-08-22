# REL-ONEMANY-001 — Proposta de Política 001

## Proposta A — hipótese conservadora de relacionamento um-para-muitos

Um **par opaco de abas candidatas** somente poderá receber a hipótese `one_to_many_relationship_candidate` quando uma aba já tiver classificação draft de dimensão padrão e a outra já tiver classificação draft de fato transacional ou fato periódico. A futura regra exigirá exatamente uma chave física não sensível, completa e única na dimensão candidata; exatamente uma referência física não sensível e completa no fato candidato; e cobertura referencial integral da referência no conjunto de chaves da dimensão, calculada transitoriamente em memória.

O resultado não cria relacionamento, não confirma chave primária ou estrangeira, não escolhe direção de filtro e não altera modelo Power BI. Ele apenas registra uma hipótese 1:N para confirmação humana. A Proposta A exige que o par seja composto por abas distintas, que exista somente uma direção elegível no par e que a referência do fato não seja única. Isso evita que relações 1:1 sejam apresentadas como 1:N.

As evidências futuras serão exclusivamente agregadas: contagens de linhas, quantidades de chaves e referências elegíveis, cardinalidades agregadas, cobertura referencial agregada, quantidade de direções candidatas e indicadores booleanos de completude, unicidade, fórmulas, sensibilidade, conflito e ambiguidade. A regra não projeta, persiste ou expõe títulos de abas, cabeçalhos, valores, posições, pares correspondentes, frequências individuais, exemplos, chaves ou identificadores.

Fórmulas, sinais sensíveis, chaves ou referências incompletas, cobertura referencial parcial, nenhuma correspondência, mais de uma direção ou par elegível, autorreferência, cardinalidade 1:1, muitos-para-muitos, classificação indefinida, fato sem granularidade definida, dimensão calendário, conflito entre classificações ou qualquer ambiguidade bloqueiam a emissão. A política não usa semelhança livre de nomes, contexto de negócio ou títulos de abas para inferir relacionamentos.

A hipótese proposta tem confiança `0,85`, severidade informativa e pergunta humana bloqueante para confirmar a relação antes de qualquer recomendação de modelo. Produção permanece bloqueada.

## Alternativa B — pergunta guiada sem hipótese automática

Como alternativa mais restritiva, a regra não emitiria hipótese de relacionamento e formularia apenas uma pergunta humana caso um par de abas tivesse classificações compatíveis. Essa alternativa reduz ainda mais o risco de falso positivo, mas perde a evidência agregada que permite ao revisor priorizar uma validação 1:N objetiva.

## Estado

**Proposta A pendente de aprovação explícita de Chris.** Este documento é não executável. Não autoriza perfil, classificador, registro, contrato, pipeline, catálogo, testes, dataset golden, calibração, ativação draft ou produção. Mesmo após eventual aprovação da política, a implementação continuará dependente de gate de reconstrução e de autorização explícita posterior de Chris.
