# MANUAL-DO-USUARIO-MVP-DRAFT-001 — Uso Controlado

Este manual descreve o uso do MVP no perfil **draft**. O resultado é um diagnóstico de qualidade estruturado para apoiar validação humana; ele não é uma aprovação automática de arquitetura Power BI nem uma autorização para produção.

## Iniciar uma análise

Após autenticar-se, informe um nome de projeto, um objetivo e selecione uma planilha `.xlsx`. O arquivo deve ter até **25 MB** e entre **1 e 10 abas**. Durante o processamento, o formulário fica bloqueado e o painel exibe etapas qualitativas, sem percentual ou tempo estimado fabricado. Caso a validação falhe, corrija o arquivo e envie novamente; mensagens de falha não expõem detalhes internos do conteúdo.

## Interpretar o diagnóstico

Ao concluir, selecione a versão no histórico do projeto. A tela apresenta achados de qualidade, evidências agregadas, recomendações, perguntas de validação e a versão do diagnóstico. Uma pergunta bloqueante precisa de confirmação humana porque pode alterar a interpretação de uma coluna, por exemplo, distinguir medida de código quando números foram armazenados como texto.

| Elemento exibido | Como usar | Limite do perfil draft |
|---|---|---|
| Finding | Leia a evidência, o impacto e a recomendação associados à regra. | O finding não modifica a planilha original. |
| Pergunta | Valide o significado de negócio com o responsável pelos dados. | A resposta não cria automaticamente um modelo completo. |
| Histórico | Compare versões pertencentes ao mesmo projeto e proprietário. | Não é possível acessar recursos de outro usuário. |
| Exportação JSON | Baixe o diagnóstico selecionado para integração ou auditoria. | Exportação PDF está indisponível neste perfil. |

## Privacidade e retenção

O MVP mascara CPF, e-mail e nomes explicitamente rotulados nos metadados e evita persistir valores brutos no diagnóstico. Depois da análise, a referência privada ao arquivo é removida da aplicação, preservando metadados mínimos de auditoria. Essa remoção **não é exclusão física** no provedor de armazenamento; por isso, não utilize o MVP para dados cujo requisito exija garantia imediata de eliminação definitiva.

## Limitações conhecidas

Atualmente somente `QLT-NUMTEXT-007` e `QLT-NULL-001` são regras executáveis calibradas. Não há interpretação semântica por LLM, inferência automática de fatos e dimensões, proposta de relacionamentos, métricas prontas ou recomendação de produção. Use os resultados como base de triagem e validação, mantendo a decisão de modelagem sob responsabilidade humana.
