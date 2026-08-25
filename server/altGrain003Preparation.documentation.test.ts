import { readFileSync } from "node:fs";
import { resolve } from "node:path";
import { describe, expect, it } from "vitest";

const root = resolve(import.meta.dirname, "..");

describe("ALT-GRAIN-003 preparation", () => {
  it("preserves non-executable aggregate-only policy and production block", () => {
    const intake = readFileSync(resolve(root, "artifacts/intake/ALT-GRAIN-003.json"), "utf8");
    const policy = readFileSync(resolve(root, "docs/rules/ALT_GRAIN_003_POLICY_PROPOSAL_001.md"), "utf8");
    const gate = readFileSync(resolve(root, "docs/gates/ALT_GRAIN_003_RECONSTRUCTION_AUTHORIZATION_001.md"), "utf8");
    expect(intake).toContain('"local_readiness": "intake_required"');
    expect(intake).toContain('"implementation_authorized": false');
    expect(policy).toContain("sinal de granularidade já inferido, opaco e agregado");
    expect(policy).toContain("não afirmará qual deve ser a entidade, o evento, a chave ou o fato do modelo");
    expect(gate).toContain("continuam não autorizados");
    expect(gate).toContain("Produção permanece bloqueada");
  });
});
