import { readFileSync } from "node:fs";
import { resolve } from "node:path";
import { describe, expect, it } from "vitest";

const root = resolve(import.meta.dirname, "..");

describe("ALT-AMBIG-005 draft activation", () => {
  it("preserves authorized aggregate-only policy and production block", () => {
    const intake = readFileSync(resolve(root, "artifacts/intake/ALT-AMBIG-005.json"), "utf8");
    const policy = readFileSync(resolve(root, "docs/rules/ALT_AMBIG_005_POLICY_PROPOSAL_001.md"), "utf8");
    const gate = readFileSync(resolve(root, "docs/gates/ALT_AMBIG_005_RECONSTRUCTION_AUTHORIZATION_001.md"), "utf8");
    expect(intake).toContain('"local_readiness": "executable_draft"');
    expect(intake).toContain('"implementation_authorized": true');
    expect(policy).toContain("sinais já inferidos, independentes, opacos e agregados");
    expect(policy).toContain("não decidirá uma solução de modelagem");
    expect(gate).toContain("sim, autorizado");
    expect(gate).toContain("Produção permanece bloqueada");
  });
});
