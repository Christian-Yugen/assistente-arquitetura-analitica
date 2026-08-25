import { describe, expect, it } from "vitest";
import { readFileSync } from "node:fs";
import { resolve } from "node:path";

const delegationPath = resolve(import.meta.dirname, "../docs/governance/PROPOSAL_A_APPROVAL_DELEGATION_001.md");

describe("PROPOSAL-A-APPROVAL-DELEGATION-001", () => {
  it("allows only unchanged Proposal A approvals and preserves separate authorization gates", () => {
    const delegation = readFileSync(delegationPath, "utf8");

    expect(delegation).toContain("somente a aprovação de uma Proposta A");
    expect(delegation).toContain("não autoriza automaticamente implementação");
    expect(delegation).toContain("autorização específica de implementação");
    expect(delegation).toContain("mudança material");
    expect(delegation).toContain("produção permanece bloqueada");
  });
});
