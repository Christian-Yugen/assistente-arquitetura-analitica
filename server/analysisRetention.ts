export type ReferenceRemovalAudit = {
  storageKey: null;
  retentionStatus: "reference_removed";
  referenceRemovedAt: Date;
};

/**
 * Representa o limite atual de retenção: a aplicação deixa de ter caminho ou credencial
 * para recuperar a planilha e guarda apenas o registro mínimo de auditoria no banco.
 * A exclusão física exige uma operação oficial de deleção no armazenamento.
 */
export function buildReferenceRemovalAudit(removedAt = new Date()): ReferenceRemovalAudit {
  return { storageKey: null, retentionStatus: "reference_removed", referenceRemovedAt: removedAt };
}
