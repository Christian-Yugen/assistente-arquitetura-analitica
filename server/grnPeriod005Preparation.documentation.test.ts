import { readFileSync } from "node:fs";
import { resolve } from "node:path";
import { describe, expect, it } from "vitest";

const root = resolve(import.meta.dirname, "..");

describe("GRN-PERIOD-005 preparation", () => {
  it("registra a Proposta A documental sem autorização de execução", () => {
    const intake = JSON.parse(readFileSync(resolve(root, "artifacts/intake/GRN-PERIOD-005.json"), "utf8"));
    const policy = readFileSync(resolve(root, "docs/rules/GRN_PERIOD_005_POLICY_PROPOSAL_001.md"), "utf8");
    const gate = readFileSync(resolve(root, "docs/gates/GRN_PERIOD_005_RECONSTRUCTION_AUTHORIZATION_001.md"), "utf8");

    expect(intake.rule.rule_id).toBe("GRN-PERIOD-005");
    expect(intake.local_readiness).toBe("intake_required");
    expect(intake.authorization.implementation_authorized).toBe(false);
    expect(intake.execution_blocked).toBe(true);
    expect(intake.production_blocked).toBe(true);
    expect(policy).toContain("sinal **independente, autorizado, opaco e agregado**");
    expect(policy).toContain("não valida nem afirma que qualquer período seja correto");
    expect(policy).toContain("Produção permanece bloqueada");
    expect(gate).toContain("autorização explícita adicional de Chris para código");
    expect(gate).toContain("Produção permanece bloqueada");
  });
});
