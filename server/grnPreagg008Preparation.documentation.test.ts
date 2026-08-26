import { readFileSync } from "node:fs";
import { resolve } from "node:path";
import { describe, expect, it } from "vitest";

const root = resolve(import.meta.dirname, "..");

describe("GRN-PREAGG-008 policy boundaries", () => {
  it("preserva a Proposta A documental e o bloqueio produtivo após a autorização draft", () => {
    const intake = JSON.parse(readFileSync(resolve(root, "artifacts/intake/GRN-PREAGG-008.json"), "utf8"));
    const policy = readFileSync(resolve(root, "docs/rules/GRN_PREAGG_008_POLICY_PROPOSAL_001.md"), "utf8");
    const gate = readFileSync(resolve(root, "docs/gates/GRN_PREAGG_008_RECONSTRUCTION_AUTHORIZATION_001.md"), "utf8");

    expect(intake.rule.rule_id).toBe("GRN-PREAGG-008");
    expect(intake.local_readiness).toBe("executable_draft");
    expect(intake.authorization.implementation_authorized).toBe(true);
    expect(intake.execution_blocked).toBe(false);
    expect(intake.production_blocked).toBe(true);
    expect(policy).toContain("sinal **independente, autorizado, opaco e agregado**");
    expect(policy).toContain("não afirma, valida, calcula, determina ou cria agregação");
    expect(policy).toContain("Produção permanece bloqueada");
    expect(gate).toContain("Chris — “autorizado”");
    expect(gate).toContain("Produção permanece bloqueada");
  });
});
