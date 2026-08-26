import { readFileSync } from "node:fs";
import { resolve } from "node:path";
import { describe, expect, it } from "vitest";

const root = resolve(import.meta.dirname, "..");

describe("MDL-DIMEXTRACT-016 preparation boundaries", () => {
  it("preserva a preparação documental e bloqueia execução e produção", () => {
    const intake = JSON.parse(readFileSync(resolve(root, "artifacts/intake/MDL-DIMEXTRACT-016.json"), "utf8"));
    const policy = readFileSync(resolve(root, "docs/rules/MDL_DIMEXTRACT_016_POLICY_PROPOSAL_001.md"), "utf8");
    const gate = readFileSync(resolve(root, "docs/gates/MDL_DIMEXTRACT_016_RECONSTRUCTION_AUTHORIZATION_001.md"), "utf8");

    expect(intake.rule.rule_id).toBe("MDL-DIMEXTRACT-016");
    expect(intake.local_readiness).toBe("intake_required");
    expect(intake.authorization.implementation_authorized).toBe(false);
    expect(intake.execution_blocked).toBe(true);
    expect(intake.production_blocked).toBe(true);
    expect(policy).toContain("sinal **independente, autorizado, opaco e agregado**");
    expect(policy).toContain("Produção permanece bloqueada");
    expect(gate).toContain("Produção permanece bloqueada");
  });
});
