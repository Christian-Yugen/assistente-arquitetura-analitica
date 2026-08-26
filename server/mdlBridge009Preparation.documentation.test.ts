import { readFileSync } from "node:fs";
import { resolve } from "node:path";
import { describe, expect, it } from "vitest";

const root = resolve(import.meta.dirname, "..");

describe("MDL-BRIDGE-009 policy boundaries", () => {
  it("preserva a Proposta A e o bloqueio produtivo após a autorização draft", () => {
    const intake = JSON.parse(readFileSync(resolve(root, "artifacts/intake/MDL-BRIDGE-009.json"), "utf8"));
    const policy = readFileSync(resolve(root, "docs/rules/MDL_BRIDGE_009_POLICY_PROPOSAL_001.md"), "utf8");
    const gate = readFileSync(resolve(root, "docs/gates/MDL_BRIDGE_009_RECONSTRUCTION_AUTHORIZATION_001.md"), "utf8");
    expect(intake.local_readiness).toBe("executable_draft");
    expect(intake.authorization.implementation_authorized).toBe(true);
    expect(intake.execution_blocked).toBe(false);
    expect(intake.production_blocked).toBe(true);
    expect(policy).toContain("sinal **independente, autorizado, opaco e agregado**");
    expect(policy).toContain("Produção permanece bloqueada");
    expect(gate).toContain("Produção permanece bloqueada");
  });
});
