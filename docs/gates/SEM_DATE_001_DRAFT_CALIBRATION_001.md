# SEM-DATE-001 — Gate de Calibração Draft

**Gate:** `SEM-DATE-001-DRAFT-CALIBRATION-001`  
**Status:** aprovado para perfil draft controlado.  
**Política vinculada:** `SEM_DATE_001_POLICY_PROPOSAL_001.md` (Proposta A aprovada por Chris).

| Evidência | Resultado |
|---|---|
| Golden dataset | `GD-SEM-DATE-001-001` |
| SHA-256 | `ce22b8df5bf00b7dee3cce6bf939bc5217b430c3bae0e955f3eb31fc234a5aac` |
| Calibração | 3 TP, 0 FP, 0 FN |
| Limiar | Pelo menos 10 valores não ausentes e 100% reconhecidos |
| Formatos textuais | `AAAA-MM-DD`, `DD-MM-AAAA`, `DD/MM/AAAA` com calendário estrito |

> A regra classifica apenas `date_generic`, com confiança 0,85, e solicita confirmação humana não bloqueante. Evidências contêm exclusivamente contagens, razões e base técnica; dados brutos, cabeçalhos, posições e títulos de aba não são projetados.

A autorização é limitada ao **perfil draft**. A promoção para produção requer calibração ampliada, revisão de privacidade e gate produtivo próprio; este documento não remove nenhum bloqueio de produção.
