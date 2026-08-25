# O que estamos construindo — Assistente de Arquitetura Analítica

**Destinatário:** Chris  
**Estado de referência:** workspace reconciliado com **42 regras executáveis somente em draft**  
**Propósito deste documento:** explicar de forma direta o produto, o motivo da arquitetura, o que já funciona e o que ainda impede chamá-lo de produto pronto para produção.

---

## 1. A ideia central

Estamos construindo um **assistente de diagnóstico para planilhas Excel** que ajuda a transformar uma planilha operacional em uma proposta de arquitetura analítica para Power BI. Ele não é apenas um “leitor de Excel”, nem um gerador automático de dashboards. Seu trabalho é ler a estrutura de um workbook, identificar riscos de qualidade, hipóteses de significado, possíveis fatos, dimensões, granularidade e relacionamentos, e então apresentar **recomendações que exigem validação humana**.

> Em termos simples: o sistema ajuda a responder “o que esta planilha parece representar, quais problemas impedem uma boa modelagem e o que preciso confirmar antes de criar o modelo no Power BI?”.

O resultado esperado para o usuário não é uma decisão automática. É um diagnóstico rastreável, por exemplo: “esta coluna parece uma data”, “esta tabela parece uma dimensão”, “há uma chave possivelmente não única no lado 1” ou “há valores ausentes relevantes”. Cada conclusão relevante traz evidências agregadas, confiança limitada e uma pergunta de revisão.

## 2. O problema de negócio que o site resolve

Planilhas são frequentemente usadas como fonte para relatórios, mas costumam chegar ao Power BI com problemas silenciosos: cabeçalhos inconsistentes, dados mistos, datas inválidas, chaves incompletas, tabelas sem granularidade clara, dimensões misturadas com fatos e relações ambíguas.

Esses problemas produzem relatórios aparentemente corretos, mas com medidas duplicadas, filtros errados, totais inflados ou relações que não representam o processo de negócio. Corrigir isso depois que o dashboard já está em uso é caro e arriscado.

O MVP busca antecipar essa etapa. Antes de modelar, ele cria um **mapa de qualidade e estrutura** da planilha. Assim, o analista humano pode decidir conscientemente o que é uma tabela de fatos, uma dimensão, uma chave, uma relação válida ou uma exceção do processo.

| Sem o assistente | Com o assistente em draft |
|---|---|
| A pessoa abre a planilha e interpreta tudo manualmente. | O sistema reúne sinais estruturais e apresenta hipóteses revisáveis. |
| Erros podem ser encontrados apenas depois de um dashboard pronto. | Riscos de modelagem podem ser vistos antes da construção do modelo. |
| Regras de decisão podem ficar implícitas na experiência de cada analista. | Regras ficam versionadas, testadas, calibradas e auditáveis. |
| Uma coincidência de nomes pode virar uma relação incorreta. | Relações só são sugeridas sob guardas conservadoras e confirmação humana. |

## 3. Como o fluxo do site funciona

O fluxo principal é deliberadamente simples para o usuário, mas rigoroso no servidor.

1. **Autenticação e escopo.** Chris entra no sistema. Projetos, arquivos, diagnósticos e versões são tratados no escopo do proprietário autenticado.
2. **Envio da planilha.** O usuário informa o nome do projeto, o objetivo da análise e envia um arquivo `.xlsx`.
3. **Validação antes de persistir.** O servidor verifica extensão, MIME permitido, codificação, assinatura ZIP, tamanho máximo de **25 MB** e limite de **1 a 10 abas**. A estrutura do XLSX é aberta de forma controlada antes de seguir para análise.
4. **Profiling no servidor.** O motor Python percorre a planilha em modo de leitura controlado e reduz o conteúdo a contagens, proporções, tipos físicos, indicadores e outros sinais agregados.
5. **Execução das regras draft autorizadas.** As regras disponíveis avaliam somente os perfis agregados compatíveis com cada hipótese. Elas não recebem uma licença geral para inferir livremente o negócio.
6. **Diagnóstico canônico.** O servidor gera um objeto de diagnóstico versionado com achados, classificações, perguntas humanas, limitações e propostas de próximos passos.
7. **Consulta pelo usuário.** O diagnóstico é exibido no workspace, onde o analista pode revisar as hipóteses antes de levar a decisão para o modelo Power BI.

## 4. O que significa “perfil draft”

O termo **draft** é central. Não significa que o site é falso ou apenas visual. Significa que as regras disponíveis estão funcionando em um ambiente de experimento controlado, sob limites explícitos.

| Perfil draft protegido | Produção |
|---|---|
| Regras executam apenas quando estão explicitamente autorizadas em catálogo. | Regras só poderiam executar após validação operacional e gate de produção. |
| A saída é uma hipótese, achado ou pergunta humana. | A saída poderia apoiar decisões operacionais com confiança maior e controles completos. |
| O sistema não cria relações nem altera dados ou modelos Power BI. | Mesmo em produção, alterações automáticas exigiriam governança própria; não estão no escopo atual. |
| Calibração limitada por regra, com datasets sintéticos e revisão. | Calibração ampliada, monitoramento e evidências operacionais são necessários. |
| Produção permanece bloqueada. | Ainda não autorizado. |

Portanto, **draft é o ambiente correto para aprender com segurança**. Ele permite testar o motor sobre planilhas reais sem fingir que uma inferência estatística ou estrutural substitui o conhecimento do analista.

## 5. As regras: por que existem 95 e por que só 42 estão ativas

O projeto possui um catálogo oficial de **95 slots de regras**. Isso é o mapa completo do que o produto pretende analisar, dividido entre qualidade, tipagem semântica, granularidade, fato e dimensão, relacionamentos, métricas e alertas.

Atualmente, o workspace reconciliado apresenta **42 regras executáveis em draft**. As demais ainda permanecem como referência ou exigem um ciclo formal de definição. Isso é intencional: uma regra não entra no motor apenas porque possui nome no catálogo.

Cada regra precisa atravessar um ciclo de governança:

1. **Intake:** registrar objetivo, dependências, lacunas da fonte e riscos.
2. **Proposta de política:** escolher uma definição conservadora, incluindo condição, exclusões, evidência, severidade, confiança e pergunta humana.
3. **Aprovação humana:** Chris escolhe ou aprova a proposta.
4. **Gate de reconstrução:** sela o escopo e deixa claro o que ainda não está autorizado.
5. **Autorização específica de implementação:** separada da aprovação de política.
6. **Implementação e testes:** perfil privado, classificador determinístico, contrato, pipeline e catálogo.
7. **Golden dataset sintético e calibração:** medir verdadeiros positivos, falsos positivos e falsos negativos.
8. **Gate individual de draft:** só então a regra pode entrar na allowlist executável.

Esse processo é mais lento que adicionar regras por tentativa e erro, mas reduz o risco de o sistema sugerir decisões estruturais erradas com aparência de certeza.

## 6. Exemplos concretos do que o motor já procura

As regras ativas não cobrem todo o catálogo, mas já exercitam as principais camadas do produto.

| Camada | Exemplos de perguntas que o assistente consegue estruturar |
|---|---|
| Qualidade | Há nulos relevantes, duplicidades, colunas ou linhas vazias, números gravados como texto, fórmulas inconsistentes, datas inválidas, valores extremos ou cabeçalhos problemáticos? |
| Tipagem semântica | Uma coluna parece data, competência, identificador, quantidade, valor monetário, percentual, descrição, categoria, localização, responsável, meta, realizado ou dado sensível? |
| Granularidade | A linha parece representar evento, entidade, chave explícita, chave composta ou um caso ainda ambíguo? |
| Fato e dimensão | Uma aba parece dimensão padrão, dimensão calendário, fato transacional, fato periódico, fato sem granularidade ou classificação indefinida? |
| Relacionamentos | Uma relação 1:N é estruturalmente plausível? O lado que deveria ser único tem duplicidade? Há referências parcialmente cobertas, sem revelar valores? |

As regras relacionais são particularmente sensíveis. A REL-ONEMANY-001 somente sugere uma hipótese 1:N quando existe uma dimensão e um fato compatíveis, uma chave completa e única, uma referência completa e não única, cobertura referencial integral e direção única. A REL-NONUNIQ-002, ativa em draft na versão reconciliada, faz o oposto: alerta quando o lado que deveria ser “1” aparenta **não ser único**. Nenhuma delas cria uma relação automaticamente.

## 7. Privacidade, segurança e limites de retenção

O produto trata planilhas como material potencialmente sensível. Por isso, o desenho separa deliberadamente o acesso transitório ao arquivo do diagnóstico que permanece disponível.

| Controle | Objetivo |
|---|---|
| Análise no servidor | Evitar que valores da planilha sejam processados no navegador como resultado do diagnóstico. |
| Escopo por `ownerId` | Impedir que um usuário consulte projetos, arquivos ou diagnósticos de outro proprietário. |
| Mascaramento | Evitar que elementos reconhecidos como sensíveis alcancem saídas, perguntas ou evidências. |
| Perfil agregado | Reduzir dados de célula a contagens, razões, tipos e indicadores antes da execução de regras. |
| Pares opacos de abas | Nas regras de relacionamento, impedir a exposição de títulos, cabeçalhos, posições, pares de valor ou chaves. |
| Arquivo privado temporário | O arquivo é usado para a análise e sua referência de retenção é removida após a conclusão; o diagnóstico preserva somente metadados mínimos autorizados. |
| Bloqueio de produção | Evitar que o produto seja apresentado como pronto antes da validação completa dos controles. |

Há um ponto que precisa ser tratado com transparência: durante a investigação recente, o coletor de rede de desenvolvimento registrou o payload da requisição de upload em base64. Isso significa que o controle de **logs seguros no ambiente de desenvolvimento ainda precisa de endurecimento explícito** antes de qualquer alegação de prontidão produtiva. O conteúdo não será reproduzido nem utilizado, mas o fato deve orientar a priorização de correção e uma revisão de observabilidade.

## 8. O que o site não faz hoje

É importante alinhar expectativa. Hoje, o MVP **não**:

- gera automaticamente um arquivo `.pbix`;
- cria relações, exclui duplicidades ou corrige valores da planilha;
- decide sozinho o significado de uma coluna;
- garante que uma relação sugerida corresponde ao processo de negócio;
- possui as 95 regras em estado executável;
- está autorizado para produção;
- concluiu a exclusão física verificável de todos os objetos após retenção;
- substitui o arquiteto de dados, o analista de negócio ou o administrador do Power BI.

Ele é uma camada de **diagnóstico e preparação de decisão**. A decisão de modelagem continua humana.

## 9. O que já faz sentido e o que ainda precisa fazer sentido

O trabalho faz sentido se o objetivo for construir uma ferramenta que reduza risco antes da modelagem dimensional, com decisões auditáveis e sem expor dados. A parte difícil não é identificar que uma coluna “parece um ID”; é garantir que essa hipótese não se transforme silenciosamente em uma decisão errada, invasiva ou impossível de explicar depois.

O investimento em regras, testes, datasets sintéticos, calibração e gates é justamente o que transforma uma coleção de heurísticas em um produto confiável o suficiente para auxiliar uma equipe real.

Ainda assim, antes de chamar o projeto de versão 1.0 produtiva, precisamos fechar quatro grupos de trabalho:

1. **Cobertura funcional:** completar as regras planejadas que fizerem sentido para o escopo final, sem ativar regras apenas para atingir uma contagem.
2. **Confiabilidade:** ampliar a calibração contra cenários sintéticos e revisar falsos positivos e falsos negativos por regra.
3. **Segurança e operações:** corrigir o registro de payloads no coletor de rede de desenvolvimento, validar exclusão física, retenção e observabilidade segura.
4. **Experiência de usuário:** consolidar a tela de resultados, as perguntas humanas, a revisão de hipóteses e a exportação útil para o fluxo Power BI.

## 10. A decisão que precisamos tomar antes de avançar

Antes de criar a próxima regra, vale validar se este é o produto que você quer:

> Um assistente de arquitetura analítica que prepara e explica decisões de modelagem, mas nunca se comporta como um gerador automático e opaco de relações ou dashboards.

Se essa direção estiver correta, a próxima etapa deve ser priorizar, junto com a expansão de regras, os controles de segurança restantes e uma experiência clara de revisão humana. Se você desejar algo diferente — por exemplo, geração de modelo Power BI, mapeamento manual assistido, catálogo de dados, dicionário de negócio ou integração direta com fontes corporativas — podemos ajustar o plano antes de continuar aumentando o motor.
