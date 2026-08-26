import { readFileSync } from "node:fs";
import { resolve } from "node:path";
import { describe, expect, it } from "vitest";

const root = resolve(import.meta.dirname, "..");

describe("production lineage reconciliation boundaries", () => {
  it("registra 95 regras draft e preserva todos os bloqueios de produção", () => {
    const document = readFileSync(resolve(root, "docs/gates/PRODUCTION_LINEAGE_RECONCILIATION_001.md"), "utf8");
    expect(document).toContain("95 regras `executable_draft`");
    expect(document).toContain("zero `intake_required`");
    expect(document).toContain("não autoriza produção");
    expect(document).toContain("Exclusão física do objeto privado");
    expect(document).toContain("Calibração para produção");
    expect(document).toContain("Testes ponta a ponta");
    expect(document).toContain("Linhagem canônica da QLT-NULL-001");
    expect(document).toContain("Reconciliação de intakes");
    expect(document).toContain("requer autorização explícita de Chris");
  });

  it("mantém a proposta de migração aditiva e sem alteração de runtime", () => {
    const proposal = readFileSync(resolve(root, "docs/gates/INTAKE_LINEAGE_MIGRATION_PROPOSAL_001.md"), "utf8");
    expect(proposal).toContain("normalização aditiva e versionada");
    expect(proposal).toContain("não altera a allowlist, o contrato, o pipeline");
    expect(proposal).toContain("não sobrescreverá o intake histórico");
    expect(proposal).toContain("produção segue bloqueada");
    expect(proposal).toContain("exige autorização explícita de Chris");
  });
});
