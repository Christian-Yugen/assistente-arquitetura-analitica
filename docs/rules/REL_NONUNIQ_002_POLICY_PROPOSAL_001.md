# REL-NONUNIQ-002 — Proposta de Política 001

## Estado não executável

Esta proposta recupera somente os limites ausentes do blueprint para a regra **Chave não única no lado 1**. Ela não cria perfil, classificador, registro, contrato, pipeline, catálogo, testes executáveis, dataset golden, calibração ou ativação draft. A regra e a produção permanecem bloqueadas até decisão humana posterior.

## Proposta A — alerta conservador de chave não única no lado 1

Um **par opaco de abas distintas** poderá receber, no futuro, a hipótese `one_side_key_non_unique_candidate` somente quando uma aba já tiver classificação draft de dimensão padrão e a outra já tiver classificação draft de fato transacional ou periódico. A futura regra exigirá exatamente um candidato físico elegível de chave no lado dimensional, exatamente uma referência física elegível no lado fato, completude integral de ambos os sinais, cobertura referencial integral e uma única direção elegível.

A condição positiva exige que a chave do lado dimensional seja **não única**, demonstrada exclusivamente por uma contagem agregada positiva de duplicidades e por um indicador agregado de unicidade falso. A hipótese não identifica a chave duplicada, não aponta linhas, não enumera valores, não calcula frequências individuais e não sugere remover, consolidar ou escolher registros. Ela apenas alerta que o lado que seria o lado 1 não satisfaz a unicidade necessária e requer confirmação humana antes de qualquer modelagem.

As futuras evidências serão estritamente agregadas: classificações de tabela, quantidades de chaves e referências elegíveis, contagens de linhas observadas, completude, unicidade, quantidade agregada de duplicidades, cobertura referencial, quantidade de direções candidatas e indicadores de fórmulas, sensibilidade, conflito e ambiguidade. Nenhum título de aba, cabeçalho, valor, posição, par correspondente, frequência individual, exemplo, chave ou identificador poderá alcançar o perfil persistível, a saída, o contrato ou os logs.

Fórmulas, sensibilidade, chaves ou referências incompletas, cobertura referencial inferior a `1.0`, ausência de correspondências, mais de uma chave ou referência elegível, mais de uma direção, autorreferência, dimensão calendário, fato sem granularidade, classificação indefinida, conflito, relação 1:1, padrão muitos-para-muitos ou qualquer ambiguidade bloqueiam a emissão. A política não usa semelhança livre de nomes, contexto de negócio, títulos de abas ou cabeçalhos para inferir a condição.

A hipótese proposta terá confiança `0.80`, severidade `warning` e pergunta humana bloqueante para revisar a unicidade do lado 1 antes de qualquer recomendação de relacionamento. Ela não confirma qual coluna deve ser chave, não confirma duplicidade de negócio, não deduz chave substituta, não cria uma relação e não altera o modelo Power BI. A produção permanece bloqueada.

## Alternativa B — pergunta guiada sem hipótese automática

Como alternativa mais restritiva, a regra futura poderia apenas perguntar ao revisor se o lado dimensional possui chave única quando o par tiver classificações compatíveis, sem emitir hipótese. Essa alternativa reduz o risco de falso positivo, mas também descarta a evidência agregada que permite priorizar a revisão de uma condição estrutural objetiva.

## Controle de autorização

**A Proposta A ainda não foi aprovada por Chris.** A aprovação desta política, se ocorrer, não autorizará por si só perfil, classificador, registro, contrato, pipeline, catálogo, testes executáveis, dataset golden, calibração, ativação draft ou produção. Um gate de reconstrução e uma autorização específica posterior continuarão obrigatórios.
