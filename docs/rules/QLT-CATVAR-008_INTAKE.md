# Intake — QLT-CATVAR-008: Variações de Categoria

| Item | Fonte ou decisão |
|---|---|
| ID | `QLT-CATVAR-008` |
| Título | Variações de categoria |
| Propósito oficial | Detectar grafias potencialmente equivalentes. |
| Prioridade | P1 |
| Escopo | Coluna |
| Dependência | `profiling` |
| Estado da fonte | `planned` |
| Estado local | `intake_required` |

O blueprint oficial define o **objetivo**, mas não a política operacional. Em particular, ele não decide se diferenças de caixa, acentuação, pontuação, abreviação, singular/plural ou distância textual devem ser tratadas como equivalência. Essas escolhas podem alterar o significado de categorias de negócio e não devem ser inferidas silenciosamente.

> **Decisão:** a QLT-CATVAR-008 permanece não executável até que uma política de normalização e um gate de autorização sejam aprovados. O intake preserva a ordem do catálogo sem inventar a condição da regra.
