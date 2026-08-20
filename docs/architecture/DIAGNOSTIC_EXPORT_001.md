# DIAGNOSTIC-EXPORT-001 — Exportação Estruturada do Diagnóstico

**Status:** exportação JSON implementada para o MVP draft.  
**Escopo de acesso:** somente uma versão já retornada por `analysis.getDiagnostic`, procedimento autenticado e filtrado por proprietário.

O painel de diagnóstico apresenta a ação **Exportar JSON** apenas após o carregamento da versão selecionada. A ação usa o objeto já autorizado pela consulta owner-scoped; ela não recebe identificadores adicionais, não cria rota pública e não tenta recuperar o workbook original. O arquivo é composto no navegador, por URL de objeto temporária revogada logo após a solicitação de download.

| Campo de exportação | Origem | Finalidade |
|---|---|---|
| `export_format` | Constante do exportador | Identifica o envelope JSON da plataforma. |
| `contract_version` | Versão persistida do diagnóstico | Permite interpretar o payload conforme o contrato canônico. |
| `diagnostic_id`, `project_id`, `version` | Versão owner-scoped selecionada | Mantém rastreabilidade da exportação. |
| `payload` | Diagnóstico canônico persistido | Entrega achados, perguntas e evidências estruturadas já sujeitas às proteções de sanitização. |

> A exportação em PDF permanece **indisponível** no MVP draft. Não há botão ou arquivo simulado para esse formato. A sua implementação depende de especificação de layout, controles de privacidade equivalentes e uma etapa própria de validação de qualidade visual.

As provas automatizadas em `client/src/lib/diagnosticExport.test.ts` validam o envelope, o nome de arquivo, a URL temporária e a sua revogação. `client/src/pages/Home.test.tsx` confirma que a ação aparece apenas quando o diagnóstico autorizado já está carregado.
