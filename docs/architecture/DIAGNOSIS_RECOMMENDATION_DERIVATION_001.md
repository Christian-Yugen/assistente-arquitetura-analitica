# DIAGNOSIS-RECOMMENDATION-DERIVATION-001 — Recomendações Derivadas no Diagnóstico Draft

**Status:** implementado para as regras executáveis do perfil draft.  
**Escopo:** recomendações de qualidade derivadas de findings; não há recomendação automática de modelo dimensional completo.

O pipeline não inventa recomendações de modelagem dimensional quando as categorias semânticas, fatos, dimensões, relacionamentos e métricas ainda não foram autorizadas. Em vez disso, cada finding produzido por uma regra executável traz uma recomendação específica, rastreável e condicionada à evidência agregada da coluna afetada.

| Regra | Condição observada | Recomendação derivada |
|---|---|---|
| `QLT-NUMTEXT-007` | Valores predominantemente numéricos armazenados como texto. | Validar a conversão do tipo da coluna antes de definir o tratamento analítico. |
| `QLT-NULL-001` | Ausências estruturais acima dos limiares aprovados. | Validar a regra de preenchimento, exclusão ou tratamento de ausência antes de modelar a coluna. |

O adaptador `engine/contracts/diagnosis.py` preserva `finding["recommendation"]` no campo canônico `findings[].recommendation`. `engine/pipeline/quality_diagnosis.py` apenas agrega essas recomendações derivadas aos findings; `summary.next_recommended_action` e `proposed_model` permanecem marcadores governados do resultado parcial, conforme o perfil draft.

> As recomendações atuais orientam validação humana de qualidade. Elas não classificam automaticamente fatos ou dimensões, não propõem relacionamentos e não autorizam modelo Power BI de produção.
