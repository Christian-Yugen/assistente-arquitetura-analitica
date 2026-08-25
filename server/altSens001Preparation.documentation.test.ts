import { readFileSync } from "node:fs";
import { resolve } from "node:path";
import { describe, expect, it } from "vitest";

const root = resolve(import.meta.dirname, "..");

describe("ALT-SENS-001 preparation", () => {
  it("preserves non-executable aggregate-only policy and production block", () => {
    const intake = readFileSync(resolve(root, "artifacts/intake/ALT-SENS-001.json"), "utf8");
    const policy = readFileSync(resolve(root, "docs/rules/ALT_SENS_001_POLICY_PROPOSAL_001.md"), "utf8");
    const gate = readFileSync(resolve(root, "docs/gates/ALT_SENS_001_RECONSTRUCTION_AUTHORIZATION_001.md"), "utf8");

    expect(intake).toContain('"local_readiness": "intake_required"');
    expect(intake).toContain('"implementation_authorized": false');
    expect(policy).toContain("sinal independente de sensibilidade");
    expect(policy).toContain("não reconhecerá, classificará, nomeará, exibirá ou deduzirá");
    expect(gate).toContain("continuam não autorizados");
    expect(gate).toContain("Produção permanece bloqueada");
  });
});
