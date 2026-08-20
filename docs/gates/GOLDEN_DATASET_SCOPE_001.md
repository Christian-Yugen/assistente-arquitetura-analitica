# GOLDEN-DATASET-SCOPE-001 — Escopo de Calibração do Draft

**Status:** aprovado para construção de fixtures determinísticas.  
**Escopo:** somente `QLT-NUMTEXT-007` e `QLT-NULL-001@0.1.0-reconstructed.1`.

Os golden datasets deste ciclo são fixtures de regressão propositalmente pequenas, sem dados reais, sem valores pessoais e sem aleatoriedade. Eles não representam uma amostra estatística de produção. Seu objetivo é fixar decisões aprovadas de limiar, severidade, confiança, não aplicabilidade e coexistência entre as duas regras atualmente autorizadas no perfil draft.

| Regra | Cenários positivos | Cenários negativos ou excluídos | Expectativa controlada |
|---|---|---|---|
| `QLT-NULL-001` | Ausências estruturais, texto em branco e `NaN` nas faixas baixa, média e alta. | Coluna vazia integral, sentinelas textuais e fórmulas. | Finding, severidade, confiança e pergunta somente nas condições definidas no baseline reconstruído. |
| `QLT-NUMTEXT-007` | Texto numérico estrito nas faixas menor que 5%, de 5% a menor que 50% e a partir de 50%. | Coluna física numérica, base não canônica, candidatos ausentes e ambiguidade controlada. | Finding, severidade, confiança e pergunta somente quando o perfil for aplicável. |
| Interação draft | Coluna que contenha simultaneamente ausência e texto numérico. | Nenhuma regra deve suprimir ou alterar a evidência aprovada da outra. | Dois findings independentes, com IDs e evidências correspondentes. |

| Medida de calibração | Critério de aceitação draft |
|---|---|
| Verdadeiro positivo | Cada fixture positiva produz o finding e a severidade esperados. |
| Verdadeiro negativo | Cada fixture excluída ou não aplicável não produz o finding correspondente. |
| Falso positivo conhecido | Zero nos cenários de não aplicabilidade definidos nesta matriz. |
| Falso negativo conhecido | Zero nos cenários positivos definidos nesta matriz. |
| Privacidade | Diagnóstico serializado não contém valores de células, títulos originais de abas ou dados pessoais. |

> A aprovação desta matriz valida somente a calibração determinística do draft. Ela não fornece sensibilidade estatística para dados de produção, não autoriza promoção de ambiente e não substitui a futura calibração com datasets representativos aprovados.
